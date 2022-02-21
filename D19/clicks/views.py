from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from app.models import Categorys, Posts, Clicks
from django.contrib.auth.mixins import LoginRequiredMixin
#from project.any import user_type


class CreateView(LoginRequiredMixin, TemplateView):
    template_name = 'clicks/create.html'

    def get(self, request, *args, **kwargs):
        user_cat = str(self.kwargs.get('cat'))
        user_post = str(self.kwargs.get('post'))
        context = self.get_context_data()
        context['post'] = Posts.objects.get(pk=int(user_post))
        context['user_cat'] = user_cat
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_cat = str(self.kwargs.get('cat'))
        user_post = str(self.kwargs.get('post'))
        post = Posts.objects.get(pk=int(user_post))
        if not request.POST['clicks'] == '':
            clicks = Clicks(
                post=post,
                user=request.user,
                text=request.POST['clicks'],
                show=False,
            )
            clicks.save()
        return redirect(f'/posts/{user_cat}/post/{user_post}')
