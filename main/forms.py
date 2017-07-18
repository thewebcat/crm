# -*- coding: utf-8 -*-

from django import forms
from django.forms import models, inlineformset_factory

from main.models import Delivery, DeliveryProduct, Shop, Storage, Courier

# class AddDeliveryForm(forms.Form):

# 	#shop = forms.CharField(label='Выберите магазин', max_length=100)
# 	#shop = forms.ModelChoiceField( attrs={'class': 'form-control', 'placeholder': 'Имя', 'aria-describedby': 'helpBlock1',}, queryset=Shop.objects.all())
# 	shop = forms.ModelChoiceField(
# 		label = 'Выберите магазин',
#         queryset = Shop.objects.all(),
#         widget = forms.Select(attrs={'class': 'form-control',})
#     )

# 	# PRODUCT_CHOICES=[('0','select 1'), ('1','select 2')]

# 	# is_custom_product = forms.ChoiceField(
# 	# 	choices=PRODUCT_CHOICES,
# 	# 	widget=forms.RadioSelect()
# 	# )
# 	is_custom_product = forms.BooleanField(required=False)
# 	is_custom_price = forms.BooleanField(required=False)

# 	custom_product = forms.CharField(
# 		label='Другой товар',
# 		max_length=100,
# 		widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите наименование', }),
# 		required=False
# 	)

# 	custom_price = forms.IntegerField(
# 		label='Другая цена',
# 		widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену', }),
# 		required=False
# 	)

# 	delivery_fromclient = forms.IntegerField(
# 		label='Стоимость доставки с клиента',
# 		widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену', }),
# 		required=False
# 	)

# 	delivery_price = forms.IntegerField(
# 		label='Стоимость доставки',
# 		widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену', }),
# 		required=False
# 	)

# 	delivery_date = forms.DateField(
# 		label='Дата доставки',
# 		widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите дату', }),
# 	)

# 	address = forms.CharField(
# 		label='Адрес доставки',
# 		max_length=100,
# 		widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес', })
# 	)

# 	phone = forms.CharField(
# 		label='Телефон клиента',
# 		max_length=100,
# 		widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите телефон', })
# 	)

# 	time = forms.CharField(
# 		label='Время доставки',
# 		max_length=100,
# 		widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите временной диапазон', }),
# 		required=False
# 	)

# 	courier = forms.ModelChoiceField(
# 		label = 'Курьер',
#         queryset = Courier.objects.all(),
#         widget = forms.Select(attrs={'class': 'form-control',}),
#         required=False
#     )



class DeliveryForm(models.ModelForm):
    class Meta:
        model = Delivery
        exclude = ('date', 'cash_in_transaction_id', 'cash_out_transaction_id', 'storage_in_transaction_id', 'storage_out_transaction_id' )
        widgets = {
        	'shop': forms.Select(attrs={'class': 'form-control','required': True}),
        	'custom_product': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите наименование', }),
        	'custom_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену', }),
        	'delivery_fromclient': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену', }),
        	'delivery_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену', }),
        	'delivery_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите дату', 'required': True}),
        	'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'required': True}),
        	'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите телефон', 'required': True}),
        	'time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите временной диапазон', }),
        	'courier': forms.Select(attrs={'class': 'form-control',}),
        }

DeliveryProductFormSet = inlineformset_factory(Delivery, DeliveryProduct,
        formset=models.BaseInlineFormSet,
        fields=('product', 'delivery', 'count'),
        widgets={
            'product': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'count': forms.TextInput(attrs={'class': 'form-control', 'required': True})
        },
        extra=1,
        can_delete = True
    )