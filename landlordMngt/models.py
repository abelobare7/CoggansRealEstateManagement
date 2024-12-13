from django.db import models

# Create your models here.
class Documents(models.Model):
    name = models.CharField('Name', max_length=20)
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    phone_number = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.phone_number
