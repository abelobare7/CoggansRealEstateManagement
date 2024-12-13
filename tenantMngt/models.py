from django.db import models
from accounts.models import CustomUser
from listings.models import Listing



class PropertyInquiry(models.Model):
    property = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type":"tenant"})
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.first_name} to {self.receiver.first_name}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Tenant(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type": "tenant"}
    )
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type": "tenant"}
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="maintenance_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ),
    )


class Communication(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sent_communications",
        limit_choices_to={"user_type": "tenant"},
    )
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="received_communications",
        limit_choices_to={"user_type": "landlord"},
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    tenant = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type": "tenant"}
    )
    document = models.FileField(upload_to="tenant_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Lease(models.Model):
    tenant = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type": "tenant"}
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, limit_choices_to={"status":"rent"})
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    additional_terms = models.TextField(blank=True, null=True)
