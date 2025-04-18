from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUserManager(BaseUserManager):
    def create_user(self, phone ,  **extra_fields):
        """
        Creates and saves a User with the given phone, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an phone number")

        user = self.model(
            phone=phone,
            **extra_fields
        )


        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            **extra_fields,
            
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True)
    verify_code = models.CharField(max_length=11)

    is_active = models.BooleanField(default=True)
    is_Doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="Profile")
    first_name = models.CharField(max_length=50, blank=True, null=False, verbose_name="نام")
    last_name = models.CharField(max_length=50, blank=True, null=False, verbose_name="نام خانوادگی")
    nationality_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد ملی")
    personal_code = models.CharField(max_length=5, blank=True, null=False, verbose_name="کد نظام پزشکی")
    date_of_birth = models.CharField(max_length=12, blank=True, null=False, verbose_name="تاریخ تولد")
    city = models.CharField(max_length=70, blank=True, null=False, verbose_name="شهر")
    address = models.CharField(max_length=200, blank=True, null=False, verbose_name="آدرس")
    photo = models.ImageField(upload_to='face/', verbose_name="عکس")
    nationality_photo = models.ImageField(upload_to='nationality/', verbose_name="عکس کارت ملی")
    personal_photo = models.ImageField(upload_to='personal/', verbose_name="عکس کارت پرسنلی")


@receiver(post_save, sender=MyUser)
def save_profile_user(sender, instance, created, **kwargs):
    if created and instance.is_Doctor:
        profile_user = Profile(user=instance)
        profile_user.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ManyToManyField(Category, verbose_name="دسته", related_name="post")
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=250)
    price = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
