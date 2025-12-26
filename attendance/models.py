from django.db import models
from django.contrib.auth.models import User

from academics.models import SubjectsModel
from accounts.models import TeacherModel
from school_structure.models import AcademicSessionModel, AcademicTermModel, StudentClassArmModel, StudentClassModel

# Create your models here.

class ClassesAttendanceModel(models.Model):
    subject = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)
    class_room = models.ForeignKey(StudentClassModel,on_delete=models.CASCADE)
    arm = models.ForeignKey(StudentClassArmModel, on_delete=models.CASCADE)
    date_taken = models.DateField()
    time_taken = models.TimeField()
    teacher = models.ForeignKey(TeacherModel, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTermModel, on_delete=models.CASCADE)
    report = models.JSONField()
    
    class Meta:
        unique_together = ['subject', 'class_room', 'arm', 'date_taken']
    
    
class DayAttendanceModel(models.Model):
    class_room = models.ForeignKey(StudentClassModel,on_delete=models.CASCADE)
    arm = models.ForeignKey(StudentClassArmModel, on_delete=models.CASCADE)
    date_taken = models.DateField()
    time_taken = models.TimeField()
    academic_year = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTermModel, on_delete=models.CASCADE)
    report = models.JSONField()
    
    class Meta:
        unique_together = ['class_room', 'arm', 'date_taken']