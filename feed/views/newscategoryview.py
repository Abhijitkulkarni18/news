from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from feed.serializers import NewsSerializer, NewsPostSerializer, CategorySerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from feed.models import News as News_model, Category
from news import settings
import os
import NewsApiClient


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class=CategorySerializer



db_keys = {"author":"author","description":"description","title":"title",
            "urlToImage":"url_image","publishedAt":"published_at"}

def get_category_name(self, request):
    try:
        if request.GET.get('category_id'):
            return Category.objects.get(id=request.GET.get('category_id'))
        elif Category.objects.filter(name=request.GET.get('category_name')).exists():
            return Category.objects.get(name=request.GET.get('category_name'))
        else:
            return None
    except Exception as e:
        return None

class NewsPostView(GenericAPIView):
    serializer_class=NewsSerializer
    def post(self, request, format=None):
        try:
            category = get_category_name(self, request)
            if category:
                newsapi = NewsApiClient(api_key=os.environ.get('IS_HEROKU', None))
                top_headlines = newsapi.get_top_headlines(category=str(category.name))
                if top_headlines['status'] == 'ok':
                    for news_data in top_headlines['articles']:
                        input_data = {db_keys[key]:news_data[key] for key in news_data.keys() if key in db_keys.keys()}
                        input_data['category'] = category.id
                        serializer = NewsPostSerializer(data=input_data)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)
                            continue
                    return Response({'message':'News created'},
                                    status=status.HTTP_201_CREATED,
                                    content_type="application/json")
                else:
                    return Response(top_headlines,
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type="application/json")
            else:
                return Response({'message':'invalid category name or category id'},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")
        except Exception as e:
            return Response({'message':str(e)},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")


news_filter = { "id" : "id__in", "category_id":"category__in","category_name":"category__name__in",
                "title":"title__in","published_range":"published_at__date__range","items_per_page":
                "items_per_page","page_no":"page_no","sort_by":"sort_by","published_date":"published_at__date__in",
                }

class NewsListView(GenericAPIView):
    serializer_class=NewsSerializer
    items_per_page = openapi.Parameter('items_per_page', in_=openapi.IN_QUERY, description='items per page',type=openapi.TYPE_STRING)
    page_no = openapi.Parameter('page_no', in_=openapi.IN_QUERY, description='page no',type=openapi.TYPE_STRING)
    sort_by = openapi.Parameter('sort_by', in_=openapi.IN_QUERY, description='sort by',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[sort_by,items_per_page,page_no])
    def get(self, request, format=None):
        try:
            filters = {news_filter[key]:request.GET.get(key).split(',') for key in dict(request.GET).keys()}
            items = filters.pop('items_per_page')[0]
            page_num = filters.pop('page_no')[0]
            sort_by = filters.pop('sort_by')[0]
            data = News_model.objects.filter(**filters).order_by(sort_by)
            if data:
                paginator = Paginator(data,items)
                page = request.GET.get('page',page_num)
                News = paginator.get_page(page)
                serializer = NewsSerializer(News, many = True)
                page_num = int(page_num)
                if (page_num<=0)or(page_num>paginator.num_pages):
                    return Response({'message':'Empty Records','data':{}},
                                    status=status.HTTP_204_NO_CONTENT,
                                    content_type="application/json"
                                    )
                else:
                    return Response({'message':'Found','data':{"News_data":serializer.data},
                        "paginator":{"page_num":page,"items":items,"count":str(paginator.count)}},
                        status=status.HTTP_200_OK,content_type="application/json")
            else:
                return Response({'message':'not Found','data':[]},
                                status=status.HTTP_200_OK,
                                content_type="application/json")
        except Exception as e:
            return Response({'message':str(e)},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")