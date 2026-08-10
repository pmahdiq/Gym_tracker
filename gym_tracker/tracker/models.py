from django.db import models
class User(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.PositiveIntegerField(null=True)
    weight = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    last_login = models.DateTimeField(null=True)

class Training_Program(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class Exercise(models.Model):
    training_program = models.ForeignKey(Training_Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    reps = models.PositiveIntegerField(default=0)
    sets = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)

class Training_Session(models.Model):
    training_program = models.ForeignKey(Training_Program, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
