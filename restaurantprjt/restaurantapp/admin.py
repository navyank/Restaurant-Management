from django.contrib import admin
from .models import Employee,Food,OrderItems,OrderDetails,District,State
from restaurantapp import forms
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.
class EmpAdmin(admin.ModelAdmin):
    list_display=('FullName','ID_Number','Gender','phoneNumber','state','district')
class FoodAdmin(admin.ModelAdmin):
    list_display=('items','price')    
    form=forms.FoodForm
class OrderItemsModelAdmin(admin.ModelAdmin):
    list_display = ('OrderId', 'Items', 'Quantity')
    
class OrderItemsAdmin(admin.TabularInline):  # Make sure it's a TabularInline or StackedInline
    model = OrderItems
    list_display = ('OrderId', 'Items', 'Quantity')
    extra=1
    min_num=1
    # max_num=2

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('OrderId', 'location', 'orderDate', 'DeliveryTime', 'staff', 'price','view_order_items')
    exclude = ('OrderId', 'price')
    inlines = [OrderItemsAdmin] 
    def view_order_items(self, obj):
        url = reverse('admin:%s_%s_changelist' % (OrderItems._meta.app_label,  OrderItems._meta.model_name))
        return format_html('<a href="{}?OrderId__id__exact={}">View Food Items</a>', url, obj.id)

    view_order_items.short_description = 'Food Items'
   
    def save_model(self, request, obj, form, change):
        if not obj.OrderId:
            # Generate OrderID based on customer name, date, and time
            date_str = obj.orderDate.strftime("%m_%d")
            time_str = obj.DeliveryTime.strftime("%H_%M")
            obj.OrderId = f"{obj.Customer}_{date_str}_{time_str}"

        super().save_model(request, obj, form, change)

class StateAdmin(admin.ModelAdmin):
    list_display=('state',) 
class DistAdmin(admin.ModelAdmin):
    list_display=('state','district')                    
admin.site.register(Employee,EmpAdmin)
admin.site.register(Food,FoodAdmin)
admin.site.register(OrderItems,OrderItemsModelAdmin)
admin.site.register(OrderDetails,OrderDetailsAdmin)
admin.site.register(District,DistAdmin)
admin.site.register(State,StateAdmin)
