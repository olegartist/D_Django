from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.template.loader import render_to_string

from allauth.account.forms import SignupForm
#from django.contrib.auth.models import Group

from django.core.mail import EmailMultiAlternatives # send_mail
from project.settings import ALLOWED_HOSTS

import logging
logger = logging.getLogger(__name__)

class BaseRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)

        if user.email:
            html_content = render_to_string(
                'account/letter_mail.html', {
                    'username': user.username,
                    'joined': user.date_joined.strftime("%d-%m-%Y %H:%M"),
                    'link': f'http://{ALLOWED_HOSTS[0]}:8000/',
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
                #print('Not sen email')
                logger.error(f'Ошибка отправки письма при регистрации {user.email}')

        return user
