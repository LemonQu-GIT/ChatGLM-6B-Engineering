		payload = {
				"input": prompt,
				"history": history,
				"html_entities": False
		}
		url = 'http://127.0.0.1:8000/stream'
		response = requests.post(url, stream=True, json = payload)
		resp = ""
		for chunk in response.iter_content(chunk_size=1024):
			await asyncio.sleep(0.1)
			resp = chunk.decode('utf-8')
			yield resp
		chatmsg = resp.removeprefix("data: ")
		history.append([prompt, chatmsg])
		if len(history) > 10:
			history.pop(0)
		log(f"Chat history: {repr(history)}. Response: {repr(chatmsg)}")