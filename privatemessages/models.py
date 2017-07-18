# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

class Thread(models.Model):
    participants = models.ManyToManyField(User)
    last_message = models.DateTimeField(null=True, blank=True, db_index=True)

    def __unicode__(self):
    	return ", ".join(str(i) for i in self.participants.all())

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)

@receiver(post_save, sender=Message)
def update_last_message_datetime(sender, instance, created, **kwargs):
    """
    Update Thread's last_message field when
    a new message is sent.
    """
    if not created:
        return

    Thread.objects.filter(id=instance.thread.id).update(
        last_message=instance.datetime
    )
