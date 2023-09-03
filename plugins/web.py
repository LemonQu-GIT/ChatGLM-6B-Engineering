import json, requests, re, time
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
from plugins.utils import *

def get_basic_url(url: str):
	try:
		method = url.replace("http://", "").replace("https://", "")
		method = method.split('/')
		return method[0]
	except:
		return ''


def generate_reference(reference: list):
	response = "\n了解更多信息：\n "
	for urls in reference:
		response += f"> * [{get_basic_url(urls)}]({urls})\n"
	return response

def filter_tags(htmlstr):
	re_cdata=re.compile(r'//<!\[CDATA\[[^>]*//\]\]>',re.I)
	re_script=re.compile(r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
	re_style=re.compile(r'<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
	re_br=re.compile(r'<br\s*?/?>')
	re_h=re.compile(r'</?\w+[^>]*>')
	re_comment=re.compile(r'<!--[^>]*-->')
	s=re_cdata.sub('',htmlstr)
	s=re_script.sub('',s)
	s=re_style.sub('',s)
	s=re_br.sub('\n',s)
	s=re_h.sub('',s)
	s=re_comment.sub('',s)
	blank_line=re.compile('\n+')
	s=blank_line.sub('\n',s)
	s=replaceCharEntity(s)
	return s

def replaceCharEntity(htmlstr):
	CHAR_ENTITIES={'nbsp':' ','160':' ',
				'lt':'<','60':'<',
				'gt':'>','62':'>',
				'amp':'&','38':'&',
				'quot':'"','34':'"',}

	re_charEntity=re.compile(r'&#?(?P<name>\w+);')
	sz=re_charEntity.search(htmlstr)
	while sz:
		key=sz.group('name')
		try:
			htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
			sz=re_charEntity.search(htmlstr)
		except KeyError:
			htmlstr=re_charEntity.sub('',htmlstr,1)
			sz=re_charEntity.search(htmlstr)
	return htmlstr

def repalce(s,re_exp,repl_string):
	return re_exp.sub(repl_string,s)

def search_plain(url):
	try:
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Chrome(options=options)
		driver.set_page_load_timeout(10)
		driver.set_script_timeout(10)
		try:
			driver.get(url)
		except Exception:
			driver.execute_script('window.stop()')
		for i in range(0, 20000, 350):
			time.sleep(0.02)
			driver.execute_script('window.scrollTo(0, %s)' % i)
		html = driver.execute_script("return document.documentElement.outerHTML")
		html = filter_tags(html).replace('\n','').replace('\r','').replace('\t','')
		return repr(html)
	except:
		log(f"Error fetching url: {url}", 'ERROR')
		return "None"
  
def test_if_url_ignore(test_url):
	for url in get_config().get("web").get('ignore_url'):
		if url in test_url:
			return True
	return False

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
	if str(get_config['web']['browser_name']).lower() == "chrome":
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		options.add_experimental_option('useAutomationExtension', False)
		options.add_argument('lang=zh-CN,en-US,en')
		driver = webdriver.Chrome(options=options)
	elif str(get_config['web']['browser_name']).lower() == "edge":
		options = webdriver.EdgeOptions()
		options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Edge(options=options)
	elif str(get_config['web']['browser_name']).lower() == "firefox":
		options = webdriver.FirefoxOptions()
		options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Firefox(options=options)
	elif str(get_config['web']['browser_name']).lower() == "ie":
		options = webdriver.IeOptions()
		options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		driver = webdriver.Ie(options=options)
	else:
		log('Incompatible browser name.', "CRITICAL")
	driver.get(quote("https://cn.bing.com/search?q="+str(keyword),safe='/:?=.'))
	for i in range(0, 20000, 350):
		time.sleep(0.02)
		driver.execute_script('window.scrollTo(0, %s)' % i)
	html = driver.execute_script("return document.documentElement.outerHTML")
	driver.close()
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find_all(class_='b_algo')
	relist = []
	for items in item_list:
		item_prelist = items.find('h2')
		item_title = re.sub(r'(<[^>]+>|\s)','',str(item_prelist))
		href_s = item_prelist.find("a", href=True)
		href = href_s["href"]
		relist.append([item_title, href])
	item_list = soup.find_all(class_ ='ans_nws ans_nws_fdbk')
	for items in item_list:
		for i in range(1,10):
			item_prelist = items.find(class_ = f"nws_cwrp nws_itm_cjk item{i}", url=True, titletext=True)
			if item_prelist is not None:
				url = item_prelist["url"].replace('\ue000','').replace('\ue001','')
				title = item_prelist["titletext"]
				relist.append([title, url])
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

def search_baidu_zhidao(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
	}
	r = requests.get(url, headers=headers)
	r.encoding = 'utf-8'
	html = str(r.text)
	soup = BeautifulSoup(html, 'html.parser')
	item_list = soup.find(class_='rich-content-container rich-text-')
	item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list))
	return item_title

def search_baike(keyword):
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
	for items in relist:
		if "baike.sogou.com" in items[1]:
			r = requests.get(items[1], headers=headers)
			html_s = r.text
			soup_s = BeautifulSoup(html_s, 'html.parser')
			item_list_s = soup_s.find(class_='lemma_name')
			item_title = re.sub(r'(<[^>]+>|\s)','',str(item_list_s))
			item_title = item_title.replace('编辑词条','')
			answer_sogou = soup_s.find(class_='abstract')
			answer_sogou = re.sub(r'(<[^>]+>|\s)','',str(answer_sogou))
			r = requests.get("https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key="+item_title+"&bk_length=600", headers=headers)
			resp = r.text.encode('utf-8').decode('gbk')
			resp_json = json.loads(resp)
			answer_baidu = resp_json.get('abstract')
			refer = resp_json.get('url')
			return [[items[1], refer], [answer_sogou, answer_baidu]]
		else:
			r = requests.get("https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key="+url+"&bk_length=600", headers=headers)
			resp = r.text.encode('utf-8').decode('gbk')
			resp_json = json.loads(resp)
			answer = resp_json.get('abstract')
			refer = resp_json.get('url')
			return [[refer], [answer]]

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

def search_github(keyword):
	token = get_config().get("web").get('git_token')
	if not token == "":
		headers={"Authorization":"token "+ str(token)}
	else:
		headers={}
	new_key = ""
	for ch in keyword:
		if not u'\u4e00' <= ch <= u'\u9fff':
			new_key += ch
	url = quote("https://api.github.com/search/repositories?q="+str(new_key)+"&sort=match&order=desc",safe='/:?=.&')
	r = requests.get(url)
	resp_json = json.loads(r.text)
	items = resp_json.get('items')
	try:
		item_json = json.dumps(items[0])
		item_json = json.loads(str(item_json))
		addr = item_json.get('full_name')
		url = quote("https://api.github.com/repos/"+str(addr)+"/readme",safe='/:?=.&')
		r = requests.get(url)
		repo_json = json.loads(r.text)
		readme = repo_json.get('download_url')
		readme = readme.replace("https://raw.githubusercontent.com/", "https://raw.fastgit.org/")
		r = requests.get(str(readme))
		relist = [addr, r.text]
		return relist
	except:
		return []

def search_fandom_wiki(url):
	try:
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
		}
		r = requests.get(url, headers=headers, timeout=30)
		html = r.text
		soup = BeautifulSoup(html, 'html.parser')
		item_list = str(soup.find('div', id='content'))
		ig_script_list = item_list.split('<script')
		ig_script = ' '+ig_script_list[1].split('</script>')[0].strip()
		ig_script = item_list.replace(ig_script, '>')
		item_title = re.sub(r'(<[^>]+>|\s)','', ig_script)
		return item_title
	except:
		return ''

def search_main(item, feature: list):
	if not feature == []:
		web_list = search_web(item)
		log(str(web_list), 'INFO')
		return_content = []
		reference_list = []
		if '百科' in feature:
			baike = search_baike(str(item))
			log(str(baike), "INFO")
			if baike is not None:
				reference_list = baike[0]
				content_list = baike[1]
				if reference_list is not None:
					for references in reference_list:
						reference_list.append(references)
				if content_list is not None:
					for contents in content_list:
						return_content.append(contents)
		if 'GitHub' in feature:
			githubresp = search_github(item)
			if not githubresp == "":
				try:
					ans = githubresp[1]
					return_content.append(ans[0:int(get_config().get("web").get('web_max_length'))])
					reference_list.append("https://github.com/"+githubresp[0])
				except:
					pass
		for items in web_list:
			log(f'Processing on {items}', 'EVENT')
			if "zhihu.com/question/" in items[1] and '知乎回复' in feature:
				return_content.append(str(search_zhihu_que(ext_zhihu(items[1])))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "baike.sogou.com" in items[1] and '百科' in feature:
				return_content.append(str(search_baike(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "mp.weixin.qq.com" in items[1] and '微信公众号' in feature:
				return_content.append(str(search_wx(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "zhuanlan.zhihu.com" in items[1] and '知乎专栏' in feature:
				return_content.append(str(search_zhihu_zhuanlan(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "163.com/dy/article/" in items[1] and '新闻' in feature:
				return_content.append(str(search_news_163(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "sohu.com/a/" in items[1] and '新闻' in feature:
				return_content.append(str(search_news_sohu(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "bilibili.com/read/" in items[1] and 'B站专栏' in feature:
				return_content.append(str(search_bilibili(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "blog.csdn.net" in items[1] and 'CSDN' in feature:
				return_content.append(str(search_csdn(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "zhidao.baidu.com" in items[1] and '百度知道' in feature:
				return_content.append(str(search_baidu_zhidao(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if "fandom.com" in items[1] and "/wiki/" in items[1] and 'fandom' in feature:
				return_content.append(str(search_fandom_wiki(items[1]))[0:int(get_config().get("web").get('web_max_length'))])
				reference_list.append(items[1])
			if 'All(Preview)' in feature:
				if not 'zhihu.com/question/' or not 'baike.sogou.com' or not 'mp.weixin.qq.com' or not 'zhuanlan.zhihu.com' or not '163.com/dy/article/' or not 'sohu.com/a/' or not 'bilibili.com/read/' or not 'blog.csdn.net' in items[1]:
					if not test_if_url_ignore(items[1]):
						ans = search_plain(items[1])
						if ans is not None:
							return_content.append(ans)
							reference_list.append(items[1][0:int(get_config().get("web").get('web_max_length'))])
			
		return [reference_list,return_content]

def match_url(string:str):
	reg = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	return re.findall(reg, string)


def if_trigger_web(word):
	triggers = get_config()['web']['trigger_words']
	for trigger in triggers:
		if trigger in word:
			return True
	else:
		return False

def run(prompt: str):
	if if_trigger_web(prompt):
		feature = get_config()['web']['feature']
		references = []
		try_match_url = match_url(prompt)
		web_info = ''
		if not try_match_url == []:
			for urls in try_match_url:
				log(f"Finding url in prompt, url: {urls}", "EVENT")
				plain_text = search_plain(urls)
				log(f"URL content: {repr(plain_text)}", "INFO")
				web_info += f"已知{urls}上的文字有：{repr(plain_text)}"
				references += [urls]
		else:
			log(f'Begin searching job. Feature: {feature}', "EVENT")
			search_resp = search_main(str(prompt), feature)
			web_info = search_resp[1] # type:ignore
			references += search_resp[0] # type:ignore
		if len(str(web_info)) > 2000:
			web_info = web_info[0:2000]
		log(f'Search finished. Web search response: {repr(web_info)}', "INFO")
		preview_reference = generate_reference(references)
		return {"add": f"我在网络上查询到了一些网络上的参考信息“{web_info}”", "prefix": "", "suffix": f"\n{preview_reference}"}
