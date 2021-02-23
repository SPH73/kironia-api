from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify

User = get_user_model()

def post_image_dir(instance, filename):
    return f"{instance.user}/{filename}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to=post_image_dir)
    content = models.TextField() # this content will be created in markdown and compiled to html on the frontend
    
    def __str__(self):
        return self.title

def pre_save_receiveer(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_receiveer, sender=Post)
