_base_ = [
    '../_base_/datasets/imagenet_bs64_swin_384.py',
    '../_base_/schedules/imagenet_bs4096_AdamW.py',
    '../_base_/default_runtime.py'
]

# model settings
model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='VisionTransformer',
        arch='deit-base',
        img_size=384,
        patch_size=16,
    ),
    neck=None,
    head=dict(
        type='VisionTransformerClsHead',
        num_classes=1000,
        in_channels=768,
        loss=dict(
            type='LabelSmoothLoss', label_smooth_val=0.1, mode='original'),
    ),
    # Change to the path of the pretrained model
    # init_cfg=dict(type='Pretrained', checkpoint=''),
)

# data settings
data = dict(samples_per_gpu=32, workers_per_gpu=5)
