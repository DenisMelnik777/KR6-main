from django import forms

from blog.models import Article
from mailing.forms import StyleFormMixin


class ArticleForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания и изменения статей блога
    """
    class Meta:
        model = Article
        exclude = ('publication', 'views_count',)
