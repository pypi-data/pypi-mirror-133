_base_ = '../repvgg-A1_4xb64-coslr-120e_in1k.py'

model = dict(backbone=dict(deploy=True))
