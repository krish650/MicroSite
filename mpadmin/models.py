from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, Permission, _user_has_perm, Group)
import hashlib
import time

GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

USER_ROLES = (
              ('Admin', 'Admin'), # Admin
              ('PM', 'Project Manager'),
              ('Designer', 'Designer'),
              ('Developer', 'Developer'),
              ('Employee', 'Employee'), # Employee
              )
    
    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        
        if not email:
            raise ValueError('Users must have an email address')
        c = ContactDetails.objects.create(address='')
        user = self.model(email=EUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, db_index=True,)
    user_roles = models.CharField(choices=USER_ROLES, max_length=10)
    date_of_birth = models.DateField(default='1970-01-01')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    gender = models.CharField(choices = GENDER_TYPES ,max_length = 10)
    fb_profile = models.URLField(default='')
    tw_profile = models.URLField(default='')
    ln_profile = models.URLField(default='')
    google_plus_url = models.URLField(default='')

    about = models.CharField(max_length=2000, default='', null=True, blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=150)
    address = models.TextField(max_length=1000, default='')
    mobile = models.BigIntegerField(default='0')
    website = models.URLField(default='',null=True)
    phones = models.TextField(max_length=100, default='',null=True)
    pincode = models.TextField(max_length=50, default='',null=True)
    
    
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), 
        related_name='user_groups',
        blank=True, help_text=_('The groups this user belongs to. A user will '
                                'get all permissions granted to each of '
                                'his/her group.'))
    
    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_('user permissions'), blank=True,
        related_name='user_permissions',
        help_text='Specific permissions for this user.')
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __unicode__(self):
        return self.first_name + ' (' + self.email + ')'

    def has_perm(self, perm, obj=None):
        # Active superusers have all permissions.
        if self.is_active and self.is_admin:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    class Meta:
        permissions = (
            ("blog_moderator", "Can enable or disable blog posts"),
            ("blogger", "Can write blog posts"),            
        )

