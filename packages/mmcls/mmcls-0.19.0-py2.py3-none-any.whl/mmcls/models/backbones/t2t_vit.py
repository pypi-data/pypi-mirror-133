# Copyright (c) OpenMMLab. All rights reserved.
from copy import deepcopy
from typing import Sequence

import numpy as np
import torch
import torch.nn as nn
from mmcv.cnn import build_norm_layer
from mmcv.cnn.bricks.transformer import FFN
from mmcv.cnn.utils.weight_init import trunc_normal_
from mmcv.runner.base_module import BaseModule, ModuleList

from ..builder import BACKBONES
from ..utils import MultiheadAttention
from .base_backbone import BaseBackbone


class T2TTransformerLayer(BaseModule):
    """Transformer Layer for T2T_ViT.

    Comparing with :obj:`TransformerEncoderLayer` in ViT, it supports
    different ``input_dims`` and ``embed_dims``.

    Args:
        embed_dims (int): The feature dimension.
        num_heads (int): Parallel attention heads.
        feedforward_channels (int): The hidden dimension for FFNs
        input_dims (int, optional): The input token dimension.
            Defaults to None.
        drop_rate (float): Probability of an element to be zeroed
            after the feed forward layer. Defaults to 0.
        attn_drop_rate (float): The drop out rate for attention output weights.
            Defaults to 0.
        drop_path_rate (float): Stochastic depth rate. Defaults to 0.
        num_fcs (int): The number of fully-connected layers for FFNs.
            Defaults to 2.
        qkv_bias (bool): enable bias for qkv if True. Defaults to True.
        qk_scale (float, optional): Override default qk scale of
            ``(input_dims // num_heads) ** -0.5`` if set. Defaults to None.
        act_cfg (dict): The activation config for FFNs.
            Defaluts to ``dict(type='GELU')``.
        norm_cfg (dict): Config dict for normalization layer.
            Defaults to ``dict(type='LN')``.
        init_cfg (dict, optional): Initialization config dict.
            Defaults to None.

    Notes:
        In general, ``qk_scale`` should be ``head_dims ** -0.5``, i.e.
        ``(embed_dims // num_heads) ** -0.5``. However, in the official
        code, it uses ``(input_dims // num_heads) ** -0.5``, so here we
        keep the same with the official implementation.
    """

    def __init__(self,
                 embed_dims,
                 num_heads,
                 feedforward_channels,
                 input_dims=None,
                 drop_rate=0.,
                 attn_drop_rate=0.,
                 drop_path_rate=0.,
                 num_fcs=2,
                 qkv_bias=False,
                 qk_scale=None,
                 act_cfg=dict(type='GELU'),
                 norm_cfg=dict(type='LN'),
                 init_cfg=None):
        super(T2TTransformerLayer, self).__init__(init_cfg=init_cfg)

        self.v_shortcut = True if input_dims is not None else False
        input_dims = input_dims or embed_dims

        self.norm1_name, norm1 = build_norm_layer(
            norm_cfg, input_dims, postfix=1)
        self.add_module(self.norm1_name, norm1)

        self.attn = MultiheadAttention(
            input_dims=input_dims,
            embed_dims=embed_dims,
            num_heads=num_heads,
            attn_drop=attn_drop_rate,
            proj_drop=drop_rate,
            dropout_layer=dict(type='DropPath', drop_prob=drop_path_rate),
            qkv_bias=qkv_bias,
            qk_scale=qk_scale or (input_dims // num_heads)**-0.5,
            v_shortcut=self.v_shortcut)

        self.norm2_name, norm2 = build_norm_layer(
            norm_cfg, embed_dims, postfix=2)
        self.add_module(self.norm2_name, norm2)

        self.ffn = FFN(
            embed_dims=embed_dims,
            feedforward_channels=feedforward_channels,
            num_fcs=num_fcs,
            ffn_drop=drop_rate,
            dropout_layer=dict(type='DropPath', drop_prob=drop_path_rate),
            act_cfg=act_cfg)

    @property
    def norm1(self):
        return getattr(self, self.norm1_name)

    @property
    def norm2(self):
        return getattr(self, self.norm2_name)

    def forward(self, x):
        if self.v_shortcut:
            x = self.attn(self.norm1(x))
        else:
            x = x + self.attn(self.norm1(x))
        x = self.ffn(self.norm2(x), identity=x)
        return x


class T2TModule(BaseModule):
    """Tokens-to-Token module.

    "Tokens-to-Token module" (T2T Module) can model the local structure
    information of images and reduce the length of tokens progressively.

    Args:
        img_size (int): Input image size
        in_channels (int): Number of input channels
        embed_dims (int): Embedding dimension
        token_dims (int): Tokens dimension in T2TModuleAttention.
        use_performer (bool): If True, use Performer version self-attention to
            adopt regular self-attention. Defaults to False.
        init_cfg (dict, optional): The extra config for initialization.
            Default: None.

    Notes:
        Usually, ``token_dim`` is set as a small value (32 or 64) to reduce
        MACs
    """

    def __init__(
        self,
        img_size=224,
        in_channels=3,
        embed_dims=384,
        token_dims=64,
        use_performer=False,
        init_cfg=None,
    ):
        super(T2TModule, self).__init__(init_cfg)

        self.embed_dims = embed_dims

        self.soft_split0 = nn.Unfold(
            kernel_size=(7, 7), stride=(4, 4), padding=(2, 2))
        self.soft_split1 = nn.Unfold(
            kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.soft_split2 = nn.Unfold(
            kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))

        if not use_performer:
            self.attention1 = T2TTransformerLayer(
                input_dims=in_channels * 7 * 7,
                embed_dims=token_dims,
                num_heads=1,
                feedforward_channels=token_dims)

            self.attention2 = T2TTransformerLayer(
                input_dims=token_dims * 3 * 3,
                embed_dims=token_dims,
                num_heads=1,
                feedforward_channels=token_dims)

            self.project = nn.Linear(token_dims * 3 * 3, embed_dims)
        else:
            raise NotImplementedError("Performer hasn't been implemented.")

        # there are 3 soft split, stride are 4,2,2 separately
        self.num_patches = (img_size // (4 * 2 * 2))**2

    def forward(self, x):
        # step0: soft split
        x = self.soft_split0(x).transpose(1, 2)

        for step in [1, 2]:
            # re-structurization/reconstruction
            attn = getattr(self, f'attention{step}')
            x = attn(x).transpose(1, 2)
            B, C, new_HW = x.shape
            x = x.reshape(B, C, int(np.sqrt(new_HW)), int(np.sqrt(new_HW)))

            # soft split
            soft_split = getattr(self, f'soft_split{step}')
            x = soft_split(x).transpose(1, 2)

        # final tokens
        x = self.project(x)
        return x


def get_sinusoid_encoding(n_position, embed_dims):
    """Generate sinusoid encoding table.

    Sinusoid encoding is a kind of relative position encoding method came from
    `Attention Is All You Need<https://arxiv.org/abs/1706.03762>`_.

    Args:
        n_position (int): The length of the input token.
        embed_dims (int): The position embedding dimension.

    Returns:
        :obj:`torch.FloatTensor`: The sinusoid encoding table.
    """

    def get_position_angle_vec(position):
        return [
            position / np.power(10000, 2 * (i // 2) / embed_dims)
            for i in range(embed_dims)
        ]

    sinusoid_table = np.array(
        [get_position_angle_vec(pos) for pos in range(n_position)])
    sinusoid_table[:, 0::2] = np.sin(sinusoid_table[:, 0::2])  # dim 2i
    sinusoid_table[:, 1::2] = np.cos(sinusoid_table[:, 1::2])  # dim 2i+1

    return torch.FloatTensor(sinusoid_table).unsqueeze(0)


@BACKBONES.register_module()
class T2T_ViT(BaseBackbone):
    """Tokens-to-Token Vision Transformer (T2T-ViT)

    A PyTorch implementation of `Tokens-to-Token ViT: Training Vision
    Transformers from Scratch on ImageNet <https://arxiv.org/abs/2101.11986>`_

    Args:
        img_size (int): Input image size.
        in_channels (int): Number of input channels.
        embed_dims (int): Embedding dimension.
        t2t_cfg (dict): Extra config of Tokens-to-Token module.
            Defaults to an empty dict.
        drop_rate (float): Dropout rate after position embedding.
            Defaults to 0.
        num_layers (int): Num of transformer layers in encoder.
            Defaults to 14.
        out_indices (Sequence | int): Output from which stages.
            Defaults to -1, means the last stage.
        layer_cfgs (Sequence | dict): Configs of each transformer layer in
            encoder. Defaults to an empty dict.
        drop_path_rate (float): stochastic depth rate. Defaults to 0.
        norm_cfg (dict): Config dict for normalization layer. Defaults to
            ``dict(type='LN')``.
        final_norm (bool): Whether to add a additional layer to normalize
            final feature map. Defaults to True.
        output_cls_token (bool): Whether output the cls_token.
            Defaults to True.
        init_cfg (dict, optional): The Config for initialization.
            Defaults to None.
    """

    def __init__(self,
                 img_size=224,
                 in_channels=3,
                 embed_dims=384,
                 t2t_cfg=dict(),
                 drop_rate=0.,
                 num_layers=14,
                 out_indices=-1,
                 layer_cfgs=dict(),
                 drop_path_rate=0.,
                 norm_cfg=dict(type='LN'),
                 final_norm=True,
                 output_cls_token=True,
                 init_cfg=None):
        super(T2T_ViT, self).__init__(init_cfg)

        # Token-to-Token Module
        self.tokens_to_token = T2TModule(
            img_size=img_size,
            in_channels=in_channels,
            embed_dims=embed_dims,
            **t2t_cfg)
        num_patches = self.tokens_to_token.num_patches

        # Class token
        self.output_cls_token = output_cls_token
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dims))
        self.num_extra_tokens = 1

        # Position Embedding
        sinusoid_table = get_sinusoid_encoding(num_patches + 1, embed_dims)
        self.register_buffer('pos_embed', sinusoid_table)
        self.drop_after_pos = nn.Dropout(p=drop_rate)

        if isinstance(out_indices, int):
            out_indices = [out_indices]
        assert isinstance(out_indices, Sequence), \
            f'"out_indices" must by a sequence or int, ' \
            f'get {type(out_indices)} instead.'
        for i, index in enumerate(out_indices):
            if index < 0:
                out_indices[i] = num_layers + index
                assert out_indices[i] >= 0, f'Invalid out_indices {index}'
        self.out_indices = out_indices

        dpr = [x for x in np.linspace(0, drop_path_rate, num_layers)]
        self.encoder = ModuleList()
        for i in range(num_layers):
            if isinstance(layer_cfgs, Sequence):
                layer_cfg = layer_cfgs[i]
            else:
                layer_cfg = deepcopy(layer_cfgs)
            layer_cfg = {
                'embed_dims': embed_dims,
                'num_heads': 6,
                'feedforward_channels': 3 * embed_dims,
                'drop_path_rate': dpr[i],
                'qkv_bias': False,
                'norm_cfg': norm_cfg,
                **layer_cfg
            }

            layer = T2TTransformerLayer(**layer_cfg)
            self.encoder.append(layer)

        self.final_norm = final_norm
        if final_norm:
            self.norm = build_norm_layer(norm_cfg, embed_dims)[1]
        else:
            self.norm = nn.Identity()

    def init_weights(self):
        super().init_weights()

        if (isinstance(self.init_cfg, dict)
                and self.init_cfg['type'] == 'Pretrained'):
            # Suppress custom init if use pretrained model.
            return

        trunc_normal_(self.cls_token, std=.02)

    def forward(self, x):
        B = x.shape[0]
        x = self.tokens_to_token(x)
        num_patches = self.tokens_to_token.num_patches
        patch_resolution = [int(np.sqrt(num_patches))] * 2

        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)
        x = x + self.pos_embed
        x = self.drop_after_pos(x)

        outs = []
        for i, layer in enumerate(self.encoder):
            x = layer(x)

            if i == len(self.encoder) - 1 and self.final_norm:
                x = self.norm(x)

            if i in self.out_indices:
                B, _, C = x.shape
                patch_token = x[:, 1:].reshape(B, *patch_resolution, C)
                patch_token = patch_token.permute(0, 3, 1, 2)
                cls_token = x[:, 0]
                if self.output_cls_token:
                    out = [patch_token, cls_token]
                else:
                    out = patch_token
                outs.append(out)

        return tuple(outs)
