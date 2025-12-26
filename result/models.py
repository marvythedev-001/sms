from django.db import models

from accounts.models import StudentModel
from school_structure.models import AcademicSessionModel, AcademicTermModel, StudentClassArmModel, StudentClassModel

# Create your models here.

class ResultModel(models.Model):
    class Status(models.TextChoices):
        PASS = 'PASS'
        FAIL = 'FAIL'
        
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    report = models.JSONField()
    term = models.ForeignKey(AcademicTermModel, on_delete=models.CASCADE)
    academic_session = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClassModel, on_delete=models.CASCADE)
    student_class_arm = models.ForeignKey(StudentClassArmModel, on_delete=models.CASCADE)
    remark = models.CharField(max_length=50, null=True, blank=True)
    total_score = models.FloatField()
    average = models.IntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(choices=Status.choices, max_length=10, null=True, blank=True)
    position = models.CharField(max_length=10, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    

class ResultSettingsModel(models.Model):
    score_for_exams = models.IntegerField()
    score_for_tests = models.IntegerField()
    num_of_tests = models.IntegerField()
    