import torch

hifigan_ts_ckpt = './ckpts/hfgan-fcm_base2-L-16k-v0.1.1.ts'
hifigan_ts = torch.jit.load(hifigan_ts_ckpt).cuda()

def VOC(mel):
    return hifigan_ts(mel)