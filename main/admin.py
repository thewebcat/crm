from django.contrib import admin

from main.models import (
	Shop,
	Service,
	Storage,
	StorageLogType,
	StorageLog,
	Delivery,
	DeliveryProduct,
	Courier,
	Cash,
	CashType,
	DeliveryStatus,
	DeliveryStatusList,
	DeliveryLog,
)

class ShopAdmin(admin.ModelAdmin):
    list_display = ('url', 'alias', 'directors_name', 'directors_phone', 'directors_email', 'servises_list', 'last_calculation')

class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'last_coming')


class DeliveryAdminInline(admin.StackedInline):
	model = DeliveryProduct
	extra = 0
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('shop', 'date', 'delivery_date', 'address', 'cash_in_transaction_id', 'cash_out_transaction_id', 'storage_in_transaction_id', 'storage_out_transaction_id')
    inlines = [DeliveryAdminInline]

class DeliveryProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'count', 'delivery_id')

admin.site.register(Shop, ShopAdmin)
admin.site.register(Service)
admin.site.register(Storage, StorageAdmin)
admin.site.register(StorageLogType)
admin.site.register(StorageLog)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(DeliveryProduct, DeliveryProductAdmin)
admin.site.register(Courier)
admin.site.register(Cash)
admin.site.register(CashType)
admin.site.register(DeliveryStatus)
admin.site.register(DeliveryStatusList)
admin.site.register(DeliveryLog)