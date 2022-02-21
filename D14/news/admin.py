from django.contrib import admin
from .models import *

class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Author._meta.get_fields()]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_str')

class SubscribeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Subscribe._meta.get_fields()]

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]

def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)

nullfy_rating.short_description = 'Обнулить рэйтинг'

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'created', 'title', 'text', 'rating', 'cats_str')
    list_filter = ('author', 'post_type', 'rating')
    search_fields = ('text', 'text')
    actions = [nullfy_rating]


# Register your models here.

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)



#admin.site.unregister(Post)