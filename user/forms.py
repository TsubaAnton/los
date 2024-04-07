from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from user.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'tg_link', 'course', 'direction']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['tg_link'].required = False
        self.fields['course'].required = False
        self.fields['direction'].required = False


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),  # Используйте FileInput вместо ClearableFileInput
        }


class LoginForm(AuthenticationForm):
    pass
