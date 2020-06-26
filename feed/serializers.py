from rest_framework import serializers
from feed.models import Category, News


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')

class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    class Meta:
        model = News
        fields = ('id','category','author','title','description','url_image','published_at')

class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id','category','author','title','description','url_image','published_at')