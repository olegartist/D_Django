from celery import shared_task
import time

from news.models import Post, Subscribe
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives # send_mail
from NewsPaper.settings import ALLOWED_HOSTS
from datetime import date, timedelta, datetime

@shared_task
def hello():
    time.sleep(1)
    print("Hello, world!")
    print(f"Date: {datetime.now()}")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
def post_mail_week():

    some_day_last_week = date.today() - timedelta(days=7)
    posts = Post.objects.filter(created__date__gte=some_day_last_week)
    #print(f'Post {posts.count()} date {date.today()}')
    for post in posts:
        for cat in post.cats.all():
            for sub in Subscribe.objects.filter(category_id=cat.id):
                # получить всех авторов подписаных на категорию
                # print(sub.user.id, cat.id)

                if sub.user.email:
                    # если есть майл

                    html_content = render_to_string(
                        'post/pochta_week.html', {
                            'user': sub.user,
                            'title': post.title,
                            'cat': cat,
                            'text': post.text[:50],
                            'link': f'http://{ALLOWED_HOSTS[0]}:8000/news/{post.id}',
                        }
                    )

                    # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
                    msg = EmailMultiAlternatives(
                        subject=f'{cat} создана {post.created.strftime("%d-%m-%Y %H:%M")}',
                        # body=f'{post.head} \n {post.text}',  # это то же, что и message
                        from_email='Skill.testing@yandex.ru',
                        to=[sub.user.email],  # это то же, что и recipients_list
                    )
                    msg.attach_alternative(html_content, "text/html")  # добавляем html
                    try:
                        msg.send()  # отсылаем
                    except Exception as e:
                        print('Not sen email')

@shared_task
def mail_new_post(id):
    post = Post.objects.get(pk=id)
    for cat in post.cats.all():
        for sub in Subscribe.objects.filter(category_id=cat.id):
            # получить всех авторов подписаных на категорию
            # print(sub.user.id, cat.id)

            if sub.user.email:
                # если есть майл

                # отправляем письмо
                # send_mail(
                #     subject=f'{post.author.user.username} {post.created.strftime("%d-%m-%Y %H:%M")}',  # имя клиента и дата записи будут в теме для удобства
                #     message=f'{post.head} \n {post.text}',  # сообщение с кратким описанием проблемы
                #     from_email='Skill.testing@yandex.ru', # здесь указываете почту, с которой будете отправлять (об этом попозже)
                #     recipient_list=[post.author.user.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
                # )

                html_content = render_to_string(
                    'post/pochta.html', {
                        'user': sub.user,
                        'title': post.title,
                        'cat': cat,
                        'text': post.text[:50],
                        'link': f'http://{ALLOWED_HOSTS[0]}:8000/news/{post.id}',
                    }
                )

                # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
                msg = EmailMultiAlternatives(
                    subject=f'{cat} создана {post.created.strftime("%d-%m-%Y %H:%M")}',
                    # body=f'{post.head} \n {post.text}',  # это то же, что и message
                    from_email='Skill.testing@yandex.ru',
                    to=[sub.user.email],  # это то же, что и recipients_list
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                try:
                    msg.send()  # отсылаем
                except Exception as e:
                    print('Not sen email')

