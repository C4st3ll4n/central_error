from django.contrib import admin

from .models import ErrorLog, AppException, Agent

# Register your models here.
admin.site.register(ErrorLog)
admin.site.register(AppException)
admin.site.register(Agent)
