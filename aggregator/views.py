from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Article
from .serializers import ArticleSerializer


class ArticleView(APIView):
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def get(self, request, pk = None):
		if not pk:
			articles = Article.objects.all()
			serializer = ArticleSerializer(articles, many = True)
			return Response({"articles": serializer.data})
		else:
			article = get_object_or_404(Article.objects.all(), pk=pk)
			serializer = ArticleSerializer(article, many=False)
			return Response({"article": serializer.data})
	
	def post(self, request, pk = None):
		#Here would be parser
		article = request.data.get('article')
		if type(article) is dict:
			article.update({'author_id': request.user.pk}) #It's ok with IsAuthenticatedOrReadOnly?
			if pk is not None:
				article.update({'id': pk})
		else:
			return Response({"success": "False", "msg": "data type is not dict"})

		serializer = ArticleSerializer(data = article)

		if serializer.is_valid(raise_exception = True):
			phonograms = Article.create_phonograms(article['title'] + ' \n' +  article['text'])
			identical_articles = Article.objects.filter(phonograms = phonograms)
			if identical_articles.exists():
				return Response({"success": "True", "data": identical_articles[0].thread.id}) #Return only group?
			else:
				article_received = serializer.save()
				thread_received = article_received.find_thread()
				return Response({"success": "True", "data": thread_received.id}) #Return only group?
		else:
			return Response({"success": "False", "msg": "data is not valid"})

	def put(self, request, pk = None):
		if not pk:
			return Response({"success": "False", "msg": "primary key is not found"})
		else:
			article = get_object_or_404(Article.objects.all(), pk = pk)
			data = request.data.get('article')
			serializer = ArticleSerializer(instance = article, data = data, partial = True)
			if serializer.is_valid(raise_exception = True):
				article_received = serializer.save()
				return Response({"success": "True", "data": article_received.id}) #What to return?
			else:
				return Response({"success": "False", "msg": "data is not valid"})

	def delete(self, request, pk = None):
		if not pk:
			return Response({"success": "False", "msg": "primary key is not found"})
		else:
			article = get_object_or_404(Article.objects.all(), pk=pk)
			article.delete()
			return Response({"success": "True", "data": pk}, status=204) #Return something?