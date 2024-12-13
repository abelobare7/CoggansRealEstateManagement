from django.db import models
from accounts.models import CustomUser
from multiupload.fields import MultiFileField
from django.core.validators import MinValueValidator

# Create your models here.


class Listing(models.Model):
    PROPERTY_TYPES = (
        ("townhouse", "Town House"),
        ("apartment", "Apartment"),
        ("bungalow", "Bungalow"),
        ("studio", "Studio"),
    )

    PROPERTY_STATUSES = (
        ("rent", "For Rent"),
        ("sale", "For Sale"),
    )

    landlord = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "landlord"},
        editable=False,
    )
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(
        max_length=30, choices=PROPERTY_TYPES, default="house"
    )
    status = models.CharField(max_length=15, choices=PROPERTY_STATUSES, default="sale")
    units_available = models.PositiveIntegerField(validators=[MinValueValidator(0)],)
    bedrooms = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    bathrooms = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    square_feet = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    views = models.PositiveIntegerField(validators=[MinValueValidator(0)],default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    images = MultiFileField(min_num=4, max_num=10, max_file_size=1024 * 1024 * 5)

    @property
    def price_display(self):
        return "Ksh %s" % self.price

    def __str__(self):
        return f"| {self.title:30} | Ksh{self.price:10} |"

class ViewRequest(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"