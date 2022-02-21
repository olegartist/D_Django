#from django.db.models import Q
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import date, timedelta
from news.models import Post, Subscribe

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives # send_mail
from NewsPaper.settings import ALLOWED_HOSTS

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    some_day_last_week = date.today() - timedelta(days=7)
    posts = Post.objects.filter(created__date__gte=some_day_last_week)
    #print(f'{post} {post[0]}')
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                #second="*/33"
                day_of_week="mon", hour="02", minute="00"
            ),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="01", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")