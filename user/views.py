from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from user.forms import UserForm, RegisterForm, ProfileForm, ImageUploadForm, LoginForm, AuthenticationForm
from user.models import User


# Create your views here.
class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


# class RegisterView(CreateView):
#     model = User
#     form_class = RegisterForm
#
#     success_url = reverse_lazy('los:event_list')
#
#     def form_valid(self, form):
#         return super().form_valid(form)


def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid() and image_form.is_valid():
            profile_form.save()
            image_form.save()
            return redirect('user:profile')  # или куда вы хотите перенаправить пользователя после сохранения
    else:
        profile_form = ProfileForm(instance=request.user)
        image_form = ImageUploadForm(instance=request.user)
    return render(request, 'user/profile.html', {'profile_form': profile_form, 'image_form': image_form})


class RegisterView(CreateView):
    template_name = 'user/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user:login')


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('profile')


