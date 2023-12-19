from django.db import models
from django.utils import timezone


# Create your models here.


class Slider(models.Model):
  name = models.CharField(max_length=200)
  image = models.ImageField(upload_to='slider')
  
  def __str__(self):
    return self.name
  

class User(models.Model):
  name = models.CharField(max_length=200)
  email = models.EmailField(max_length=200)
  password = models.CharField(max_length=200 , default="123456789")
  phone = models.CharField(max_length=20)
  local_address = models.TextField(max_length=300)
  town = models.CharField(max_length=100)
  dist = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  zip = models.IntegerField()
  profile_pic = models.ImageField(upload_to='user_images' )
  dob = models.CharField(max_length=50)
  
  def __str__(self):
    return self.name
  
  
class Brand(models.Model):
  name = models.CharField(max_length=200)
  brand_pic = models.ImageField(upload_to='brand_images' , default='none.jpg')
  
  def __str__(self):
    return self.name
  
  

class Category(models.Model):
  name = models.CharField(max_length=200)
  category_pic = models.ImageField(upload_to='category_images' , default='none.jpg')
  
  def __str__(self):
    return self.name
  


class Product(models.Model):
  name = models.CharField(max_length=200)
  brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
  description = models.TextField(max_length=700)
  warranty = models.FloatField()
  original_price = models.IntegerField()
  discounted_price = models.IntegerField()
  replacement_time = models.IntegerField()
  shipping_cost = models.IntegerField()
  offer = models.BooleanField(default=False)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  product_pic = models.ImageField(upload_to='product_images' , default='none.jpg')
  
  def __str__(self):
    return self.name
    
    
class Cart(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  count = models.IntegerField(default=1)
  
  def __str__(self):
    return self.product.name
    

class Order(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  count = models.IntegerField(default=1)
  total_price = models.IntegerField()
  delivery_date = models.DateField(default=timezone.now() + timezone.timedelta(days=7))
  
  def __str__(self):
    return self.user.name