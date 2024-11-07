from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class ToDo(models.Model):
    PRIORITY = (
        ('None', ('None')),
        ('Low', ('Low')),
        ('Medium', ('Medium')),
        ('High', ('High')),
    )
    title = models.CharField(max_length=250, unique=True)
    sub_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True, db_index=True, max_length=250)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITY, default=('None', ('None')))
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
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('todo-detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = "To-Do Item"
        verbose_name_plural = "To-Do Items"