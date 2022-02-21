from django.urls import path, include
from django.contrib.auth.views import LogoutView, TemplateView
#from .views import LoginView

urlpatterns = [
#    path('', IndexView.as_view()),
    #path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('login/login_error/', TemplateView.as_view(template_name='accounts/error.html'), name='login_error'),
]
