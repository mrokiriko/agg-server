from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.Serializer):
	id = serializers.IntegerField(required = False)
	author_id = serializers.IntegerField()
	title = serializers.CharField(required = False)
	text = serializers.CharField()
	phonograms = serializers.CharField(required = False)
	thread_id = serializers.IntegerField(required = False)
	hash = serializers.CharField(max_length=256, required = False)

	def create(self, validated_data):
		return Article.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.id = validated_data.get('id', instance.id)
		#instance.author_id = validated_data.get('author_id', instance.author_id)
		instance.title = validated_data.get('title', instance.title)
		instance.text = validated_data.get('text', instance.text)
		instance.phonograms = validated_data.get('phonograms', instance.phonograms)
		instance.thread_id = validated_data.get('thread_id', instance.thread_id)
		#instance.date = validated_data.get('date ', instance.date)
		instance.hash = validated_data.get('phonograms_hash', instance.hash)

		instance.save()
		return instance
