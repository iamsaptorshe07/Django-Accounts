from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# User Model For registration ---------------------------------------------------------------------------
class UserManager(BaseUserManager):
    def create_user(self, name,email,gender, password):
        """
        Creates and saves a User with the given email and password.
        """
        if not gender:
            raise ValueError('User must have a gender')
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name = name,
            email=self.normalize_email(email),
            gender = gender,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, gender, password,):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            name = name,
            email=self.normalize_email(email),
            gender = gender,
            password=password,
          
           
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    GENDER_CHOICE = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )
    name = models.CharField(max_length=100, default='Open Blog Forum User')
    gender = models.CharField(max_length=10,null=True, blank=False, choices = GENDER_CHOICE)
    creationTime = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','gender']

    def __str__(self):
        return self.email

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
# User Model Ends ---------------------------------------------------------------------------------------
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=200, unique=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    picture = models.ImageField(upload_to='User Picture', blank=True, null=True)
    profession = models.CharField(max_length=200,blank=True, null=True)
    birthdate = models.DateField()
    country = models.CharField(max_length=200)
    followers = models.ManyToManyField(User, related_name='followers',blank=True)
    
    def __str__(self):
        return self.user.name