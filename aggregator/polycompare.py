import json
import re
import collections
from . import polyphone

def links_cleaner(text):
	text = re.sub(r"«http:.+?»",'',text)

	return text

def normalization(text):
	text - links_cleaner(text)
	text = re.sub(r'[^а-яА-ЯёЁa-zA-Z ]', ' ', text)
	text = re.sub(r'\b[a-zа-яё0-9]{1,4}\b', ' ', text)
	text = re.sub(r'\b[а-яё0-9]{1,3}\b', ' ', text)
	text = re.sub(r'\b[АОИЕЭУЮЯ][а-яё0-9]{1,3}\b', ' ', text)
	text = re.sub('[ ]+', ' ', text)
	text = " ".join(text.split())

	return text	

def polyconverter(text, round_dict = 1024):
	words = normalization(text).split(' ')
	phonograms = []
	poly = polyphone.Polyphone()

	for word in words:
		phonogram = poly.convert(word)
		if (phonogram != ''):
			phonograms.append(phonogram)

	phonograms = dict(collections.Counter(phonograms).most_common(round_dict))

	return phonograms

def polycompare(dict1, dict2):
	intersection = set(dict1.keys()) & set(dict2.keys())
	intersection_count = 0

	for C in intersection:
		A = dict1.get(C, 0)
		B = dict2.get(C, 0)
		intersection_count += B if (A>B) else A
	common_count = sum(dict1.values()) + sum(dict2.values())

	if common_count:
		return 2 * intersection_count / common_count
	else:
		return 1
