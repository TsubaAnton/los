from django.contrib import admin

from quizz.models import Question, Test, TestResults


@admin.register(Test)
class AdminTest(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Question)
class AdminQuestion(admin.ModelAdmin):
    list_display = ['text']


@admin.register(TestResults)
class AdminResults(admin.ModelAdmin):
    list_display = ['test', 'is_passed']
