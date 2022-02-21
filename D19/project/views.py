#from datetime import datetime, date, timedelta
#from datetime import datetime, timedelta

#from django.shortcuts import render, reverse, redirect

from django.contrib.auth.models import User

# from django.contrib.auth.models import Group
# from django.contrib.auth.decorators import login_required
# from .tasks import hello, printer

from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

#from django.utils import timezone
from django.shortcuts import redirect
from allauth.account.views import LogoutView
from django.contrib.auth import logout

from .any import user_type

import logging
logger = logging.getLogger(__name__)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'Зашел username {request.user.username} mail {request.user.email}')

        context = self.get_context_data()
        #context['current_time'] = timezone.now()
        context['type_user'] = user_type(request.user)
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
