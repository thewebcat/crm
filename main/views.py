# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django import forms

from datetime import datetime
import json
import logging

from main.models import (
    Shop,
    Storage,
    StorageLog,
    StorageLogType,
    Delivery,
    DeliveryProduct,
    Cash,
    CashType,
    DeliveryStatusList,
    DeliveryStatus,
    DeliveryLog,
)
from main.forms import DeliveryForm, DeliveryProductFormSet

now = datetime.now()
logger = logging.getLogger('user') # пользовательский логгер для бебага


def index(request):
    delivery = Delivery.objects.all().order_by('-date')

    context = {
        'delivery': delivery,
    }

    return render(request, 'dashboard.html', context)

def create_goods(request):
    if request.method == "POST":
        own_shop = Shop.objects.get(alias=request.POST['own_shop'])
        storage = Storage(
            name = request.POST['name'],
            price = request.POST['price'],
            own_shop = own_shop,
            last_coming = now.strftime('%Y-%m-%d %H:%M:%S')
        )
        storage.save()

        if request.POST['count']:
            storagelog = StorageLog(
                log_type = StorageLogType.objects.get(pk=3),
                action = "Создан новый товар: "+request.POST['name'].encode('utf-8')+" с начальным остатком: "+request.POST['count'].encode('utf-8')+" шт.",
                shop = own_shop,
                storage = storage,
                date = now.strftime('%Y-%m-%d %H:%M:%S'),
                count = int(request.POST['count'])
            )
            storagelog.save()

        return HttpResponseRedirect('/storage/')

    raise Http404

def add_goods(request, goods_id):
    if request.method == "POST":
        now = datetime.now()
        goods = Storage.objects.get(pk=goods_id)
        storagelog = StorageLog(
            log_type = StorageLogType.objects.get(pk=1),
            action = "Поступление товара: "+goods.name.encode('utf-8')+" в количестве: "+request.POST['count'].encode('utf-8')+" шт.",
            shop = goods.own_shop,
            storage = goods,
            date = now.strftime('%Y-%m-%d %H:%M:%S'),
            count = int(request.POST['count'])
        )
        storagelog.save()

        return HttpResponseRedirect('/storage/')

    raise Http404

def remove_goods(request, goods_id):
    if request.method == "POST":
        now = datetime.now()
        goods = Storage.objects.get(pk=goods_id)
        storagelog = StorageLog(
            log_type = StorageLogType.objects.get(pk=2),
            action="Списание товара: "+goods.name.encode('utf-8')+" в количестве: "+request.POST['count'].encode('utf-8')+" шт.",
            shop = goods.own_shop,
            storage = goods,
            date = now.strftime('%Y-%m-%d %H:%M:%S'),
            count = int(request.POST['count'])
        )
        storagelog.save()

        return HttpResponseRedirect('/storage/')

    raise Http404


def storage(request):
    goods_list = Storage.objects.all()
    shops_list = Shop.objects.all()
    logs_list = StorageLog.objects.all().order_by('-date')

    context = {
        'goods_list': goods_list,
        'shops_list': shops_list,
        'logs_list': logs_list
    }

    return render(request, 'storage.html', context)

def cash(request):
    cash = Cash.objects.all().order_by('-last_coming')

    context = {
        'cash': cash,
    }

    return render(request, 'cash.html', context)

def get_storage_price(request):
    if request.is_ajax():
        #storage = Storage.objects.get
        #product = Menu.objects.get(id=product_id)
        #cart = Cart(request)
        price = 0
        received_json_data = json.loads(request.body)
        if received_json_data != None:
            for pk in received_json_data:
                product = Storage.objects.get(id=pk)
                price += product.price

        response_data = {}
        response_data['result'] = price
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse("Это работает не так :(")


"""add_delivery_status functions"""
""""""
def delete_cache_fn(cache_id):
    try:
        cash = Cash.objects.get(pk=cache_id)
        cash.delete()
        return cash
    except Exception as e:
        return 0

def add_to_cache_fn(creator_url, sum, delivery, action):
    cash = Cash(
        creator_url = creator_url,
        sum = sum,
        last_coming = now.strftime('%Y-%m-%d %H:%M'),
        own_shop = delivery.shop,
        cash_type = get_object_or_404(CashType, type_code=action),
    )
    cash.save()
    return cash

def add_delivery_status_fn(status_id, delivery_id):
    status = DeliveryStatusList(
        status = get_object_or_404(DeliveryStatus, code=status_id),
        delivery = get_object_or_404(Delivery, pk=delivery_id),
        date = now.strftime('%Y-%m-%d %H:%M')
    )
    status.save()

    if status.status.code == "1":
        if status.delivery.cash_in_transaction_id != 0 and status.delivery.cash_out_transaction_id != 0:
            cash_in = delete_cache_fn(status.delivery.cash_in_transaction_id)
            cash_out = delete_cache_fn(status.delivery.cash_out_transaction_id)
        status.delivery.cash_in_transaction_id = 0
        status.delivery.cash_out_transaction_id = 0
        status.delivery.save()

    if status.status.code == "4" and status.delivery.cash_in_transaction_id == 0 and status.delivery.cash_out_transaction_id == 0:
        cash_in = add_to_cache_fn('/delivery/'+str(status.delivery.id)+'/', status.delivery.client_price(), status.delivery, 'in')
        cash_out = add_to_cache_fn('/delivery/'+str(status.delivery.id)+'/', status.delivery.delivery_price, status.delivery, 'out')
        status.delivery.cash_in_transaction_id = cash_in.id
        status.delivery.cash_out_transaction_id = cash_out.id
        status.delivery.save()

    if status.status.code == "5" and status.delivery.cash_in_transaction_id != 0 and status.delivery.cash_out_transaction_id != 0:
        cash_in = delete_cache_fn(status.delivery.cash_in_transaction_id)
        cash_out = delete_cache_fn(status.delivery.cash_out_transaction_id)
        status.delivery.cash_in_transaction_id = 0
        status.delivery.cash_out_transaction_id = 0
        status.delivery.save()

    if status.status.code == "6":
        if status.delivery.cash_in_transaction_id == 0 and status.delivery.cash_out_transaction_id == 0:
            cash_in = add_to_cache_fn('/delivery/'+str(status.delivery.id)+'/', 0, status.delivery, 'in')
            cash_out = add_to_cache_fn('/delivery/'+str(status.delivery.id)+'/', status.delivery.delivery_price, status.delivery, 'out')
            status.delivery.cash_in_transaction_id = cash_in.id
            status.delivery.cash_out_transaction_id = cash_out.id
            status.delivery.save()

    return status
""""""
"""/add_delivery_status functions"""

def add_delivery_status(request):
    if request.is_ajax():
        if request.POST.get('value') and request.POST.get('delivery'):
            new_status = add_delivery_status_fn(request.POST.get('value'), request.POST.get('delivery'))

            response_data = {}
            response_data['result'] = str(new_status.status)
            response_data['code'] = str(new_status.status.code)
            response_data['label'] = str(new_status.status.label)
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse("Это работает не так :(")

def delivery(request):
    delivery = Delivery.objects.all().order_by('-date')
    status = DeliveryStatus.objects.all()
    deliverylog = DeliveryLog.objects.all().order_by('-date')

    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DeliveryForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.cleaned_data['is_custom_product']:
                custom_product = form.cleaned_data['custom_product']
            else:
                custom_product = ''

            if form.cleaned_data['is_custom_price']:
                custom_price = form.cleaned_data['custom_price']
                #custom_price = cleaned_data['is_custom_price']
            else:
                custom_price = 0
            
            if (form.cleaned_data['delivery_fromclient'] == '' or form.cleaned_data['delivery_fromclient'] == None):
                delivery_fromclient = 0
            else:
                delivery_fromclient = form.cleaned_data['delivery_fromclient']

            created_delivery = form.save(commit=False)

            created_delivery.date = now.strftime('%Y-%m-%d %H:%M')
            created_delivery.custom_product = custom_product
            created_delivery.custom_price = custom_price
            created_delivery.delivery_fromclient = delivery_fromclient
            
            formset = DeliveryProductFormSet(request.POST, instance=created_delivery)

            if formset.is_valid():
                created_delivery.save()
                formset.save()

                new_status = DeliveryStatusList(
                    status = get_object_or_404(DeliveryStatus, code=1),
                    delivery = get_object_or_404(Delivery, pk=created_delivery.pk),
                    date = now.strftime('%Y-%m-%d %H:%M')
                )
                new_status.save()
                # redirect to a new URL:
                return HttpResponseRedirect('/delivery/')
            #else:
            #    return HttpResponse("Ошибка второй формы"+str(formset.errors))

        #else:
        #    return HttpResponse("Ошибка первой формы: "+str(form.errors))


    form = DeliveryForm()
    formset = DeliveryProductFormSet(instance=Delivery())

    context = {
        'delivery': delivery,
        'status': status,
        'deliverylog': deliverylog,
        'form': form,
        'formset': formset,
    }

    return render(request, 'delivery.html', context)

def delivery_show(request, pk):
    try:
        delivery = Delivery.objects.get(pk=pk)
    except Exception as e:
        raise Http404(e)


    context = {
        'delivery': delivery,
        
    }

    return render(request, 'delivery_show.html', context)

@login_required
def delivery_edit(request, pk):

    try:
        delivery = Delivery.objects.get(pk=pk)
        deliverylog = DeliveryLog.objects.filter(delivery=delivery).order_by('-date')
        deliveryproduct = DeliveryProduct.objects.filter(delivery=delivery)
    except Exception as e:
        raise Http404(e)

    data = {'shop': delivery.shop.id,
            'custom_product': delivery.custom_product,
            'custom_price': delivery.custom_price,
            'delivery_fromclient': delivery.delivery_fromclient,
            'delivery_price': delivery.delivery_price,
            'delivery_date': delivery.delivery_date,
            'address': delivery.address,
            'phone': delivery.phone,
            'time': delivery.time,
            'courier': (delivery.courier and delivery.courier.id or ''),
            'is_custom_price': delivery.is_custom_price,
            'is_custom_product': delivery.is_custom_product}

    
    if request.method == 'POST':
        form = DeliveryForm(request.POST, initial=data)
        formset = DeliveryProductFormSet(request.POST, request.FILES, instance=delivery)
        if formset.is_valid():
            formset.save()
        
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data['is_custom_product']:
                custom_product = form.cleaned_data['custom_product']
            else:
                custom_product = u''

            if form.cleaned_data['is_custom_price'] and form.cleaned_data['is_custom_price'] != None:
                custom_price = form.cleaned_data['custom_price']
            else:
                custom_price = 0L

            if form.cleaned_data['delivery_fromclient'] == '':
                delivery_fromclient = 0L
            else:
                delivery_fromclient = form.cleaned_data['delivery_fromclient']

            logger.error('form.cleaned_data: '+str(form.cleaned_data))

            delivery.shop = form.cleaned_data['shop']
            delivery.date = now.strftime('%Y-%m-%d %H:%M')
            delivery.custom_product = custom_product
            delivery.custom_price = custom_price
            delivery.delivery_fromclient = delivery_fromclient
            delivery.delivery_price = form.cleaned_data['delivery_price']
            delivery.delivery_date = form.cleaned_data['delivery_date']
            delivery.address = form.cleaned_data['address']
            delivery.phone = form.cleaned_data['phone']
            delivery.time = form.cleaned_data['time']
            delivery.courier = form.cleaned_data['courier']
            delivery.is_custom_product = form.cleaned_data['is_custom_product']
            delivery.is_custom_price = form.cleaned_data['is_custom_price']

            delivery.save()

            if form.has_changed():
                logger.error('form.changed_data: '+str(form.changed_data))
                arr = []
                for fieldname in form.changed_data:
                    arr.append(form.fields[fieldname].label+u' = '+unicode(form.cleaned_data[fieldname]))
                log = DeliveryLog(
                    name = u"В доставке №%s изменено: %s" % (delivery.id, ", ".join(arr)),
                    date = now.strftime('%Y-%m-%d %H:%M:%S'),
                    user = request.user,
                    shop = delivery.shop,
                    delivery = delivery,
                )
                log.save()

            return HttpResponseRedirect('/delivery/')

    else:
        form = DeliveryForm(data)
        
        formset = DeliveryProductFormSet(instance=delivery)
        context = {
            'delivery': delivery,
            'deliverylog': deliverylog,
            'deliveryproduct': deliveryproduct,
            'form': form,
            'formset': formset,
        }

        return render(request, 'delivery_edit.html', context)


def delivery_status(request, pk):

    try:
        delivery = Delivery.objects.get(pk=pk)
        statuslist = DeliveryStatusList.objects.filter(delivery__pk=pk)
        status = DeliveryStatus.objects.all()
    except Exception as e:
        raise Http404(e)

    if request.method == "POST":
        if request.POST.get('add_status'):
            new = DeliveryStatusList(
                status = get_object_or_404(DeliveryStatus, pk=request.POST.get('status')),
                delivery = get_object_or_404(Delivery, pk=pk),
                date = now.strftime('%Y-%m-%d %H:%M')
            )
            new.save()

            return HttpResponseRedirect(reverse('delivery_status', args=(pk,)))

    context = {
        'delivery': delivery,
        'statuslist': statuslist,
        'status': status,
    }

    return render(request, 'delivery_status.html', context)


