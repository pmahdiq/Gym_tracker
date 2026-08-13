from django.db import models
from django.contrib.auth.models import User
class Training_Program(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.title
    

class Exercise(models.Model):
    training_program = models.ForeignKey(Training_Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    reps = models.PositiveIntegerField(default=0)
    sets = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
            return self.title
class Training_Session(models.Model):
    training_program = models.ForeignKey(Training_Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.title