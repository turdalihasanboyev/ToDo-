from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from uuid import uuid4
from datetime import datetime
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"


class ToDo(models.Model):
    """
    ToDo model
    """

    PRIORITY = (
        ('None', ('None')),
        ('Low', ('Low')),
        ('Medium', ('Medium')),
        ('High', ('High')),
    )

    title = models.CharField(max_length=250, unique=True)
    sub_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITY, default='None')
    deadline = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='todo_images', default='img/default-image.jpg')
    video = models.FileField(upload_to='todo_videos')
    is_done = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        date = datetime.today().strftime('%d-%m-%Y-%H-%M-%S')
        uuid = uuid4().hex[:8]
        self.slug = f"{slug}-{date}-{uuid}"
        super().save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('todo-detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = "To-Do Item"
        verbose_name_plural = "To-Do Items"