from django.db import models

#
NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    """
    Модель клиента, кому будет отправляться сообщение
    """
    email = models.CharField(max_length=250, verbose_name='email')
    fio = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='коментарий', **NULLABLE)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Massage(models.Model):
    """
    Модель сообщения
    """
    mail_subject = models.CharField(max_length=300, verbose_name='тема письма')
    text = models.TextField(verbose_name='тело письма')

    def __str__(self):
        return self.mail_subject

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Mailing(models.Model):
    """
    Модель рассылки
    """
    INTERVAL = [('day', 'каждый день'), ('week', 'раз в неделю'), ('month', 'раз в месяц')]
    STATUS = [('create', 'создана'), ('start', 'запущена'), ('finished', 'завершена')]
    name = models.CharField(max_length=150, verbose_name='название рассылки')
    start = models.DateField(verbose_name='начало рассылки')
    stop = models.DateField(verbose_name='конец рассылки')
    interval = models.CharField(max_length=5, choices=INTERVAL, default='day')
    status_mail = models.CharField(max_length=8, choices=STATUS, default='create')
    users_group = models.ManyToManyField(Customer, verbose_name='группа пользователей для рассылки')
    massage = models.ForeignKey(Massage, on_delete=models.SET_NULL, null=True, verbose_name='письмо')
    datetime = models.DateField(auto_now_add=True, verbose_name='дата и время попытки')
    attempt = models.BooleanField(default=False, verbose_name='статус попытки')
    feedback = models.TextField(verbose_name='ответ сервера', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

