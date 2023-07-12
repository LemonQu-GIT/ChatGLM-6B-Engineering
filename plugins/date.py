#coding:utf-8
import datetime
from zhdate import ZhDate
from plugins.utils import *

def trigger_words(prompt: str, method: str):
	triggers = get_config()['date'][method+"_trigger_words"]
	for trigger in triggers:
		if trigger in prompt:
			return True
	else:
		return False

def run(prompt: str):
	if trigger_words(prompt, "date"):
		log("Getting date", "EVENT")
		now = datetime.datetime.now()
		date_time = now.strftime("%Y年%m月%d日 %H点%M分%S秒")
		return {"add": f"已知现在的日期及时间为{date_time}，", "prefix": "", "suffix": ""}
	if trigger_words(prompt, "zh_date"):
		log("Getting date", "EVENT")
		today = datetime.datetime.today()
		zh_date = ZhDate.from_datetime(datetime.datetime(today.year, today.month, today.day)).chinese()
		return {"add": f"已知现在的农历日期为{zh_date}，", "prefix": "", "suffix": ""}