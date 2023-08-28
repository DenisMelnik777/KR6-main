import datetime

import schedule
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailing.models import Mailing


def sendmail(massage, user):
    """
    Отправляет письмо клиенту
    """
    send_mail(
        subject=massage.mail_subject,
        message=massage.text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def interval_check(mailing):
    """
    Проверяет периодичность оправки писем
    """
    next_try = None
    if mailing.interval == 'day':
        next_try = mailing.datetime + datetime.timedelta(days=1)
    elif mailing.interval == 'week':
        next_try = mailing.datetime + datetime.timedelta(days=7)
    elif mailing.interval == 'month':
        next_try = mailing.datetime + datetime.timedelta(days=30)
    return next_try


def start_check(mailing):
    """
    Проверяет дату начала рассылки для ее активации
    """
    if mailing.start == datetime.date.today():
        for user in mailing.users_group.all():
            sendmail(mailing.massage, user)
            mailing.status_mail = 'start'
            mailing.save()


def finish_check(mailing):
    """
    Проверяет дату окончания рассылки для ее отключения
    """
    for user in mailing.users_group.all():
        sendmail(mailing.massage, user)
        mailing.datetime = datetime.date.today()
    if mailing.stop == datetime.date.today():
        mailing.status_mail = 'finished'
    mailing.save()


def mail_func():
    """
    Проверяет все рассылки на сроки этой рассылки и отправляет сообщения
    """
    for mailing in Mailing.objects.all():
        try:
            if datetime.date.today() == interval_check(mailing):
                if mailing.status_mail == 'create':
                    start_check(mailing)
                elif mailing.status_mail == 'start':
                    finish_check(mailing)
            mailing.attempt = True
        except:
            mailing.feedback = 'Рассылка не удалась'
            mailing.attempt = False


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Запуск бесконечного цикла, для проверки рассылок и отправки сообщений
        """
        schedule.every().day.at("10:00").do(mail_func)

        while True:
            schedule.run_pending()
