from django.db import models
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
import mutagen
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import calendar
import json

# Create your models here.

def validate_sample_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.wav']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Vous ne pouvez importer que des fichiers wav.')

def validate_project_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.json']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Vous ne pouvez importer que des fichiers .json')


def user_directory_path(instance, filename):
    return 'samples/user_{0}/{1}'.format(instance.user.id, filename)

def user_directory_path2(instance, filename):
    return 'samples/user_{0}/{1}'.format(instance.user.id, filename)

def user_directory_path_project(instance, filename):
    return 'samples/user_{0}/projects/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=11)
    image = models.FileField(upload_to='icons/tags', null=True, blank=True)

    def __str__(self):
        return self.name

class Background(models.Model):
    image = models.ImageField(upload_to='backgrounds/', null=True)

    def __str__(self):
        return str(self.id)

class Project(models.Model):
    created_date = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    typeOfMusic = models.CharField(max_length=10)
    file = models.FileField(upload_to=user_directory_path_project, validators=[validate_project_extension])

    def __str__(self):
        return self.name
    
    def month_name(self):
        return calendar.month_name[self.created_date.month][0:3]
    
    def fileName(self):
        name = str(self.file).split("/")
        name = name[-1]
        return name
    
    def nbOfChannels(self):
        data = self.file.read()
        dataJson = json.loads(data)
        self.file.close()
        return len(dataJson["channels"])
    
    def nbOfTime(self):
        data = self.file.read()
        dataJson = json.loads(data)
        self.file.close()
        return dataJson["nbTemps"]
    
    def bpm(self):
        data = self.file.read()
        dataJson = json.loads(data)
        self.file.close()
        return dataJson["bpm"]

class Sample(models.Model):
    created_date = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    users = models.ManyToManyField(User, related_name="user")
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to=user_directory_path, validators=[validate_sample_extension])
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    isRecent = models.BooleanField(default=True)
    isMacro = models.BooleanField(default=False)
    isPublic = models.BooleanField(default=False, verbose_name="Public ? ")
    background = models.ForeignKey(on_delete=models.SET_NULL,to=Background,null=True)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        now = timezone.now()
        if now - datetime.timedelta(days=1) < self.created_date <= now:
            self.isRecent = True
        else:
            self.isRecent = False
            
    def get_bits_per_sample(self):
        return mutagen.File(self.file).info.bits_per_sample

    def isItMacro(self):
        if mutagen.File(self.file).info.length > 2 :
            self.isMacro = True
        else:
            self.isMacro = False
    
    def get_bgId_or_bg(self):
        if not self.background:
            bgId = random.randint(1,16)
            return bgId
        else:
            return self.background

class Collection(models.Model):
    created_date = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authorCollection")
    users = models.ManyToManyField(User, related_name="userCollection")
    name = models.CharField(max_length=200)
    description = models.TextField()
    samples = models.ManyToManyField(Sample)
    isRecent=models.BooleanField(default=True)
    isPublic = models.BooleanField(default=False, verbose_name="Public Collection ? ")
    image = models.ImageField(upload_to="collections/", null=True, blank=True)

    def was_published_recently(self):
        now = timezone.now()
        if now - datetime.timedelta(days=1) < self.pub_date <= now:
            self.isRecent = True
        else:
            self.isRecent = False

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    favMusicSoftware = models.CharField(max_length=30, blank=True)
    musicStyle = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True, default='no-profile-pic.png')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
        
    def __str__(self):
        return self.user.username

class Kit(models.Model):
    sampleList = models.ManyToManyField(Sample)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)