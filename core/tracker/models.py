from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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
    
    def __str__(self):
            return self.title
class Training_Session(models.Model):
    training_program = models.ForeignKey(Training_Program, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def duration_display(self):
        if not self.completed_at:
            return None
        total_seconds = int((self.completed_at - self.started_at).total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


    def __str__(self):
            return self.training_program.title

class Training_Session_Exercise(models.Model):
    training_session = models.ForeignKey(Training_Session, on_delete=models.CASCADE, related_name='exercise_logs')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    reps = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return f"{self.title} — {self.training_session}"