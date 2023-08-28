import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Article
from mailing.forms import MailingForm
from mailing.models import Mailing, Massage, Customer


def main(request):
    """
    Переходит на страницу "Главная"
    """
    mailing_count = len(Mailing.objects.all())
    mailing_active = len(Mailing.objects.filter(status_mail='start'))
    customer_count = len(Customer.objects.all())
    blog_list = Article.objects.order_by('?')[:3]
    context = {'mailing_count': mailing_count,
               'mailing_active': mailing_active,
               'customer_count': customer_count,
               'blog_list': blog_list}
    return render(request, 'mailing/main.html', context)


class MailingCreateView(CreateView):
    """
    Создание рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:main')

    def form_valid(self, form):

        """
        Проверка текущей даты, с датой начала и окончания рассылки.
        """
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            day_today = datetime.date.today()
            if self.object.start <= day_today < self.object.stop:
                self.object.status_mail = 'start'
                mail = self.object.massage
                users = self.object.users_group.all()
                for user in users:
                    send_mail(
                        subject=mail.mail_subject,
                        message=mail.text,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email]
                    )
                self.object.datatime = day_today
            elif day_today > self.object.stop:
                self.object.status_mail = 'finished'
            self.object.save()
            return super().form_valid(form)


class MailingListView(ListView):
    """
    Отображение всех рассылок
    """
    model = Mailing


class MailingDetailView(DetailView):
    """
    Просмотр информации о рассылке
    """
    model = Mailing


class MailingUpdateView(UpdateView):
    """
    Изменение параметров рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing')


class MailingDeleteView(DeleteView):
    """
    Удаление рассылки
    """
    model = Mailing
    success_url = reverse_lazy('mailing:mailing')
