from django.urls import path
from . import views
from los.apps import LosConfig

app_name = LosConfig.name

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/attend/', views.event_attend, name='event_attend'),
    path('event/<int:user_id>/visit/', views.profile_attend, name='profile_attend'),
    path('articles', views.articles_list, name='articles_list'),
    path('user_events', views.all_user_events, name='all_user_events')
]
