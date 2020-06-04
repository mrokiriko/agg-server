import requests
import time
import os

# Пока только jpg, надо будет расширять
'''
url - ссылка на изображение
path - диретория для сохранения
exp - расширение файла, по умолчанию '.jpg'
'''
def download_image(url, path, exp = '.jpg'):
	file = None
	try:
		image=requests.get(url)
		if (path[-1] != '/'):
			path = path + '/'
		filename = path + str(hash(url)) + '_' + str(round(time.time() * 1000)) + exp

		download_quittance = dict(filename = filename, extension = exp, f_hash = str(hash(image.content)))

		file = open(filename,'wb')
		file.write(image.content)
		file.close()

	except:
		if file:
			if not file.closed:
				file.close()
		return None
		
	else:	
		return download_quittance

#download_image("https://sun1-91.userapi.com/KiW_0EteNZeQKjNUu0itbCYDh1OKBdI8VulRxg/cQlmMndGyAo.jpg", '.')