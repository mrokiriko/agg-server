from django.conf import settings
from django.db import models
from django.utils import timezone

import json
from .comparators.polyphone.polycompare import *
from .downloaders.download_image import download_image


class Thread(models.Model):
	title = models.TextField()
	phonograms = models.TextField()
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title


class Article(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.TextField(default='', blank=True)
	text = models.TextField()
	phonograms = models.TextField(blank=True)
	date = models.DateTimeField(default=timezone.now)
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE, blank=True, null=True)
	ph_hash = models.CharField(max_length=256, null=True)
	source = models.IntegerField(default=None, null=True)
	# image = models.TextField(blank=True)

	def __str__(self):
		return (self.title + ' \n' +  self.text)

	@staticmethod
	def create_phonograms(text, round_dict = 1024):
		return json.dumps(polyconverter(text = text, round_dict = round_dict))

	@staticmethod
	def normilize_input(text, onlylinks = False, getlist = True):
		return normalization(text = text, onlylinks = onlylinks, getlist = getlist)

	def find_thread(self, min_coef = 0.185085, round_dec = 3, round_dict = 1024):
		isThreadFound = False
		round_order = 10 ** (round_dec)
		threads = Thread.objects.all()

		if self.phonograms == '' or self.phonograms is None:
			self.phonograms = self.create_phonograms(str(self), round_dict = round_dict)

		if threads.exists():
			phonograms = json.loads(self.phonograms)
			if type(phonograms) is dict:
				for thread in threads:
					current_phonograms = json.loads(thread.phonograms)
					coef = polycompare(phonograms, current_phonograms)
					coef = round(coef * round_order) / round_order
					if (coef >= min_coef):
						self.thread = thread
						min_coef = coef
						if not isThreadFound:
							isThreadFound = True
			else:
				return None

		if not threads.exists() or not isThreadFound:
			self.thread = Thread.objects.create(title = self.title, phonograms = self.phonograms)

		self.save()

		return self.thread

	# def download_image(self, path = 'images'):
	# 	try:
	# 		if type(self.image) is not str:
	# 			raise Exception('link not found or unexpected type')
	#
	# 		image_info = download_image(self.image, path)
	#
	# 		if (type(image_info['filename']) is not str):
	# 			raise Exception('unexpected error while downloading')
	#
	# 		data = Data.objects.create(filename = image_info['filename'], extension = image_info['extension'], f_hash = image_info['f_hash'])
	# 		a_d = ArticleData.objects.create(article = self, data = data)
	#
	# 	except Exception as e:
	# 		print("image download error: {error}".format(error = e))
	# 		return False
	#
	# 	else:
	# 		return True


class Data(models.Model):
	filename = models.TextField()
	extension = models.CharField(max_length=256, null=True)
	f_hash = models.CharField(max_length=256, null=True)

	def __str__(self):
		return (self.filename)


class ArticleData(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
	data = models.ForeignKey(Data, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return (str(self.article) + ' ~ ' +  str(self.data))