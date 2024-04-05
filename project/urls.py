from django.urls import path
from . import views
from project.apps import ProjectConfig

app_name = ProjectConfig.name

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
]