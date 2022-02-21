from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, PostSearchView, CatSubView
from django.views.decorators.cache import cache_page

app_name = 'news'
urlpatterns = [
    path('', cache_page(60*1)(PostList.as_view()) ),
    path('add/', PostCreateView.as_view(), name='post_add'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail' ),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('subscribe/', cache_page(60*5)(CatSubView.as_view()) ),
]
