from django.contrib import admin

# Register your models here.
from usermanagement.models import devices,user_policy,billboards,messages

class devices_admin(admin.ModelAdmin):
    list_display=('device_name','device_creation_date','device_type')
    list_filter=('device_name','device_creation_date','device_type')

class users_admin(admin.ModelAdmin):
    list_display=('user_name','password','user_type','login_status','email','reg_date')
    list_filter=('user_name','password','user_type','login_status','email','reg_date')

class billboards_admin(admin.ModelAdmin):
    list_display=('owner','name','lat','lng')
    list_filter=('owner','name','lat','lng')

class messages_admin(admin.ModelAdmin):
    list_display=('owner','billboard','text','start_date','stop_date')
    list_filter=('owner','billboard','text','start_date','stop_date')
    
admin.site.register(devices,devices_admin)
admin.site.register(user_policy,users_admin)
admin.site.register(billboards,billboards_admin)
admin.site.register(messages,messages_admin)