from django.db import models

from django.utils.translation import ugettext_lazy as _

from pprint import pprint

# Create your models here.
# pk value is the id of the device
    
class users(models.Model):
    auth_user = models.ForeignKey('auth.User')
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
    DEFAULT,REGISTERED,PENDING='Default','Registered','Pending'
    USER_STATUS = ( (DEFAULT,_(DEFAULT)),(REGISTERED,_(REGISTERED)) ,(PENDING,_(PENDING))  )
    user_type = models.CharField(max_length=200,choices=USER_STATUS,default=DEFAULT)
    
    LOGGED_IN,LOGGED_OUT='Logged in','Logged out'
    LOGGED_STATUS = ( (LOGGED_IN,_(LOGGED_IN)),(LOGGED_OUT,_(LOGGED_OUT))  )
    login_status = models.CharField(max_length=200,choices=LOGGED_STATUS,default=LOGGED_OUT)
    
    email = models.EmailField(max_length=200,blank=True)
    reg_date = models.DateField(blank=True);
    
class devices(models.Model):
    device_owner = models.ForeignKey(users)
    device_name = models.CharField(max_length=200)
    device_creation_date = models.DateField();
    
    BROWSER,MOBILE = 'Web Browser','Mobile App'
    DEVICE_TYPE = ( (BROWSER,_(BROWSER)), (MOBILE,_(MOBILE)) )
    
    device_type = models.CharField(max_length=200,choices=DEVICE_TYPE,default=BROWSER)
    
class billboards(models.Model):
    owner = models.ForeignKey(users)
    name = models.CharField(max_length=200)
    lat = models.DecimalField(decimal_places=7,max_digits=10)
    lng = models.DecimalField(decimal_places=7,max_digits=10)
    
class messages(models.Model):
    owner = models.ForeignKey(users)
    billboard = models.ForeignKey(billboards)
    text = models.CharField(max_length=200)
    

    

    
    
                           
