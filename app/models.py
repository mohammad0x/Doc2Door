from django.db import models
import jdatetime
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
    qty = models.CharField(max_length=11 ,default=0, verbose_name="موجودی حساب")
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
    verify = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.first_name}   {self.last_name}'



@receiver(post_save, sender=MyUser)
def save_profile_user(sender, instance, created, **kwargs):
    if created and instance.is_Doctor:
        profile_user = Profile(user=instance)
        profile_user.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name="عنوان")
    slug = models.CharField(max_length=100, unique=True,verbose_name="صاحب عنوان")

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ManyToManyField(Category, verbose_name="دسته", related_name="post")
    title = models.CharField(max_length=150,verbose_name="عنوان")
    slug = models.CharField(unique=True, max_length=250)
    price = models.CharField(max_length=10,verbose_name="قیمت")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان ساخت")

    @property
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y/%m/%d - %H:%M')

    def __str__(self):
        return self.title

class Reserve(models.Model):
    user = models.ForeignKey(MyUser , on_delete=models.CASCADE , name='user')
    post = models.ForeignKey(Post , on_delete=models.CASCADE , name='post')
    city = models.CharField(max_length=70, blank=False, null=True,verbose_name="شهر")
    address = models.CharField(max_length=250,verbose_name="آدرس")
    plate = models.CharField(max_length=10,verbose_name="پلاک")
    name = models.CharField(max_length=150,verbose_name="نام و نام خانوادگی")
    insurance = models.CharField(max_length=100 , null=True,verbose_name="بیمه")
    paid = models.BooleanField(default=False,verbose_name="پرداخت")
    accept = models.BooleanField(default=False,verbose_name="قبول شدن")
    location = models.CharField(max_length=200 ,verbose_name="مکان")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان رزرو")

    def __str__(self):
        return f"{self.user.phone } {self.post.title}"

    @property
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y/%m/%d - %H:%M')


class News(models.Model):
    title = models.CharField(max_length=100,verbose_name=" عنوان")
    slug = models.CharField(max_length=100 , unique=True,verbose_name=" صاحب عنوان")
    desc = models.TextField(verbose_name="متن")
    image = models.ImageField(upload_to='Image_news/',verbose_name="عکس")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان ساخت")

    @property
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y/%m/%d - %H:%M')

    def __str__(self):
        return self.title


class Accept(models.Model):
    reserve = models.ForeignKey(Reserve , on_delete=models.CASCADE , related_name = 'acceptReserve')
    user = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="زمان تایید")



class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=250 , null=True)
    text = models.TextField()

    def __str__(self):
        return self.phone