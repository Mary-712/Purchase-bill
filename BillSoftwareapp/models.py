from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    Company_code = models.CharField(max_length=100,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    pan_number = models.CharField(max_length=255,null=True,blank=True)
    gst_type = models.CharField(max_length=255,null=True,blank=True)
    gst_no = models.CharField(max_length=255,null=True,blank=True)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/patient')


class staff_details(models.Model):
    company = models.ForeignKey(company, on_delete=models.CASCADE,null=True,blank=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    user_name = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=255,null=True,blank=True)
    img = models.ImageField(null=True,blank = True,upload_to = 'image/staff')    
    position = models.CharField(max_length=255,null=True,blank=True,default='staff')
    
class Parties(models.Model):
    party_name = models.CharField(max_length =255)
    phone_number = models.CharField(max_length = 10)
    gstin = models.CharField(max_length =16)
    gst_type = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    opening_balance = models.FloatField(default = 0)
    to_pay = models.BooleanField(null=True)
    to_recieve = models.BooleanField(null = True)
    date =  models.DateField(null = True)
    company = models.ForeignKey(company,on_delete=models.CASCADE,default='')
    created_by = models.ForeignKey(staff_details,on_delete=models.CASCADE,default='')
    last_updated_by = models.CharField(max_length=255,default='')
    
class ItemModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company,on_delete= models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details,on_delete= models.CASCADE,null=True,blank=True)
    item_name = models.CharField(max_length=255)
    item_hsn = models.PositiveIntegerField(null=True)
    item_unit = models.CharField(max_length=255)
    item_taxable = models.CharField(max_length=255)
    item_gst = models.CharField(max_length=255,null=True)
    item_igst = models.CharField(max_length=255,null=True)
    item_sale_price = models.PositiveIntegerField()
    item_purchase_price = models.PositiveBigIntegerField()
    item_stock_in_hand = models.PositiveBigIntegerField(default=0)
    item_at_price = models.PositiveBigIntegerField(default=0)
    item_date = models.DateField()

class FirstBill(models.Model):
    customer = models.ForeignKey(Parties,on_delete=models.CASCADE,null=True,blank=True)
    bill_number=models.PositiveIntegerField()
    bill_date =  models.DateField(null = True)
    supply_source=models.CharField(max_length=150,null=True)
