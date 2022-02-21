from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.forms.fields import DateField


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    users = models.ManyToManyField(User, through='Subscribe')

    def __str__(self):
        return self.name

    @property
    def user_str(self):
        return ','.join(cc.username for cc in self.users.all())

class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):
    article = 'a'
    news = 'n'

    POST_TYPE = [
        (article, "Статья"),
        (news, "Новость")
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=POST_TYPE, default=article)
    created = models.DateTimeField(auto_now_add=True)
    cats = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        size = 124 if len(self.text) > 124 else len(self.text)
        return self.text[:size] + '...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        #cache.delete(f'news') # затем удаляем его из кэша, чтобы сбросить его
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

    @property
    def post_type_str(self):
        # for i in self.POST_TYPE:
        #     if self.post_type == i[0]:
        #         post_type = i[1]
        return [i for i in self.POST_TYPE if i[0] == self.post_type][0][1]

    @property
    def cats_str(self):
        return ','.join(cc.name for cc in self.cats.all())

    # def __str__(self):
    #     cats = ','.join(cc.name for cc in self.cats.all())
    #     post_type = [i for i in self.POST_TYPE if i[0] == self.post_type][0][1]
    #     # for i in self.POST_TYPE:
    #     #     if self.post_type == i[0]:
    #     #         post_type = i[1]
    #     res = f'{self.author.user} {post_type} {str(DateField().to_python(self.created))} {cats[:20]} {self.head} {self.text[:22]} {self.rating}'
    #     return res

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Russian_mat(models.Model):
    word = models.CharField(max_length=64, unique=True, null=False)
    # def __str__(self):
    #     return f'{self.word}'
