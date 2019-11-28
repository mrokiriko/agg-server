import re

class Polyphone:
	def __init__(self):
		#self.STEP_1 = [("[aA]", "А"), ("[eE]", "Е"), ("[oO]", "О"), ("[cC]", "С"), ("[xX]", "Х"), ("[B]", "В"), ("[M]", "М"), ("[H]", "Н")]
		self.STEP_2 = [("[^а-яА-ЯёЁa-zA-Z]", "")]
		self.STEP_3 = [("[ЬЪ]", "")]
		self.STEP_4 = [(r"([А-ЯЁ])\1", r"\1_")]
		self.STEP_5 = [("[AЕЁИОЫЭЯ](?!_)", "А"), ("[Б](?!_)", "П"), ("[В](?!_)", "Ф"), ("[Г](?!_)", "К"), ("[Д](?!_)", "Т"), ("[З](?!_)", "С"), ("[Щ](?!_)", "Ш"), ("[Ж](?!_)", "Ш"), ("[М](?!_)", "Н"), ("[Ю](?!_)", "У"), ("[_]", "")]
		self.STEP_6 = [("АКА", "АФА"), ("АН", "Н"), ("ЗЧ", "Ш"), ("ЛНЦ", "НЦ"), ("ЛФСТФ", "ЛСТФ"), ("НАТ", "Н"), ("НТЦ", "НЦ"), ("НТ", "Н"), ("НТА", "НА"), ("НТК", "НК"), ("НТС", "НС"), ("НТСК", "НСК"), ("НТШ", "НШ"), ("ОКО", "ОФО"), ("ПАЛ", "ПЛ"), ("РТЧ", "РЧ"), ("РТЦ", "РЦ"), ("СП", "СФ"), ("ТСЯ", "Ц"), ("СТЛ", "СЛ"), ("СТН", "СН"), ("СЧ", "Ш"), ("СШ", "Ш"), ("ТАТ", "Т"), ("ТСА", "Ц"), ("ТАФ", "ТФ"), ("ТС", "ТЦ"), ("ТЦ", "Ц"), ("ТЧ", "Ч"), ("ФАК", "ФК"), ("ФСТФ", "СТФ"), ("ШЧ", "Ш")]
		self.CONVERT = {'А': 2, 'П': 3, 'К': 5, 'Л': 7, 'М': 11, 'Н': 13, 'Р': 17, 'С': 19, 'Т': 23, 'У': 29, 'Ф': 31, 'Х': 37, 'Ц': 41, 'Ч': 43, 'Щ': 47, 'Э': 53, 'Я': 59}

	@staticmethod
	def replace_by_dictionary(string, dictionary):
	    for pattern, repl in dictionary:
	    	if re.search(pattern, string):
	    		string = re.sub(pattern, repl, string)
	    return string
	
	@staticmethod
	def count_by_dictionary(string, dictionary, amount = 0):
		for key in string:
			amount += dictionary.get(key, 0)
		return amount

	def convert(self, input, convert_to_value = False, is_only_letters = False, is_only_uppercase = False):
		if not is_only_letters:
			#input = self.replace_by_dictionary(input, self.STEP_1)
			input = self.replace_by_dictionary(input, self.STEP_2)
		if not is_only_uppercase:
			input = input.upper()
		for step in self.STEP_3, self.STEP_4, self.STEP_5, self.STEP_6:
			input = self.replace_by_dictionary(input, step)
		if convert_to_value:
			input = self.count_by_dictionary(input, self.CONVERT)
		return input
