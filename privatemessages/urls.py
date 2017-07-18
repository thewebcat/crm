# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from privatemessages import views

urlpatterns = [
	url(r'^send_message/$', views.send_message_view, name='send_message_view'),
	url(r'^send_message_api/(?P<thread_id>\d+)/$', views.send_message_api_view, name='send_message_api_view'),
	url(r'^chat/(?P<thread_id>\d+)/$', views.chat_view, name='chat_view'),
	url(r'^$', views.messages_view, name='messages_view'),
]