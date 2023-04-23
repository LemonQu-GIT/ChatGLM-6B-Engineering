# ChatGLM-6B-Engineering

Re-edit from [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)

https://www.bilibili.com/video/BV1gX4y1B7PV

## 介绍

ChatGLM-6B 是一个开源的、支持中英双语的对话语言模型，基于 [General Language Model (GLM)](https://github.com/THUDM/GLM) 架构，具有 62 亿参数。结合模型量化技术，用户可以在消费级的显卡上进行本地部署

本项目基于 ChatGLM-6B 进行了后期调教，支持网上搜索及生成图片

生成图片则需要本地部署 [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 并加载 API：

```powershell
python webui.py --xformers --nowebui
```

运行程序需要先运行 api.py，

再运行：

```powershell
streamlit run streamlit_new.py
```

加载完成后在 http://localhost:8501/ 中查看

## 运行时错误

AssertionError: Torch not compiled with CUDA enabled

RuntimeError: CUDA error: no kernel image is available for execution on the device

请运行

```powershell
nvidia-smi
```

及

```powershell
nvcc -V
```

查看结果 如都正常无 error ，请运行

```python
import torch
print(torch.cuda.is_available())
```

**如返回为 True，**

请将在api.py中第57行

```python
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(4).half().cuda()
```

更改为

```python
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
```

**如返回为 False**

请确认自己是否已安装gpu版本的torch

可参考网络教程

若设备无 nvidia 显卡，可参考 [Readme](https://github.com/THUDM/ChatGLM-6B/blob/main/README.md) 修改模型为 cpu 量化模型

## 引用

Forked from https://github.com/THUDM/ChatGLM-6B
