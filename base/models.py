from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.timesince import timesince
import os 
import datetime

class CustomUser(AbstractUser):
    email = models.EmailField()
    profile_photo = models.ImageField(upload_to='images', default='images/default_user_image.jpg')
    is_free_trial = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    expiry_free_trial = models.DateTimeField(default=datetime.datetime.now)
    finished_free_trial = models.BooleanField(default = False)
    # def set_avatar(self):
    #     if not self.profile_photo:
    #         self.profile_photo = os.path.join(settings.MEDIA_URL,'images/default_image.jpg')

class Classrooms(models.Model):
    classroom_name=models.CharField(max_length=100)
    section = models.CharField(max_length=100,default='Third Year')
    class_code = models.CharField(max_length = 10,default='0000000')

    def __str__(self):
        return self.classroom_name

class Students(models.Model): 
    student_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    # student_uid = models.AutoField(primary_key= True,default = 1)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)

class Teachers(models.Model):
    teacher_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    # teacher_uid = models.AutoField(primary_key= True,default = 1)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)

class Assignments(models.Model):
    assignment_name=models.CharField(max_length=50)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)
    due_date=models.DateField()
    due_time=models.TimeField(default=datetime.time(10,10))
    posted_date=models.DateField(auto_now_add=True)
    instructions=models.TextField()
    total_marks=models.IntegerField(default=100)
    instruction_file = models.FileField(upload_to='documents')

    def __str__(self):
        return self.assignment_name

class Submissions(models.Model):
    assignment_id=models.ForeignKey(Assignments,on_delete=models.CASCADE)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    submitted_date=models.DateField(auto_now_add=True)
    submitted_time=models.TimeField(auto_now_add=True)
    submitted_on_time=models.BooleanField(default=True)
    marks_alloted=models.IntegerField(default=0)
    submission_file = models.FileField(upload_to='documents')


class Appointment(models.Model):
    appointmentId = models.AutoField(primary_key= True)
    # student_id=models.ForeignKey(Students, on_delete=models.CASCADE)
    teacher_id=models.ForeignKey(Teachers, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=250, default="None")
    lastname = models.CharField(max_length=250, default="None")
    appointment_link = models.CharField(max_length=250, default="None")
    date = models.DateField()
    timing=models.TimeField()
    isCancelled=models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    reasonOfDisapproval = models.CharField(max_length=250, default="None")
    start_link = models.CharField(max_length=3000, default="None")
    zoom_id = models.CharField(max_length=20, default="None")
    zoom_password = models.CharField(max_length=20, default="None")
    #appointmentDate=models.DateField(auto_now=True)
    #description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    is_disapproved = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)
    user_email = models.CharField(max_length=50, default="None")

class Announcements(models.Model):
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)
    instructions=models.TextField()
    instruction_file = models.FileField(upload_to='documents', blank = True, null= True)
    posted_date=models.DateField(auto_now_add=True)

class Videos(models.Model):
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)
    video=models.FileField(upload_to='documents', blank = True, null = True)
    video_name=models.CharField(max_length=50)
    description=models.TextField()


# def __str__(self):
#         return self.classroom_id.classroom_name