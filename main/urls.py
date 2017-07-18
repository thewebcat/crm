# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from main import views

urlpatterns = [
	# client side


	# admin
	url(r'^$', views.index, name='index'),
	url(r'^get_storage_price/$', views.get_storage_price, name='get_storage_price'),
	url(r'^add_delivery_status/$', views.add_delivery_status, name='add_delivery_status'),
	url(r'^delivery/$', views.delivery, name='delivery'),
	url(r'^delivery/(?P<pk>[0-9]+)/$', views.delivery_show, name='delivery_show'),
	url(r'^delivery/(?P<pk>[0-9]+)/edit/$', views.delivery_edit, name='delivery_edit'),
	url(r'^delivery/(?P<pk>[0-9]+)/status/$', views.delivery_status, name='delivery_status'),
	url(r'^storage/$', views.storage, name='storage'),
	url(r'^cash/$', views.cash, name='cash'),
	url(r'^create_goods/$', views.create_goods, name='create_goods'),
	url(r'^add_goods/(?P<goods_id>\d+)/$', views.add_goods, name='add_goods'),
	url(r'^remove_goods/(?P<goods_id>\d+)/$', views.remove_goods, name='remove_goods'),

	# asterisk cdr load
	#url(r'^main/sms/$', smssend, name='smssend'),
]
