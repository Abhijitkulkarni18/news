from django.conf.urls import url
from django.urls import path,re_path
from feed.views import CategoryListView, NewsListView, NewsPostView

urlpatterns = [
    path(r'categorylist/',CategoryListView.as_view(),name='CategoryListView'),
    path(r'newslist/',NewsListView.as_view(),name='NewsListView'),
    path(r'newspost/',NewsPostView.as_view(),name='NewsPostView'),
]