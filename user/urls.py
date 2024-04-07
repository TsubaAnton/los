from django.urls import path
from user.views import RegisterView
from user.apps import UserConfig
from django.contrib.auth.views import  LogoutView
from user.views import profile_view, CustomLoginView, RegisterView

app_name = UserConfig.name
urlpatterns = [

    # path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('profile/', ProfileUpdateView.as_view(), name='profile'),
    # path('', RegisterView.as_view(), name='register')
    path('', RegisterView.as_view(template_name='user/registration.html'), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('login/', CustomLoginView.as_view(), name='login')
    # path('reset/', ResetView.as_view(), name='reset'),
    # path('reset/done/', ResetDoneView.as_view(), name='reset_done'),
    # path('reset/<uidb64>/<token>/', ResetConfirmView.as_view(), name='password_confirm'),
    # path('reset/compete/', ResetCompleteView.as_view(), name='confirm')]
]
