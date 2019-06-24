from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length = 80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

