from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации пользователя
    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
    """
    Форма для редактирования данных о пользователе
    """

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        """
        Скрывает изменение пароля
        """
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
