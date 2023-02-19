from datetime import datetime
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.
class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user= models.IntegerField()
    first_name= models.CharField(max_length=50, blank=True)
    last_name= models.CharField(max_length= 50, blank=True)
    bio= models.TextField(blank=True)
    profileimg= models.ImageField(upload_to='profile_images', default='default-profile-picture.png')
    location= models.CharField(max_length=100, blank=True)
    work= models.CharField(max_length=100, blank=True)
    class relationship_status(models.IntegerChoices):
        NA=0, 
        Single=1
        In_a_relationship=2
        Married=3
        Engaged=4

    relationship= models.IntegerField(choices=relationship_status.choices, default=0)
    relationship_to_word={0:'NA', 1:'Single', 2:'In a Relationship', 3:'Married', 4:'Engaged'}
    display_relationship=relationship_to_word.get(relationship)

    def __str__(self) -> str:
        return self.user.username

class post(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    user= models.CharField(max_length=100)
    image= models.ImageField(upload_to='post_images')
    caption= models.TextField()
    created_at= models.DateTimeField(default=datetime.now)
    likes= models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user

class like(models.Model):

    post_id=models.CharField(max_length=500)
    username= models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.username

class follower(models.Model):
    follower= models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user


