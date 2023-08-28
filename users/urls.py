from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, verification_user, password_recovery, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # Авторизация пользователя
    path('logout/', LogoutView.as_view(), name='logout'),  # Выход пользователя
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация пользователя
    path('success_register/<str:register_uuid>/', verification_user, name='success_register'),  # Верификация пользователя
    path('password_recovery', password_recovery, name='password_recovery'),  # Восстановление доступа с помощью сгенерированного пароля и электронной почты
    path('profile/', UserUpdateView.as_view(), name='profile'),  # Изменение данных о пользователе
]
