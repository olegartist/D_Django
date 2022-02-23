from django.urls import path, include
from .views import CreateView, ListView, ConfirmView #, DetailView#, editor IndexView,

urlpatterns = [
    #path('', CreateView.as_view() ),
    path('create/', CreateView.as_view() ),
    path('list/', ListView.as_view()),
    path('list/confirm/<int:post>/', ConfirmView.as_view()),

]