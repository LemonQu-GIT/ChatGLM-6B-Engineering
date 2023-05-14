from selenium import webdriver
import time, re

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

def search_not(url):
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    try:
        driver.get(url)
    except Exception:
        driver.execute_script('window.stop()')
    for i in range(0, 20000, 350):
        time.sleep(0.1)
        driver.execute_script('window.scrollTo(0, %s)' % i)
    html = driver.execute_script("return document.documentElement.outerHTML")
    html = filter_tags(html).replace('\n','').replace('\r','').replace('\t','')
    return repr(html)