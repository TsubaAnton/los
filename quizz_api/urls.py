from rest_framework.routers import DefaultRouter
from django.urls import path

from quizz_api.apps import QuizzApiConfig
from quizz_api.views import TestViewSet,  AnswerQuestionView, TestCreateApiView


app_name = QuizzApiConfig.name
router = DefaultRouter()

router.register(r'tests', TestViewSet, basename='test')


urlpatterns = [
    path('test/create/', TestCreateApiView.as_view()),


    path('start/<int:test_pk>/answer/<int:question_pk>/', AnswerQuestionView.as_view())
              ] + router.urls
