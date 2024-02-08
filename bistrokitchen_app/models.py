from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY = ((1, 'Starter'), (2, 'Breakfast'), (3,'Lunch'), (4, 'Dinner'), (5, 'Bread & Rice'))
class menuitem(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Item Name")
    price = models.FloatField()
    details = models.CharField(max_length = 200, verbose_name = "Item Details")
    category = models.IntegerField(choices = CATEGORY)
    is_active = models.BooleanField(default = True, verbose_name = "Available")
    menuimage = models.ImageField(upload_to='image')


class cart(models.Model):
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = "uid")
    pid = models.ForeignKey(menuitem, on_delete = models.CASCADE, db_column = "pid")
    qty = models.IntegerField(default = 1)

class order(models.Model):
    orderid = models.CharField(max_length = 50)
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = "uid")
    pid = models.ForeignKey(menuitem, on_delete = models.CASCADE, db_column = "pid")
    qty = models.IntegerField(default = 1)


class contact(models.Model):
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100)
    subject = models.CharField(max_length = 200)
    message = models.CharField(max_length = 500)


class chef(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Chef's Name")
    position = models.CharField(max_length = 50)
    chefdetails = models.CharField(max_length = 150)
    chefimage = models.ImageField(upload_to='image')

class testimonial(models.Model):
    testimony = models.CharField(max_length = 150)
    pname = models.CharField(max_length = 50, verbose_name = "Person's Name")
    ptitle  = models.CharField(max_length = 50, verbose_name = "Person's Title")
    ptimage = models.ImageField(upload_to='image')