from django.contrib import admin

from django.contrib import admin

from los.models import Event, Article


@admin.register(Event)
class AdminTest(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
