from django_filters import FilterSet
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'created': ['date__gte'],
            'title': ['icontains'],
            'author': ['exact'],
        }
        labels = {'author': ('Автор'),}


        # fields = ('author', 'created', 'head', 'post_type', 'cats',
        #           'rating')
