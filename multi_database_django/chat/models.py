from django.db import models


class Message(models.Model):
    body = models.CharField(max_length=255)
    created_data = models.DateField(auto_created=True, auto_now_add=True)

