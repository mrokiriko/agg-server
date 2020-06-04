from django.contrib import admin
from .models import Article, Thread, Data, ArticleData

#admin.site.register(Article)
#admin.site.register(Thread)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'author', 'thread', 'date')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'date')

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
	list_display = ('filename', 'extension', 'f_hash')

@admin.register(ArticleData)
class ArticleDataAdmin(admin.ModelAdmin):
	list_display = ('article', 'data')