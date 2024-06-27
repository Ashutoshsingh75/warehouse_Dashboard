
from email.policy import default
from unicodedata import category
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField

class LaundryUser(models.Model):
    name=models.CharField(max_length=100 )
    username=models.CharField(max_length=100,unique=True )
    email=models.CharField(max_length=100,unique=True,help_text='Enter the company name')
    phone=models.CharField(max_length=10)
    email=models.EmailField()
    address=models.CharField(max_length=1000)
    pin = models.CharField(max_length=10,default=None,blank=True,null=True)
    city = models.CharField(max_length=20,default=None,blank=True,null=True)
    state = models.CharField(max_length=20,default=None,blank=True,null=True)
    password=models.CharField(max_length=200,default=0)
    img = models.ImageField(upload_to="user_images/",default=None,blank=True,null=True)
    user_type = models.CharField(max_length=10000, choices=(('admin','admin'), ('laundry_shop_user', 'laundry_shop_user'), ('customer', 'customer')), default = "customer")
    def __str__(self):
        return self.username




class LaundryshopeUser(models.Model):
    name=models.ForeignKey(LaundryUser,on_delete=models.CASCADE,related_name="laundry_shop_user")
    shop_address=models.CharField(max_length=1000,null=True ,blank=True,default=None)
    shop_name=models.CharField(max_length=100,unique=True,help_text='Enter the shop name')
    shop_img = models.ImageField(upload_to="shop_images/",default=None,blank=True,null=True)
    
    


class Laundrytype(models.Model):
    user=models.ForeignKey(LaundryshopeUser,on_delete=models.CASCADE,)
    type=models.CharField(max_length=1000,null=True ,blank=True,default=None)
    price = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=200, choices=(('active','Active'), ('active','Inactive')), default = "active")
    def __str__(self):
        return self.user.name.name


class Order_details(models.Model):
    shop_id=models.CharField(max_length=100,blank=False)
    shop_name=models.CharField(max_length=1000,blank=False)
    clint_id=models.CharField(max_length=1000,blank=False)
    clint_name=models.CharField(max_length=1000,blank=False,null=True)
    contact = models.CharField(max_length=250, blank=True, null = True)
    clint_address=models.CharField(max_length=1000,blank=True)
    category= ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    order_time = models.DateTimeField(default = timezone.now)
    total_amount = models.FloatField(max_length=15,null=True,blank=True)
    status = models.CharField(max_length=100, choices=(('Pending','Pending'), ('In-progress', 'In-progress'), ('Done', 'Done'), ('Picked Up', 'Picked Up')), default = "Pending")
    payment = models.CharField(max_length=100, choices=(('Unpaid','Unpaid'), ('Paid', 'Paid')), default = 'Unpaid')
    payment_status=models.CharField(max_length=100, choices=(('ONLINE','ONLINE'), ('COD', 'COD')), default = "COD")
    orderId = models.CharField(
        max_length=500, default=None, blank=True, null=True)
    paymentId = models.CharField(
        max_length=500, default=None, blank=True, null=True)
    paymentsignature = models.CharField(
        max_length=500, default=None, blank=True, null=True)
    date_updated = models.DateTimeField(default = timezone.now)
    delivery_date=models.DateTimeField(default = timezone.now)



    
        
class Laundry(models.Model):
    code = models.CharField(max_length=100)
    client = models.CharField(max_length=250)
    contact = models.CharField(max_length=250, blank=True, null = True)
    total_amount = models.FloatField(max_length=15)
    tendered = models.FloatField(max_length=15)
    status = models.CharField(max_length=100, choices=(('Pending','Pending'), ('In-progress', 'In-progress'), ('Done', 'Done'), ('Picked Up', 'Picked Up')), default = "Pending")
    payment = models.CharField(max_length=100, choices=(('Unpaid','Unpaid'), ('Paid', 'Paid')), default = "Unpaid")
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    delivery_date=models.DateTimeField(default = timezone.now)
