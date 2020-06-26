from django.conf.urls import url
from django.urls import path,re_path
from feed.views import CategoryListView, NewsListView, NewsPostView

urlpatterns = [
    path(r'categories',CategoryListView.as_view(),name='CategoryListView'),
    path(r'list-news',NewsListView.as_view(),name='NewsListView'),
    path(r'fetch-news',NewsPostView.as_view(),name='NewsPostView'),
]