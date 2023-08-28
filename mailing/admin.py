from django.contrib import admin

from mailing.models import Customer, Mailing, Massage


@admin.register(Customer)
class Castomeradmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'email',)


@admin.register(Mailing)
class Mailingadmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start', 'stop', 'interval', 'datetime')


@admin.register(Massage)
class Massageadmin(admin.ModelAdmin):
    list_display = ('id', 'mail_subject')
