from django.forms import ModelForm
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    # user = None
    #
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user')
    #     super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ['author', 'cats', 'post_type', 'title', 'text']
        labels = {'author': ('Автор'), 'cats': 'Категория', 'title': 'Заголовок', 'text': 'Текст'}
        #exclude = ('author',)
        #help_texts = {'author': ('Автор статьи'), }
        #help_texts = {'author': ('Автор статьи'), }
        #initial = {'author': self.user.username }
