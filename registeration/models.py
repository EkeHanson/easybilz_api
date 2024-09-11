from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, user_type, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, user_type, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")
        
        return self.create_user(email=email, password=password, user_type=user_type, **extra_fields)


class CustomUser(AbstractUser):
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=15)
    image = models.ImageField(blank=True, null=True, upload_to='user_images')
    firstName = models.CharField(max_length=255)
    otherNames = models.CharField(max_length=255, default="None")
    middleName = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=80, unique=False, blank=True, null=True)
    email = models.EmailField(max_length=80, unique=True)
    user_type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('customer', 'Customer'), ('owner', 'Owner')])

    # New fields
    maritalStatus = models.CharField(max_length=50, blank=True, null=True, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')])
    stateOfOrigin = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True,  choices=[('Male', 'Male'), ('Female', 'Female')])
    motherName = models.CharField(max_length=255, blank=True, null=True)
    residenceAddress = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    mobileNumber = models.CharField(max_length=15, blank=True, null=True)
    identity = models.CharField(max_length=100, blank=True, null=True)
    identityNumber = models.CharField(max_length=100, blank=True, null=True)
    employmentStatus = models.CharField(max_length=50, blank=True, null=True)
    annualSalary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    businessName = models.CharField(max_length=255, blank=True, null=True)
    officePhoneNumber = models.CharField(max_length=15, blank=True, null=True)
    nextOfKinFname = models.CharField(max_length=255, blank=True, null=True)
    nextOfKinSurname = models.CharField(max_length=255, blank=True, null=True)
    nextOfKinOtherNames = models.CharField(max_length=255, blank=True, null=True)
    nextOfKinDOB = models.DateField(blank=True, null=True)
    nextOfKinRelationship = models.CharField(max_length=255, blank=True, null=True)
    nextOfKinPhone = models.CharField(max_length=15, blank=True, null=True)
    nextOfKinHomeAddress = models.CharField(max_length=255, blank=True, null=True)
    nextOfKinEmail = models.EmailField(blank=True, null=True)
    nextOfKinTown = models.CharField(max_length=255, blank=True, null=True)
    nextOfKinState = models.CharField(max_length=255, blank=True, null=True)
    accountName = models.CharField(max_length=255, blank=True, null=True)
    accountNumber = models.CharField(max_length=50, blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"  # Set the email field as the unique identifier
    REQUIRED_FIELDS = ["user_type"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
