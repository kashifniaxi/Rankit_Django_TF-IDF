from django.db import models

# Create your models here.


class Page(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    def __str__(self):
        return self.title
