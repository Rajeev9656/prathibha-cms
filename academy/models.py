from django.db import models
from datetime import date

batch_choices = [
    ('Day Batch', 'Day Batch'),
    ('Sunday Batch', 'Sunday Batch'),
    ('Overseer (Sunday Only)', 'Overseer (Sunday Only)'),
    ('Night Batch', 'Night Batch'),
]

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    
    # New fields
    batch = models.CharField(max_length=50, choices=batch_choices, default='Day Batch')
    fees_paid = models.BooleanField(default=False)
    date_joined = models.DateField(default=date.today)
    
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class ClassSchedule(models.Model):
    batch = models.CharField(max_length=50, choices=batch_choices)
    topic = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    room_or_link = models.CharField(max_length=200, blank=True, null=True)

class Exam(models.Model):
    subject = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()