from django.db import models

from academics.models import SubjectsModel
from accounts.models import TeacherModel

# Create your models here.

class ClassSessionModel(models.Model):
    class ClassType(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL'
        GROUP = 'GROUP'
        WHOLE_CLASS = 'WHOLE_CLASS'
        
    subject_to_be_taught = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)
    duration = models.IntegerField()
    teacher = models.ManyToManyField(TeacherModel)
    details = models.TextField()
    start_date = models.DateField()
    start_time = models.TimeField()
    is_ended = models.BooleanField()
    session_type = models.CharField(max_length=20, choices=ClassType.choices)