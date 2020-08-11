from django.db import models

# Create your models here.
from django.conf import settings

LEVEL_CHOICES = [
    ('ERROR', 'error'),
    ('DEBUG', 'debug'),
    ('WARNING', 'warning')
]

ENVIRONMENT_CHOICES = [
    ('PRODUCTION', 'Produção'),
    ('HOMOLOGATION', 'Homologação'),
    ('DEVELOPMENT', 'Desenvolvimento')
]


class Agent(models.Model):
    address = models.CharField(max_length=200)


class AppException(models.Model):
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title


class ErrorLog(models.Model):
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES)
    environment = models.CharField(max_length=30, choices=ENVIRONMENT_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exception = models.ForeignKey(AppException, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
