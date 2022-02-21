#from datetime import datetime, date, timedelta
from datetime import datetime, timedelta

#from django.shortcuts import render, reverse, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import Post
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .tasks import hello, printer

from django.utils import timezone
from django.shortcuts import redirect

import pytz

import logging
logger = logging.getLogger(__name__)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = str(User.objects.all().count())
        context['post_count'] = str(Post.objects.all().count())
        # context['time_now'] = str(datetime.utcnow()).split(" ")[0]
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def get(self, request, *args, **kwargs):
        #hello.delay()
        #printer.delay(N=10)
        #printer.apply_async([10], countdown=5)
        #printer.apply_async([10], eta=datetime.now() + timedelta(seconds=5))

        logger.info(f'username {request.user.username}')

        context = self.get_context_data()
        if request.user.is_staff:
            context['type_user'] = 'Администратор'
        else:
            context['type_user'] = 'Пользователь'
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        click_timzone = request.POST.get('timezone', None)
        if click_timzone:
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('/')
        return redirect('/news/')

        # if request.user.is_staff:
        #     return redirect('/news/')
        # else:
        #     return redirect('/news/')

@login_required
def upgrade_premium(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('/')

@login_required
def upgrade_authors(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
