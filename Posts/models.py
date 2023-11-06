from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    name = models.CharField(
        max_length=16,
        unique=True
    )

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    title = models.CharField(
        max_length=255,
    )
    role = models.ForeignKey(
        to=Role,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    creator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    created_at = models.DateField(
        auto_now=True,
    )

    def __str__(self):
        return f'[{self.role}] {self.title}'

    def short_desc(self):
        long = False if len(f'{self.text}') < 20 else True
        return f'{self.text[:20]}{"..." if long else "" }'

    def get_absolute_url(self):
        return f'/'


class Replies(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    text = models.TextField()

    def get_absolute_url(self):
        return f'/'
