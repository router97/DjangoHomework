from django.forms import ModelForm
from .models import Article, Comment

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['article']