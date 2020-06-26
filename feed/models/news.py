from django.db import models
from feed.models import Category

class News(models.Model):
    author = models.CharField(null=True, blank=True,max_length=5000)
    title = models.CharField(null=True, blank=True,max_length=5000)
    description = models.CharField(null=True, blank=True,max_length=5000)
    url_image = models.CharField(null=True, blank=True,max_length=1000)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category,related_name='news_category',on_delete=models.CASCADE)

    def __str__(self):
        return self.title
