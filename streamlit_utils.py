import requests, re, json, io, base64, os
from urllib.parse import quote
from bs4 import BeautifulSoup
from PIL import Image, PngImagePlugin

def ext_zhihu(url):
	if "/answer" in url:
		rep = url.replace('https://www.zhihu.com/question/','')
		rep_l = rep[rep.rfind("/answer"):][7:]
		rep = 'https://www.zhihu.com/question/' + rep.replace("/answer"+rep_l,"")
		return rep
	else:
		return url

def redirect_url(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
	}
	r = requests.get(url, headers=headers, allow_redirects=False)  # 不允许重定向
	if r.status_code == 302:
		real_url = r.headers.get('Location')
	else:
		real_url = re.findall("URL='(.*?)'", r.text)[0]
	return real_url

def search_web(keyword):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	url = quote("https://www.sogou.com/web?query="+str(keyword),safe='/:?=.')
	r = requests.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find_all(class_='struct201102')
	relist = []
	for items in item_list:
		item_prelist = items.find(class_ = "vr-title")
		item_title = re.sub(r'(<[^>]+>|\s)','',str(item_prelist))
		href_s = item_prelist.find(class_ = "", href=True)
		href = href_s["href"]
		if href[0] == "/":
			href_f = redirect_url("https://www.sogou.com"+href)
		else:
			href_f = href
		relist.append([item_title, href_f])
	return relist

def search_zhihu_que(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	r = requests.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find_all(class_='List-item')
	relist = []
	for items in item_list:
		item_prelist = items.find(class_ = "RichText ztext CopyrightRichText-richText css-1g0fqss")
		item_title = re.sub(r'(<[^>]+>|\s)','',str(item_prelist))
		relist.append(item_title)
	return relist

def search_zhihu_zhuanlan(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	r = requests.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find(class_='RichText ztext Post-RichText css-1g0fqss')
	item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list))
	return item_title


def search_baike(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	if "baike.sogou.com" in url:
		r = requests.get(url, headers=headers)
		html_s = r.text
		soup_s = BeautifulSoup(html_s, 'html.parser')
		item_list_s = soup_s.find(class_='lemma_name')
		item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list_s))
		item_title = item_title.replace('编辑词条','')
		r = requests.get("https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key="+item_title+"&bk_length=600", headers=headers)
		resp = r.text.encode('utf-8').decode('gbk')
		resp_json = json.loads(resp)
		answer = resp_json.get('abstract')
		if answer == None:
			answer_f = soup_s.find(class_='abstract')
			item_title = re.sub(r'(<[^>]+>|\s)','',str(answer_f))
			return item_title
		else:
			return resp_json.get('abstract')
	else:
		r = requests.get("https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key="+url+"&bk_length=600", headers=headers)
		resp = r.text.encode('utf-8').decode('gbk')
		resp_json = json.loads(resp)
		answer = resp_json.get('abstract')
		return answer


def search_wx(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	r = requests.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find(class_='rich_media_wrp')
	item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list))
	return item_title

def search_news_sohu(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	r = requests.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find(class_='article')
	item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list))
	return item_title

def search_news_163(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	r = requests.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find(class_='post_body')
	item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list))
	return item_title

def search_bilibili(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	r = requests.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find(class_='article-content')
	item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list))
	return item_title

def search_csdn(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	r = requests.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find(class_='article_content clearfix')
	item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list))
	return item_title

def search_github(keyword,opt):
	token = os.getenv('git_token')
	if not token == None:
		headers={"Authorization":"token "+ str(token)}
	else:
		headers={}
	new_key = ""
	for ch in keyword:
		if not u'\u4e00' <= ch <= u'\u9fff':
			new_key += ch
	url = quote("https://api.github.com/search/repositories?q="+str(new_key)+"&sort=stars&order=desc",safe='/:?=.&')
	r = requests.get(url, headers=headers)
	resp_json = json.loads(r.text)
	items = resp_json.get('items')
	relist = []
	items = items[0:int(opt)]
	for repos in items:
		item_json = json.dumps(repos)
		item_json = json.loads(str(item_json))
		addr = item_json.get('full_name')
		url = quote("https://api.github.com/repos/"+str(addr)+"/readme",safe='/:?=.&')
		r = requests.get(url, headers=headers)
		repo_json = json.loads(r.text)
		readme = repo_json.get('download_url')
		r = requests.get(str(readme).replace("https://raw.githubusercontent.com/","https://raw.fastgit.org/"), headers=headers)
		relist.append(repr(r.text))
	return relist

def search_main(item, feature):
	web_list = search_web(item)
	return_list = []
	print(feature)
	#print(web_list)
	if '百科' in feature:
		ans = str(search_baike(item))
		if not ans == "":
			return_list.append(ans)
	if 'GitHub' in feature:
		ans = str(search_github(item,1))
		if not ans == "":
			return_list.append(ans)
	for items in web_list:
		if "zhihu.com/question/" in items[1] and '知乎回复' in feature:
			return_list.append(str(search_zhihu_que(ext_zhihu(items[1]))))
		if "baike.sogou.com" in items[1] and '百科' in feature:
			return_list.append(str(search_baike(items[1])))
		if "mp.weixin.qq.com" in items[1] and '微信公众号' in feature:
			return_list.append(str(search_wx(items[1])))
		if "zhuanlan.zhihu.com" in items[1] and '知乎专栏' in feature:
			return_list.append(str(search_zhihu_zhuanlan(items[1])))
		if "163.com/dy/article/" in items[1] and '新闻' in feature:
			return_list.append(str(search_news_163(items[1])))
		if "sohu.com/a/" in items[1] and '新闻' in feature:
			return_list.append(str(search_news_sohu(items[1])))
		if "bilibili.com/read/" in items[1] and 'B站专栏' in feature:
			return_list.append(str(search_bilibili(items[1])))	
		if "blog.csdn.net" in items[1] and 'CSDN' in feature:
			return_list.append(str(search_csdn(items[1])))
	return return_list

def test_if_zhcn(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def translate(word):
    if test_if_zhcn(word):
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
        key = {
            'type': "AUTO",
            'i': word,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "ue": "UTF-8",
            "action": "FY_BY_CLICKBUTTON",
            "typoResult": "true"
        }
        response = requests.post(url, data=key)
        if response.status_code == 200:
            list_trans = response.text
            result = json.loads(list_trans)
            return result['translateResult'][0][0]['tgt']
    else:
        return word

def chatglm_json(prompt, history, max_length, top_p, temperature):
    url = "http://127.0.0.1:8000"
    payload = {
        "prompt": prompt,
        "history": history,
        "max_length": max_length,
        "top_p": top_p,
        "temperature": temperature
    }
    response = requests.post(url, json=payload)
    json_resp_raw = response.json()
    json_resp_raw_list = json.dumps(json_resp_raw)
    return json_resp_raw_list

def stable_diffusion(Pprompt,Nprompt):
    url = "http://127.0.0.1:7861"
    payload = {
        "prompt": Pprompt,
        "steps": 5,
        "negative_prompt": Nprompt
    }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save('stable_diffusion.png', pnginfo=pnginfo)

