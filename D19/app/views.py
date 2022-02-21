from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import Group
from .models import *
from project.any import user_type

#from project.settings import TINYMCE_DEFAULT_CONFIG
#from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

import logging
logger = logging.getLogger(__name__)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'post/index.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'Зашел username {request.user.username} mail {request.user.email}')
        cat = int(self.kwargs.get('cat'))
        context = self.get_context_data()
        context['cats'] = Categorys.objects.order_by('sort')
        context['type_user'] = user_type(request.user)
        context['user_cat'] = cat

        if Categorys.objects.filter(pk=int(cat)).exists():
            #Переданый код есть в базе
            context['posts'] = Posts.objects.filter(cats_id=int(cat)).order_by('-created')
        else:
            context['posts'] = Posts.objects.all().order_by('-created')

        return self.render_to_response(context)


class CreateView(LoginRequiredMixin, TemplateView):
    class Null_cat():
        id = 0
        name = 'Выберите категорию'

    template_name = 'post/create.html'
    error = ''

    def get(self, request, *args, **kwargs):
        user_cat = str(self.kwargs.get('cat'))
        context = self.get_context_data()
        #context['current_time'] = timezone.now()
        if Categorys.objects.filter(pk=int(user_cat)).exists():
            context['user_cat'] = Categorys.objects.filter(pk=int(user_cat))[0]
            context['is_cat'] = True
        else:
            context['user_cat'] = self.Null_cat()
            context['is_cat'] = False
        context['title'] = ''
        context['content'] = ''
        context['cats'] = Categorys.objects.order_by('sort')
        context['error'] = ''

        return self.render_to_response(context)

    def set_cont(self, request):
        context = self.get_context_data()

        if Categorys.objects.filter(pk=int(request.POST['cats'])).exists():
            context['user_cat'] = Categorys.objects.filter(pk=int(request.POST['cats']))[0]
            context['is_cat'] = True
        else:
            context['user_cat'] = self.Null_cat()
            context['is_cat'] = False
        #print(context['is_cat'], context['user_cat'].name)
        context['title'] = request.POST['title']
        context['content'] = request.POST['content']
        context['cats'] = Categorys.objects.order_by('sort')
        context['error'] = self.error
        return context

    def check_error(self, request):
        self.error = ''
        s = ''
        if int(request.POST['cats']) == 0:
            self.error += 'выберите категорию'
            s = ', '
        if request.POST['title'] == '':
            self.error += s + 'укажите заголовок'
            s = ', '
        if request.POST['content'] == '':
            self.error += s + 'укажите текст'
        if self.error == '':
            res = False
        else:
            res = True
        return res

    def post(self, request, *args, **kwargs):
        if self.check_error(request):
            context = self.set_cont(request)
            #return redirect('create/0' + request.POST['cats'])
            return self.render_to_response(context)

        posts = Posts(
            user=request.user,
            cats=Categorys.objects.get(id=int(request.POST['cats'])),
            title=request.POST['title'],
            content=request.POST['content'],
        )
        posts.save()
        return redirect('/posts/0')

class DetailView(LoginRequiredMixin, TemplateView):
    template_name = 'post/post.html'

    def get(self, request, *args, **kwargs):
        user_cat = int(self.kwargs.get('cat'))
        post_id = int(self.kwargs.get('post'))
        post = Posts.objects.filter(pk=int(post_id))[0]
        context = self.get_context_data()
        context['post'] = post
        context['user_cat'] = user_cat
        #context['user_cat'] = Categorys.objects.filter(pk=int(user_cat))[0]
        context['cats'] = Categorys.objects.order_by('sort')
        # context['title'] = request.POST['title']
        # context['content'] = request.POST['content']
        context['is_edit'] = False
        context['clicks'] = Clicks.objects.filter(post=int(post_id)).order_by('-created')

        if request.user.pk == post.user.pk:
            context['is_edit'] = True

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_cat = int(request.POST['cats'])
        post_id = int(self.kwargs.get('post'))
        post = Posts.objects.get(id=post_id)
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.cats = Categorys.objects.get(id=user_cat)
        post.save()
        return redirect('/posts/'+str(user_cat))
