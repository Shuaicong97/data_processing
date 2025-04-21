import torch

# 加载 checkpoint 文件
checkpoint = torch.load("/nfs/data3/shuaicong/RMOT/outputs/ovis_with_checkpoint0_5_epochs/checkpoint05.pth", map_location="cpu")

# 查看 checkpoint 中的键
print("Keys in checkpoint:", checkpoint.keys())

# 如果有 'epoch' 字段，就打印出来
if 'epoch' in checkpoint:
    print(f"Checkpoint saved at epoch: {checkpoint['epoch']}")
else:
    print("No 'epoch' key found in the checkpoint.")
