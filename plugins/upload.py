from plugins.utils import *
import pdfplumber
from docx import Document
import pandas as pd

def get_suffix(str):
	suffix = str.split(".")[1]
	return "."+suffix

def preview_text(text: str, type: str):
	column = text.count("\n")+1
	response = ""
	files_max_line = get_config()['files']['files_max_line']
	if column > files_max_line:
		column_list = text.split('\n')
		for i in range(round(files_max_line/2)):
			response += column_list[i] + "\n"
		response += "...\n"
		for i in range(len(column_list)-round(files_max_line/2)+1,len(column_list)):
			response += column_list[i] + "\n"
	else:
		response = text
	response = f"```{type}\n{response}\n```"
	return response

def run(filename :str):
	try:
		host = os.environ.get('VUE_APP_API')
	except:
		host = get_config()['API_host']
	suffix = get_suffix(filename)
	log(f"Input file: {filename}, Input file suffix: {suffix}", "INFO")
	quote_filename = quote(filename, safe='<>![]&/:?=.()')
	now = datetime.datetime.now()
	time = now.strftime("%Y-%m-%d %H:%M:%S")
	log("Reading files", "EVENT")
	latest_filesize = os.path.getsize(f"./plugins/uploads/{filename}")
	if latest_filesize < 1024: # type:ignore
		latest_filesize = round(latest_filesize,2),'Byte' # type:ignore
	else: 
		KBX = latest_filesize/1024 # type:ignore
		if KBX < 1024:
			latest_filesize = round(KBX,2),'KB'
		else:
			MBX = KBX /1024
			if MBX < 1024:
				latest_filesize = round(MBX,2),'MB'
			else:
				latest_filesize = round(MBX/1024),'GB'
	latest_filesize = str(latest_filesize[0]) +" "+ str(latest_filesize[1])
	icon = ''
	preview_content = ''
	if suffix in ['.txt','.java','.py','.c','.cpp','.','.js','.html']:
		if suffix == '.txt':
			icon = f'\n<img src="{host}/api/renderfile?filename={quote_filename}&filetime={time}&filesize={latest_filesize}&filetype=text" width="50%" align="middle"/>'
		else:
			icon = f'<img src="{host}/api/renderfile?filename={quote_filename}&filetime={time}&filesize={latest_filesize}&filetype=code" width="50%" align="middle"/>'
		with open(f"./plugins/uploads/{filename}", "r", encoding="utf-8") as f:
			content = f.read()
		#log(f'Input text content: {repr(content)}', "INFO")
		if suffix == ".py":
			file_type = "python"
		else:
			file_type = suffix[1:]
		preview_content = preview_text(content, file_type)
	elif suffix == '.pdf':
		content = ""
		icon = f'\n<img src="{host}/api/renderfile?filename={quote_filename}&filetime={time}&filesize={latest_filesize}&filetype=pdf" width="50%" align="middle"/>'
		with pdfplumber.open(f"./plugins/uploads/{filename}") as pdf:
			for page in pdf.pages:
				content += page.extract_text()
		log(f"Input PDF content: {repr(content)}", "INFO")
	elif suffix == '.csv':
		content = pd.read_csv(f"./plugins/uploads/{filename}")
		log(f"Input CSV content: {repr(content)}", "INFO")
	elif suffix in '.xlsx':
		content = pd.read_excel(f"./plugins/uploads/{filename}")
		log(f"Input Microsoft Excel content: {repr(content)}", "INFO")
	elif suffix in ['.docx', '.doc']:
		doc = Document(f"./plugins/uploads/{filename}")
		content = ""
		for paragraph in doc.paragraphs:
			content += paragraph.text
		log(f"Input Microsoft Word content: {repr(content)}", "INFO")
	else:
		with open(f"./plugins/uploads/{filename}", "rb") as f:
			content = f.read()
	return {"add": f"已知上传的文件内容为：'''{content}'''，", "prefix": icon, "suffix": f"\n{preview_content}"}