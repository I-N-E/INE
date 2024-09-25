from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class DataUser(models.Model):
    data_user = models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    member_user = models.BooleanField(default=False)
    image_profile = models.ImageField(upload_to='media/profile',null=True,blank=True)
    following = models.ManyToManyField(User,related_name='follow',blank=True)

    def count_follow(self):
        return self.following.count()

    def save(self , *args , **kwargs):
        super().save(*args , **kwargs)
        SIZE = 300, 300
        if self.image_profile:
            img = Image.open(self.image_profile.path)
            img.thumbnail(SIZE,Image.LANCZOS)
            img.save(self.image_profile.path) ; del SIZE

    def __str__(self) -> str:
        return f'{self.data_user}'

class Idea(models.Model):
    key_user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    idea_name = models.CharField(max_length=100,null=False,blank=False)
    idea_description = models.TextField(null=True,blank=True)
    idea_image = models.ImageField(upload_to='media/idea',null=True,blank=True)
    idea_datetime = models.DateTimeField(auto_now_add=True)
    idea_complete = models.DateTimeField(null=True,blank=True)
    idea_status = models.BooleanField(default=False)
    idea_start = models.BooleanField(default=False)
    idea_good = models.ManyToManyField(User,related_name='good',blank=True)
    
    def count_good(self):
        return self.idea_good.count()
    
    def save(self , *args , **kwargs):
        super().save(*args , **kwargs)
        SIZE = 720, 480
        if self.idea_image:
            img = Image.open(self.idea_image.path)
            img.thumbnail(SIZE,Image.LANCZOS)
            img.save(self.idea_image.path) ; del SIZE
    
    def __str__(self) -> str:
        return f'{self.key_user} : {self.id}'
    
class SubIdea(models.Model):
    key_idea = models.ForeignKey(Idea,on_delete=models.CASCADE,null=False,blank=False)
    sub_idea = models.CharField(max_length=155,null=False,blank=False)
    sub_body = models.TextField(null=False,blank=False)
    sub_image = models.ImageField(upload_to='media/sub_idea',null=True,blank=True)
    sub_file = models.FileField(upload_to='media/document',null=True,blank=True)
    sub_datetime = models.DateTimeField(auto_now_add=True)
    sub_complete = models.DateTimeField(null=True,blank=True)

    def save(self , *args , **kwargs):
        super().save(*args , **kwargs)
        SIZE = 720, 480
        if self.sub_image:
            img = Image.open(self.sub_image.path)
            img.thumbnail(SIZE,Image.LANCZOS)
            img.save(self.sub_image.path) ; del SIZE

    def __str__(self) -> str:
        return f'{self.key_idea}'
