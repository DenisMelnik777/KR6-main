import uuid
import random

from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.checks import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    """
    Авторизация пользователя
    """
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    """
    Выход пользователя
    """
    pass


class RegisterView(CreateView):
    """
    Регистрация нового пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        После регистрации отправляет на электронную почту ссылку для верификации аккаунта
        """
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = False
            self.object.register_uuid = uuid.uuid4().hex
            self.object.save()
            current_site = get_current_site(self.request)
            send_mail(
                subject='Подтверждение аккаунта',
                message=f'Для подтверждения перейдите по ссылке http://{current_site}{reverse_lazy("users:success_register", kwargs={"register_uuid": self.object.register_uuid})}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
        return super().form_valid(form)


def verification_user(request, *args, **kwargs):
    """
    Верификации аккаунта после перехода по ссылке с электронной почты
    """
    user = User.objects.get(register_uuid=kwargs["register_uuid"])
    if user.register_uuid == kwargs['register_uuid']:
        user.is_active = True
        user.save()
        login(request, user)
    return redirect(reverse('mailing:main'))


def password_recovery(request):
    """
    Восстановление доступа с помощью сгенерированного пароля отправленного на электронную почту
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.all()
        for user in users:
            if user.email == email:
                new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
                send_mail(
                    subject='Восстановление пароля',
                    message=f'Ваш новый пароль: {new_password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
                user.set_password(new_password)
                user.save()
                return redirect(reverse('users:login'))
    return render(request, 'users/password_recovery.html')


class UserUpdateView(UpdateView):
    """
    Изменение параметров пользователя
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Получение авторизованного пользователя
        """
        return self.request.user
