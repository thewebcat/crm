# -*- coding: utf-8 -*-
import datetime
import json
import time
import urllib

import redis
import tornadoredis
import tornado.gen
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient
import sockjs.tornado

from sockjs.tornado import proto

from django.conf import settings
from importlib import import_module

session_engine = import_module(settings.SESSION_ENGINE)

from django.db import connection
from django.db.utils import OperationalError
from django.contrib.auth.models import User

from privatemessages.models import Thread

c = tornadoredis.Client()
c.connect()
redis_client = redis.Redis()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello. :)')

class ChatConnection(sockjs.tornado.SockJSConnection):
    def __init__(self, *args, **kwargs):
        super(ChatConnection, self).__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()

    def on_open(self, info):
        print 'open'
        session_key = info.get_cookie(settings.SESSION_COOKIE_NAME).value
        self.django_session = session_engine.SessionStore(session_key)

    def show_new_message(self, result):
        self.send(str(result.body))

    def handle_request(self, response):
        pass

    @tornado.gen.engine
    def on_message(self, message):
        print "send_msg_to_tornado"
        print "send_msg_to_tornado "+message
        data = proto.json_decode(message.replace('\r', '\\r').replace('\n', '\\n'))

        if data['type'] == 'auth':
            self.thread_id = data['thread_id']
            try:
                self.user_id = self.django_session["_auth_user_id"]
                try:
                    self.sender_name = User.objects.get(id=self.user_id).username
                except OperationalError:
                    connection.close()
                    self.sender_name = User.objects.get(id=self.user_id).username
            except (KeyError, User.DoesNotExist):
                self.close()
                return
            if not Thread.objects.filter(
                id=self.thread_id,
                participants__id=self.user_id
            ).exists():
                self.close()
                return
            self.channel = "".join(['thread_', self.thread_id,'_messages'])
            self.channel2 = "".join(['thread_', self.thread_id,'_notice'])
            yield tornado.gen.Task(self.client.subscribe, [
                self.channel,
                self.channel2
            ])
            #self.client.subscribe(self.channel)
            #self.client.subscribe(self.channel2)
            self.client.listen(self.show_new_message)

        if data['type'] == 'message':
            if not data['message']:
                return
            if len(data['message']) > 10000:
                return
            redis_client.publish(self.channel, json.dumps({
                "name": "message",
                "timestamp": int(time.time()),
                "sender": self.sender_name,
                "text": data['message'],
            }))
            http_client = tornado.httpclient.AsyncHTTPClient()
            request = tornado.httpclient.HTTPRequest(
                "".join([
                            settings.SEND_MESSAGE_API_URL,
                            "/",
                            self.thread_id,
                            "/"
                        ]),
                method="POST",
                body=urllib.urlencode({
                    "message": data['message'].encode("utf-8"),
                    "api_key": settings.API_KEY,
                    "sender_id": self.user_id,
                })
            )
            http_client.fetch(request, self.handle_request)

        if data['type'] == 'typing':
            if int(data['typing']):
                c.publish(self.channel2, json.dumps({
                    "name":"typing",
                    "sender": self.sender_name,
                    "typing":1
                }))
            else:
                c.publish(self.channel2, json.dumps({
                    "name":"typing",
                    "sender": self.sender_name,
                    "typing":0
                }))
    
    def on_close(self):
        try:
            self.client.unsubscribe(self.channel)
        except AttributeError:
            pass
        def check():
            if self.client.connection.in_progress:
                tornado.ioloop.IOLoop.instance().add_timeout(
                    datetime.timedelta(0.00001),
                    check
                )
            else:
                self.client.disconnect()
                connection.close()
        tornado.ioloop.IOLoop.instance().add_timeout(
            datetime.timedelta(0.00001),
            check
        )
