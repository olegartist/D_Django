from django.urls import path, include
from .views import CreateView#, DetailView#, editor IndexView,

urlpatterns = [
    #path('', CreateView.as_view() ),
    path('create/', CreateView.as_view() ),
]