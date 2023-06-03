# ChatGLM-6B Web UI

本项目参考于

* https://gitee.com/MIEAPP/chatai-vue
* https://gitee.com/MIEAPP/chatai-python
* https://github.com/LemonQu-GIT/ChatGLM-6B-Engineering

并进行多许修改以适配 ChatGLM-6B

项目基于 MIT License

## 示例

![image](img\main_menu.png)

### 基本对话

![image](img\default.png "基本对话")

### 网络搜索

![image](img\gpt4.png "网络搜索")

### Stable Diffusion

![image](img\sd.png "Stable Diffusion")

### Generate Code

![image](img\web_1.png "Generate Code")

![image](img\web_2.png "Generate Code")

## 部署

* ChatGLM-6B

  > https://github.com/THUDM/ChatGLM-6B

* Stable Diffusion

  > 由于最新版的 Stable Diffusion API 调用存在问题，本项目 Stable Diffusion 使用以下版本
  >
  > https://github.com/AUTOMATIC1111/stable-diffusion-webui/tree/35b1775b32a07f1b7c9dccad61f7aa77027a00fa

* ChatGLM-6B-Engineering

  > https://github.com/LemonQu-GIT/ChatGLM-6B-Engineering

1. 运行 ChatGLM-6B API (Port 8000)

   ```shell
   python api.py
   ```

2. 运行 Stable Diffusion API (Port 7861)

   ```shell
   python webui.py -nowebui
   ```

3. 运行 ChatGLM-6B-WebUI API (Port 8003)

   ```shell
   python front_end.py
   ```

4. 运行 npm (Port 8080) v14.21.3

   ```shell
   npm install -g yarn
   #yarn config set registry https://registry.npm.taobao.org -g
   #yarn config set sass_binary_site http://cdn.npm.taobao.org/dist/node-sass -g
   yarn install
   yarn dev
   ```

   


## 限制

* 对自我认知上会出现问题（如认为自己是由 OpenAI 开发的等）
* 会“随便”生成图片（即用户的命令回复是一张图片等）
* 会对用户有冒犯性的语句
* 生成的图片未加限制（会出现 NSFW img）

如下图

![image](img\offensive.png)