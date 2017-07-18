# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q

class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Shop(models.Model):
    url = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    directors_name = models.CharField(max_length=255)
    directors_phone = models.CharField(max_length=255)
    directors_email = models.CharField(max_length=255)
    servises = models.ManyToManyField(Service)
    last_calculation = models.DateTimeField()

    def servises_list(self):
        return ', '.join([a.name for a in self.servises.all()])

    def __unicode__(self):
        return self.alias

class Storage(models.Model):
    name = models.CharField(max_length=255)
    last_coming = models.DateTimeField()
    own_shop = models.ForeignKey(Shop)
    price = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def count_logs(self):
        storage_in = 0
        for item in StorageLog.objects.filter(storage=self, shop=self.own_shop, log_type__log_type='in'):
            storage_in = storage_in + item.count
        storage_out = 0
        for item in StorageLog.objects.filter(storage=self, shop=self.own_shop, log_type__log_type='out'):
            storage_out = storage_out + item.count
        return storage_in - storage_out

class StorageLogType(models.Model):
    """docstring for StorageLog"""
    name = models.CharField(max_length=255)
    log_type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class StorageLog(models.Model):
    """docstring for StorageLog"""
    log_type = models.ForeignKey(StorageLogType)
    action = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop)
    storage = models.ForeignKey(Storage)
    date = models.DateTimeField()
    count = models.IntegerField()

    def __unicode__(self):
        return self.action

class CashType(models.Model):
    name = models.CharField(max_length=255)
    type_code = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Cash(models.Model):
    sum = models.IntegerField()
    last_coming = models.DateTimeField()
    own_shop = models.ForeignKey(Shop)
    cash_type = models.ForeignKey(CashType)
    creator_url = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return str(self.sum)

class Courier(models.Model):
    """docstring for Сourier"""
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Delivery(models.Model):
    """docstring for Delivery"""
    shop = models.ForeignKey(Shop, verbose_name='Магазин')
    date = models.DateTimeField()
    custom_product = models.CharField(max_length=255, blank=True)
    is_custom_product = models.BooleanField(default=0)
    custom_price = models.IntegerField(default=0, blank=True)
    is_custom_price = models.BooleanField(default=0)
    delivery_fromclient = models.IntegerField(default=0, blank=True, verbose_name='Стоимость с клиента')
    delivery_price = models.IntegerField(default=0, blank=True, verbose_name='Стоимость с партнера')
    delivery_date = models.DateField(verbose_name='Дата доставки')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    phone = models.CharField(max_length=255, verbose_name='Телфон')
    time = models.CharField(max_length=255, blank=True, verbose_name='Время')
    courier = models.ForeignKey(Courier, blank=True, null=True, verbose_name='Курьер')
    cash_in_transaction_id = models.IntegerField(default=0, blank=True)
    cash_out_transaction_id = models.IntegerField(default=0, blank=True)
    storage_in_transaction_id = models.IntegerField(default=0, blank=True)
    storage_out_transaction_id = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return self.address

    def tel_addr_time(self):
        string = []
        if self.phone != '':
            string.append(self.phone)
        if self.address != '':
            string.append(self.address)
        if self.time != '':
            string.append(self.time)
        return ", ".join(string)

    def total_product(self):
        if self.custom_product == '':
            product = []
            for item in self.deliveryproduct_set.all():
                product.append(item.product.name)
            return ", ".join(product)
        else:
            return self.custom_product

    def total_price(self):
        if self.is_custom_price == False:
            price = 0
            for item in self.deliveryproduct_set.all():
                price = price + item.product.price*item.count
            return price    
        else:
            return self.custom_price

    def client_price(self):
        return self.total_price() + self.delivery_fromclient

    def to_partner(self):
        return self.total_price() - self.delivery_price + self.delivery_fromclient

class DeliveryProduct(models.Model):
    """docstring for DeliveryProduct"""
    product = models.ForeignKey(Storage)
    delivery = models.ForeignKey(Delivery)
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.product.name

    def delivery_id(self):
        return str(delivery.pk)

class DeliveryStatus(models.Model):
    """docstring for DeliveryStatus"""
    status = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.status

class DeliveryStatusList(models.Model):
    """docstring for DeliveryList"""
    status = models.ForeignKey(DeliveryStatus)
    delivery = models.ForeignKey(Delivery)
    date = models.DateTimeField()

    def __unicode__(self):
        return " | ".join([str(self.date), self.status.status, unicode(self.delivery.tel_addr_time())])

class DeliveryLog(models.Model):
    """docstring for DeliveryStatus"""
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    shop = models.ForeignKey(Shop)
    delivery = models.ForeignKey(Delivery)
    user = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name    