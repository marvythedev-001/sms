from django.db import models
from django.db.models import Count

# Create your models here.

class AcademicSessionModel(models.Model):
    name = models.CharField(max_length=12)
    is_active = models.BooleanField()
    num_of_terms = models.IntegerField()
    # terms = models.ManyToManyField('AcademicTermModel')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name.upper()


class AcademicTermModel(models.Model):
    class TermName(models.TextChoices):
        FIRST = 'FIRST'
        SECOND = 'SECOND'
        THIRD = 'THIRD'
        FOURTH = 'FOURTH'
        
    name = models.CharField(max_length=15, choices=TermName.choices)
    academic_session = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE) # Need to look more at this line
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.academic_session} - {self.name.upper()}"
    
    def save(self, *args, **kwargs):
        if not self.duration:
            duration_in_days = (self.end_date - self.start_date).days
            self.duration = duration_in_days
        
        super(AcademicTermModel, self).save(*args, **kwargs)
    

class SchoolInfoModel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=60)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    

class CurrentStateModel(models.Model):
    academic_session = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTermModel, on_delete=models.CASCADE)
    

class StudentClassTypeModel(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name.upper()
    

class StudentClassArmModel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name.upper()
    
    
class StudentClassModel(models.Model):
    class ClassType(models.TextChoices):
        CRECHE = 'CRECHE'
        PRE_NURSERY = 'PRE-NURSERY'
        NURSERY = 'NURSERY'
        PRIMARY = 'PRIMARY'
        JUNIOR_SECONDARY = 'JUNIOR-SECONDARY'
        SENIOR_SECONDARY = 'SENIOR-SECONDARY'
        
    name = models.CharField(max_length=10)
    klass_type = models.CharField(choices=ClassType.choices, max_length=30)
    arm = models.ForeignKey(StudentClassArmModel, null=True, blank=True, on_delete=models.SET_NULL, related_name='arms')
    subjects_taught = models.ManyToManyField('academics.SubjectsModel')
    num_of_students = models.IntegerField(null=True, blank=True)
    # teacher = models.ForeignKey(TeacherModel, on_delete=models.RESTRICT)
    
    class Meta:
        unique_together = ['name', 'arm']
    
    def __str__(self):
        return self.name.upper()
    

    