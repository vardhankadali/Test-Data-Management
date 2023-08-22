from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse




class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)




class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Requester"), (3, "Supplier"))
    GENDER = [("M", "Male"), ("F", "Female")]
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + " " + self.first_name



class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)



class Supplier(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name



class Requester(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name



class Request(models.Model):
    STATUS = (('new', "New"), ('pending', "Pending"), ('closed', "Closed"))
    ENV_SWIMLANE = ()
    TYPE_OF_DATA_SETUP = (('new', "New"),('existing', "Existing"),('inforce', "Inforce"),('gold copy', "Gold Copy"),('not applicable', "Not Applicable"))
    TYPE_OF_REQUEST = (('normal', "Normal"), ('expediate', "Expediate"))
    STATE_JURISDICTION = ()

    status = models.CharField(default='new', choices=STATUS, max_length=100)
    requested_by = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default="Unknown")
    assigned_to = models.CharField(max_length=100, default="-----")
    type_of_request = models.CharField(default='normal', choices=TYPE_OF_REQUEST, max_length=100)
    env_swimlane = models.CharField(max_length=100, default="-----")
    project_name = models.CharField(max_length=100, default="-----")
    number_of_records = models.CharField(max_length=100, default="-----")
    application = models.CharField(max_length=100, default="-----")
    expected_date = models.DateField()
    type_of_data_setup = models.CharField(default='new', choices=TYPE_OF_DATA_SETUP, max_length=100)
    stakeholders = models.TextField()
    state_jurisdiction = models.CharField(default='new', choices=TYPE_OF_DATA_SETUP, max_length=100)
    synopsis_of_request = models.TextField()
    description_of_request = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    test_data = models.FileField(upload_to="testdata/", null=True, default=None, max_length=250)

    def get_absolute_url(self):
        return reverse('detail_requests', kwargs={'pk':self.pk})


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Requester.objects.create(admin=instance)
        if instance.user_type == 3:
            Supplier.objects.create(admin=instance)



@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.requester.save()
    if instance.user_type == 3:
        instance.supplier.save()
