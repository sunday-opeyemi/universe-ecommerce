from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class profile(models.Model):
    countries = [
        ("Nigeria", "NIgeria"),
        ("Ghana", "Ghana"),
        ("United Kingdom", "UK"),
        ("USA", "USA")
    ]

    states = [
        ("Abia", "Abia"),
        ("Oyo", "Oyo"),
        ("Osun", "Osun"),
        ("Lagos", "Lagos"),
        ("Kano", "Kano"),
        ("Abuja", "Abuja"),
    ] 

    position = [
        ("CEO", "CEO"),
        ("GMD", "GMD"),
        ("CTO", "CTO"),
        ("Supervisor", "Supervisor"),
        ("Accountant", "Accountant"),
        ("Marketer", "Marketer"),
        ("Staff", "Staff"),
        ("HR", "HR"),    
    ]
    ma_status = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Divorce", "Divorce"),
        ("Complicate", "Complicate")
    ]

    gen = [
        ("Female", "Female"),
        ("Male", "Male"),
    ]

    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=gen, unique=False, max_length=6)
    phone = models.CharField(unique=True, max_length=14, null=True)
    address = models.CharField(unique=False, max_length=100, null=True)
    staff_id = models.CharField(max_length=8, null=True, unique=False)
    state = models.CharField(choices=states, unique=False, max_length=20, null=True)
    nationality = models.CharField(choices=countries, unique=False, max_length=50, null=True)
    position = models.CharField(choices=position, unique=False, max_length=20, null=True)
    marital_status = models.CharField(choices=ma_status, unique=False, max_length=20, null=True)
    profile_passport = models.ImageField(upload_to='staffImage/', unique=False, null=True)
    particulars = models.FileField(upload_to='particularsImage/',unique=False, null=True)
    staff = models.BooleanField(default=False, unique=False)

# Now this is where the magic happens: we will now define signals so our profile model will be automatically created upon/updated when we create/update User instances
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

