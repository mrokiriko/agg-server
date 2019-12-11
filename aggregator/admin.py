from django.contrib import admin
from .models import Article, Thread

#admin.site.register(Article)
#admin.site.register(Thread)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'author', 'thread', 'date')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'date')

