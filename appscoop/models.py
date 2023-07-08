from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings
# from datetime import datetime

# Create your models here.
class User(AbstractUser):
    classname=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100,blank=True)
    profile_img=models.ImageField(upload_to='profile_images/', default=settings.STATIC_URL + 'images/default.jpg')
    bio=models.CharField(max_length=100,default="None")
    otp=models.CharField(max_length=4,default='a')


class publics(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    imagename=models.CharField(max_length=50)
    imagecaption=models.CharField(max_length=200,default='')
    image=models.ImageField(upload_to='images/')
    date=models.DateField(auto_now_add=True)

class college(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    imagename=models.CharField(max_length=50)
    imagecaption=models.CharField(max_length=200,default='')
    image=models.ImageField(upload_to='images/')
    likes=models.ManyToManyField(User,related_name='liked_post',blank=True)
    date=models.DateField(auto_now_add=True)

class Post_req(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    image=models.ImageField(upload_to='req_images/')
    imagename=models.CharField(max_length=50)
    imagecaption=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200,default='pending')
    # deletion_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.student.first_name+' '+self.student.username
    
    # def delete_after_period(self):
    #     if self.deletion_date and self.deletion_date <= datetime.now():
    #         self.delete()
    
class Inbox(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    date=models.DateField(auto_now_add=True)
    title=models.CharField(max_length=20,default="")
    message=models.CharField(max_length=500)

    def __str__(self):
        return self.sender.first_name





