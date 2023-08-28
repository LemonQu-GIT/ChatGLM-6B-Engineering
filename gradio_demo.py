import gradio as gr
import mdtex2html, requests
from plugins import *
from urllib.parse import quote as url_encode

def postprocess(self, y):
	if y is None:
		return []
	for i, (message, response) in enumerate(y):
		y[i] = (
			None if message is None else mdtex2html.convert((message)),
			None if response is None else mdtex2html.convert(response),
		)
	return y

gr.Chatbot.postprocess = postprocess

def parse_text(text):
	"""copy from https://github.com/GaiZhenbiao/ChuanhuChatGPT/"""
	lines = text.split("\n")
	lines = [line for line in lines if line != ""]
	count = 0
	for i, line in enumerate(lines):
		if "```" in line:
			count += 1
			items = line.split('`')
			if count % 2 == 1:
				lines[i] = f'<pre><code class="language-{items[-1]}">'
			else:
				lines[i] = f'<br></code></pre>'
		else:
			if i > 0:
				if count % 2 == 1:
					line = line.replace("`", "\`")
					line = line.replace("<", "&lt;")
					line = line.replace(">", "&gt;")
					line = line.replace(" ", "&nbsp;")
					line = line.replace("*", "&ast;")
					line = line.replace("_", "&lowbar;")
					line = line.replace("-", "&#45;")
					line = line.replace(".", "&#46;")
					line = line.replace("!", "&#33;")
					line = line.replace("(", "&#40;")
					line = line.replace(")", "&#41;")
					line = line.replace("$", "&#36;")
				lines[i] = "<br>"+line
	text = "".join(lines)
	return text

def predict(input, chatbot, history, feature):
	print(feature)
	bool_feature = [False, False, False, False]
	if 'Web' in feature:
		bool_feature[0] = True
	if 'Weather' in feature:
		bool_feature[1] = True
	if 'Date' in feature:
		bool_feature[2] = True
	if 'Markmap' in feature:
		bool_feature[3] = True
	change_feature(bool_feature)
	chatbot.append((parse_text(input), ""))
	url = f"{get_config()['basic']['host']}:8003/api/chat?prompt={url_encode(input)}"
	response = requests.get(url, stream=True)
	resp = ""
	for chunk in response.iter_content(chunk_size=1024):
		resp = chunk.decode('utf-8', 'ignore').replace("data: ",'')
		chatbot[-1] = (parse_text(input), parse_text(resp))
		history = [parse_text(input), parse_text(resp)]
		yield chatbot, history

def upload_file(files):
    file_paths = [file.name for file in files]
    print(file_paths)
    url = f"{get_config()['basic']['host']}:8003/api/upload"
    files = {'file': open(file_paths[0],'rb')}
    requests.post(url=url,files=files)
    return file_paths

def reset_user_input():
	return gr.update(value='')

def reset_state():
	requests.post(f"{get_config()['basic']['host']}:8003/api/delete")
	return [], []


def change_feature(feature: list):
    requests.post(f"{get_config()['basic']['host']}:8003/api/config?web={feature[0]}&weather={feature[1]}&date={feature[2]}&markmap={feature[3]}&sd=False")
    
with gr.Blocks() as demo:
	with gr.Row():
		with gr.Column(scale=1):
			gr.HTML("""<h1>ChatGLM-6B-Engineering</h1>""")
			feature = gr.CheckboxGroup(["Web", "Weather", "Date", "Markmap"], label="Feature", info="Choose the feature you want to use")
			file_output = gr.File()
			upload_button = gr.UploadButton("Upload File", file_count="multiple")
			emptyBtn = gr.Button("Clear History")
		with gr.Column(scale=5):
			chatbot = gr.Chatbot()
			user_input = gr.Textbox(show_label=False, lines=6, placeholder="Enter your question here.").style(container=False)
			submitBtn = gr.Button("Submit", variant="primary")
	history = gr.State([])
	submitBtn.click(change_feature, [feature], show_progress=True)  
	submitBtn.click(predict, [user_input, chatbot, history, feature], [chatbot, history], show_progress=True)
	submitBtn.click(reset_user_input, [], [user_input])
	emptyBtn.click(reset_state, outputs=[chatbot, history], show_progress=True)
	upload_button.upload(upload_file, upload_button, file_output)

demo.queue().launch(share=False)