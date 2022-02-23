from django.contrib.auth.models import User

from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

#from django.utils import timezone
from django.shortcuts import redirect
from allauth.account.views import LogoutView
from django.contrib.auth import logout

from .any import user_type
from app.models import Categorys, Posts, Clicks

from django.core.mail import EmailMultiAlternatives # send_mail
from .settings import ALLOWED_HOSTS
from django.template.loader import render_to_string
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'Зашел username {request.user.username} mail {request.user.email}')
        user_id = request.user.id
        context = self.get_context_data()
        #context['current_time'] = timezone.now()
        context['type_user'] = user_type(request.user)
        context['col_posts'] = Posts.objects.filter(user=request.user).count()
        context['col_clicks'] = Clicks.objects.filter(show=False, post__user_id=user_id).count()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return redirect('/posts/0')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

class BaseLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logger.info(f'Вышел username {request.user.username} mail {request.user.email}')
        logout(request)
        return redirect('/')

class NewsView(LoginRequiredMixin, TemplateView):
    template_name = 'news.html'

    def get(self, request, *args, **kwargs):
        type_user = user_type(request.user)
        if not (type_user == 'Спициалист' or type_user == 'Администратор'):
            return redirect('/')

        logger.info(f'Зашел в рассылку username {request.user.username}')
        context = self.get_context_data()
        context['cats'] = Categorys.objects.all().order_by('sort')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        for user in User.objects.filter(is_staff=False, is_active=True):
            if user.email:
                user_cat = request.POST['cats']
                text = request.POST['text']
                send_mail(user, user_cat, text)

        return redirect('/')

def send_mail(user, cat, text):
    if user.email:
        html_content = render_to_string(
            'mail_news.html', {
                'username': user.username,
                'cat': cat,
                'text': text,
                'datetime': timezone.now().strftime("%d-%m-%Y %H:%M"),
                'link': f'http://{ALLOWED_HOSTS[0]}:8000/',
            }
        )

        msg = EmailMultiAlternatives(
            subject='Новости Доска объявлений MMORPG',
            from_email='Skill.testing@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        try:
            msg.send()  # отсылаем
            logger.info(f'Отправлена новостная рассылка на {user.email}')
        except Exception as e:
            # print('Not sen email')
            logger.error(f'Ошибка отправки новостной рассылки на {user.email}')

    return ''
