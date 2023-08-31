from django.urls import path

from users.views import UserCreateApiView

urlpatterns = [

    path('', UserCreateApiView.as_view())
]