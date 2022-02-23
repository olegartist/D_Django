from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from app.models import Categorys, Posts, Clicks
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives # send_mail
from project.settings import ALLOWED_HOSTS
from django.template.loader import render_to_string

#from project.any import user_type

import logging
logger = logging.getLogger(__name__)

class CreateView(LoginRequiredMixin, TemplateView):
    #Создание отклика
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
            try:
                clicks.save()
                logger.info(f'Пользователь {request.user.username} создал отклик {clicks.id} на объявление {post.id}')
                link = f'posts/{post.cats.id}/clicks/list/confirm/{post.id}'
                text = 'На Ваше объявление создан отклик, необходимо подтверждение'
                send_mail(post.user, post, clicks, link, text)

            except Exception as e:
                logger.error(f'Ошибка сохранения отклика Пользователем {request.user.username} на объявление {post.id}')

        return redirect(f'/posts/{user_cat}/post/{user_post}')

class ListView(LoginRequiredMixin, TemplateView):
    template_name = 'clicks/list.html'

    def get(self, request, *args, **kwargs):
        user_cat = str(self.kwargs.get('cat'))
        user_id = request.user.id
        post_id = list(set([i.post.id for i in Clicks.objects.filter(show=False, post__user_id=user_id)]))
        posts = Posts.objects.filter(id__in=post_id)
        context = self.get_context_data()
        context['user_cat'] = user_cat
        context['posts'] = posts
        context['cats'] = Categorys.objects.all()
        return self.render_to_response(context)

class ConfirmView(LoginRequiredMixin, TemplateView):
    #Подтверждение отклика
    template_name = 'clicks/confirm.html'

    def get(self, request, *args, **kwargs):
        user_cat = int(self.kwargs.get('cat'))
        post_id = int(self.kwargs.get('post'))
        post = Posts.objects.get(pk=int(post_id))
        context = self.get_context_data()
        context['post'] = post
        context['user_cat'] = user_cat
        #context['user_cat'] = Categorys.objects.filter(pk=int(user_cat))[0]
        context['cats'] = Categorys.objects.order_by('sort')
        # context['title'] = request.POST['title']
        # context['content'] = request.POST['content']
        context['clicks'] = Clicks.objects.filter(post=int(post_id), show=False).order_by('-created')


        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_cat = int(self.kwargs.get('cat'))
        post_id = int(self.kwargs.get('post'))
        clicks = Clicks.objects.filter(post=int(post_id), show=False).order_by('-created')
        for cclick in clicks:
            cod = request.POST["cl"+str(cclick.id)]
            post = Posts.objects.get(pk=post_id)

            if cod == '0': #удалить Отклик
                link = f'posts/{post.cats.id}/post/{post.id}'
                text = 'Ваш отклик отменён'
                send_mail(cclick.user, post, cclick, link, text)
                cclick.delete()
            else: #сохранить Отклик
                cclick.show = True
                cclick.save()
                #Отправить письмо тому кто наптсал отклик
                link = f'posts/{post.cats.id}/post/{post.id}'
                text = 'Ваш отклик подтверждён'
                send_mail(cclick.user, post, cclick, link, text)
        return redirect(f'/posts/{user_cat}/clicks/list')

def send_mail(user, post, clicks, link, text):
    if user.email:
        html_content = render_to_string(
            'clicks/mail_click.html', {
                'username': user.username,
                'post': post,
                'clicks': clicks,
                'text': text,
                #'joined': user.date_joined.strftime("%d-%m-%Y %H:%M"),
                'link': f'http://{ALLOWED_HOSTS[0]}:8000/{link}',
            }
        )

        msg = EmailMultiAlternatives(
            subject='Доска объявлений MMORPG',
            from_email='Skill.testing@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        try:
            msg.send()  # отсылаем
            logger.info(f'Отправлено письмо при регистрации {user.email}')
        except Exception as e:
            # print('Not sen email')
            logger.error(f'Ошибка отправки письма при регистрации {user.email}')

    return ''
