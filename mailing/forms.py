from django import forms

from mailing.models import Mailing


class StyleFormMixin:
    """
    Стиль для отображения формы заполнения
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('status_mail', 'attempt', 'feedback',)
