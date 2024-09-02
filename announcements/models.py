from django.db import models
import datetime
# Create your models here.

class Student(models.Model):
    roll_no = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    cgpa = models.FloatField(max_length=100)
    dept_name = models.CharField(max_length=100)
    year = models.IntegerField()
    pic=models.ImageField(upload_to="media",default="profile.png",null=True,blank=True)

    def __str__(self):
        return self.roll_no

class Clubs(models.Model):
    club_id = models.CharField(max_length=6,primary_key=True)
    club_name=models.CharField(max_length=50)
    club_description=models.TextField()
    def __str__(self):
        return self.club_name

class Events(models.Model):
    event_id = models.AutoField(auto_created=True,primary_key=True)
    club_id = models.CharField(max_length=6)
    club_name=models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=100)
    task=models.TextField(default='No task')
    status=models.CharField(max_length=20,default='in progress')
    poster=models.ImageField(upload_to="media",default="events.png",null=True,blank=True)
    date=models.DateField(default=datetime.date.today)
    time=models.CharField(max_length=20,default="5:00 pm-6:00 pm")
    venue=models.CharField(max_length=30,default="SRK-221")
    def __str__(self):
        return self.name
    

class club_members(models.Model):
    club_id = models.CharField(max_length=6)
    stu_id = models.IntegerField()
    position=models.CharField(max_length=20,default="Executive member")

class event_students(models.Model):
    event_id=models.IntegerField()
    stu_id=models.IntegerField()

class events_pics(models.Model):
    club_id=models.CharField(max_length=6)
    event_name=models.CharField(max_length=100)
    pic=models.ImageField(upload_to="media",null=True,blank=True)
