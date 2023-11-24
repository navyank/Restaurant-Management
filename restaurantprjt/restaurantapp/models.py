from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import RegexValidator

# Create your models here.
class State(models.Model):
    state=models.CharField(max_length=50) 
     
    
    def __str__(self):
        return self.state 
class District(models.Model):
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    district=models.CharField(max_length=50)
      
    
        
    def __str__(self):
        return self.district
class Employee(models.Model):
    FullName=models.CharField(max_length=50)
    ID_Number=models.IntegerField()
    MY_GENDER = (("male","Male"), ("female","Female"), ("others","Others"))
    Gender=models.CharField(max_length=300,choices=MY_GENDER,verbose_name="Gender")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phoneNumber = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    state=models.ForeignKey(State,on_delete=models.CASCADE)  
    district=ChainedForeignKey(District,
        chained_field="state",
        chained_model_field="state",
        show_all=False,
        auto_choose=True,
        sort=True)  
    def __str__(self):
        return self.FullName
# class Customer(models.Model):
#     FullName=models.CharField(max_length=50)    
#     phoneNumber=models.CharField(max_length=50)
#     MY_GENDER = (("male","Male"), ("female","Female"), ("others","Others"))
#     Gender=models.CharField(max_length=300,choices=MY_GENDER,verbose_name="Gender")
#     location=models.CharField(max_length=50)
#     def __str__(self):
#         return self.FullName
class OrderDetails(models.Model):
    OrderId=models.CharField(max_length=50)
    Customer=models.CharField(max_length=50)  
    location=models.CharField(max_length=50)
    orderDate=models.DateField() 
    DeliveryTime=models.TimeField()
    staff=models.ForeignKey(Employee,on_delete=models.CASCADE) 
    price = models.IntegerField(default=0)
    def __str__(self):
        return self.OrderId
class Food(models.Model):
    items=models.CharField(max_length=50)
    price = models.IntegerField()
    def __str__(self):
        return self.items
class OrderItems(models.Model):
    OrderId=models.ForeignKey(OrderDetails,on_delete=models.CASCADE)
    Items=models.ForeignKey(Food,on_delete=models.CASCADE)
    Quantity=models.CharField(max_length=50)
    def save(self, *args, **kwargs):
        total_price = float(self.Items.price) * int(self.Quantity)
        order_details = self.OrderId
        order_details.price += total_price
        order_details.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.Items)
   