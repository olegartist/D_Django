from django.urls import path, include
from .views import IndexView, CreateView, DetailView#, editor

urlpatterns = [
    path('', IndexView.as_view() ),
    path('<int:cat>', IndexView.as_view() ),
    path('create/<int:cat>', CreateView.as_view() ),
    path('<int:cat>/post/<int:post>', DetailView.as_view()),
    path('<int:cat>/post/<int:post>/clicks/', include('clicks.urls')),
    path('<int:cat>/clicks/', include('clicks.urls')),
]
