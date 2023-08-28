from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import main, MailingCreateView, MailingListView, MailingDetailView, MailingUpdateView, \
    MailingDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', main, name='main'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('mailing/', cache_page(60)(MailingListView.as_view()), name='mailing'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='view'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
]
