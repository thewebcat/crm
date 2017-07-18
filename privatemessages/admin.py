# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
	Thread,
	Message,
)

# Register your models here.
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
	pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('text', 'sender', 'thread', 'datetime')