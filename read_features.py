import numpy as np

# 载入 npz 文件
data1 = np.load("/nfs/data3/shuaicong/FlashVTG/qvhighlights_internvideo2/qvhighlight_6b/zzWIB6kuuAQ_660.0_810.0.pt")
data2 = np.load("/nfs/data3/shuaicong/FlashVTG/qvhighlights_internvideo2/qvhighlight_llama_text_feature/qid9999.pt")

# features: (75, 512)
# 列出文件中的所有数组名称
for name in data1.files:
    print(f"{name}: {data1[name]}")

print(type(data2))