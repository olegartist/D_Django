from .models import Category, Comment, Post
from modeltranslation.translator import register, TranslationOptions

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Comment)
class CommentlTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('text', 'title')