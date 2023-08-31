from django.contrib import admin
from django.urls import path, include

from django.apps import AppConfig

from quizz.apps import QuizzConfig
from quizz.views import TestsListView, start_test, question_view, create_test, add_question, TestDetail

app_name = QuizzConfig.name

urlpatterns = [
    path('', TestsListView.as_view(), name='main_page'),
    path('statistic/<int:pk>/', TestDetail.as_view(), name='statistic'),

    path('create/', create_test, name='test_create'),

    path('create/add_question/<int:test_pk>/', add_question, name='add_question'),

    path('start/<int:test_pk>/', start_test, name='start_test'),
    path('start/<int:test_pk>/questions/<int:question_pk>/', question_view,  name='questions')

]
