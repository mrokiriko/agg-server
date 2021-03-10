from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from .permissions import AllowReadAndAdd

from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer

import hashlib


class ArticleView(APIView):

	permission_classes = [IsAuthenticated | AllowReadAndAdd]
	
	def get(self, request, pk=None):
		if not pk:
			'''
			articles = Article.objects.order_by("-date")[:1000]
			serializer = ArticleSerializer(articles, many = True)
			return Response({"articles": serializer.data})
			'''
			return Response({"articles": Article.objects.count()})
		else:
			article = get_object_or_404(Article.objects.all(), pk=pk)
			serializer = ArticleSerializer(article, many = False)
			return Response({"article": serializer.data})
	
	def post(self, request, pk=None):
		#Here would be parser (possibly)
		title_len = 8 #If title is empty: how many words should be got from text to title
		min_text_len = 64 #Minimal amount symbols in text
		default_user = 3
		status_key = "success"
		message_key = "msg"

		articles = request.data.get('articles')
		responses = []
		main_response = []

		if type(articles) is list:

			for article in articles:

				if type(article) is dict:
					if request.user.pk is not None:
						article.update({'author_id': request.user.pk}) #It's ok with IsAuthenticatedOrReadOnly
					else:
						article.update({'author_id': default_user})
					if pk is not None:
						article.update({'id': pk})

				else:
					responses.append((False, "Data type is not dict"))
					continue

				serializer = ArticleSerializer(data = article)

				if serializer.is_valid(raise_exception = True):

					article.update({'text': Article.normilize_input(article['text'], onlylinks=True, getlist=False)})

					#Len validation and empty title fill
					if len(article['text']) < min_text_len:
						responses.append((False, "Insufficient text length"))
						continue

					elif not article.get('title', None):
						article.update({'title': ' '.join(article['text'].split()[:title_len])}) #get title from text

					#Uniqueness check:

					article.update({'ph_hash': hashlib.sha256(article['text'].encode()).hexdigest()}) #get hash
					identical_articles = Article.objects.filter(ph_hash = article['ph_hash'])
					#identical_images = <?>.objects.filter(<?>)

					if identical_articles.exists():

						if identical_articles[0].thread:
							responses.append((True, identical_articles[0].thread.id))

						else:
							responses.append((False, "Thread not found")) #return group only

					else:
						serializer = ArticleSerializer(data = article)

						if serializer.is_valid(): #raise_exception = False

							article_received = serializer.save()

							thread_received = article_received.find_thread()

							# if (article_received.image != ''):
							# 	image_received  = article_received.download_image()

							if not thread_received:
								Article.objects.get(id = article_received.id).delete() #!!!
								responses.append((False, "Thread not found"))

							else:
								responses.append((True, thread_received.id)) #Return only group

						else:
							responses.append((False, "Text after normalization is not valid"))
				else:
					responses.append((False, "Data is not valid")) 

		else:
			responses.append((False, "Data type is not list"))

		for response_status, response_message in responses:
			main_response.append({status_key : response_status, message_key : response_message})

		return Response(main_response)

	def put(self, request, pk=None):
		if not pk:
			return Response({"success": False, "msg": "primary key is not found"})
		else:
			article = get_object_or_404(Article.objects.all(), pk=pk) #Maybe raise not all objects?
			data = request.data.get('article')
			serializer = ArticleSerializer(instance=article, data=data, partial=True)
			if serializer.is_valid(raise_exception=True):
				article_received = serializer.save()
				return Response({"success": True, "data": article_received.id}) #What to return?
			else:
				return Response({"success": False, "msg": "data is not valid"})

	def delete(self, request, pk=None):
		if not pk:
			return Response({"success": False, "msg": "primary key is not found"})
		else:
			article = get_object_or_404(Article.objects.all(), pk=pk)
			article.delete()
			return Response({"success": True, "data": pk}, status=204) #Return something?
