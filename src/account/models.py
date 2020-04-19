from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



# Custom user manager
class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username!")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Own custom user model
class Account(AbstractBaseUser):

    username = models.CharField(max_length=30, unique=True)

    guardianSource = models.BooleanField(default=True)
    bbcSource = models.BooleanField(default=False)
    independentSource = models.BooleanField(default=False)

    categoryTech = models.BooleanField( default=True)
    categoryPolitics = models.BooleanField( default=False)
    categorySport = models.BooleanField( default=False)


    # The fields bellow are REQUIRED for AbstractBaseUser class (for custom user model)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # setting the USERNAME_FIELD to whatever we want the user to be able to log in with
    USERNAME_FIELD = 'username'

    # Referrences the account manager
    objects = MyAccountManager()

    # Whenever we print an account object to a template, display the username
    def __str__(self):
        return self.username

    # Required functions for custom users
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class ScraperData(models.Model):
    name = models.CharField(max_length=30, default="lastScraped")
    lastScraped = models.DateTimeField(verbose_name="last scraped")

    def __str__(self):
        return "lastScraped"
