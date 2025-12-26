from django.db import models
from django.contrib.auth.models import User
from school_structure.models import AcademicSessionModel, AcademicTermModel, StudentClassModel

class SubjectsModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    sub_code = models.CharField(max_length=10, unique=True)
    num_of_students = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pass_mark = models.IntegerField()
    
    class Meta:
        unique_together = ['name', 'sub_code']
        
    def __str__(self):
        return f"{self.name.upper()} - {self.sub_code.upper()}"
    
    
class AssignmentModel(models.Model):
    subject = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)
    num_of_questions = models.IntegerField()
    question = models.TextField()
    submission_date = models.DateField()
    creation_date = models.DateField()
    teacher = models.ForeignKey('accounts.TeacherModel', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    classes_included = models.ManyToManyField(StudentClassModel)
    is_valid = models.BooleanField()
    academic_session = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTermModel, on_delete=models.CASCADE)
    
    
class AnnouncementModel(models.Model):
    message= models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creation_time = models.TimeField()
    recipients = models.CharField(max_length=40, null=True, blank=True)
    academic_session = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTermModel, on_delete=models.CASCADE)
    
    
class ExtraCurricularModel(models.Model):
    class PaymentStructure(models.TextChoices):
        TERMLY = 'TERMLY'
        SESSIONLY = 'SESSIONLY'
    name = models.CharField(max_length=100, unique=True)
    regulations = models.TextField()
    description = models.CharField(max_length=170)
    person_in_charge = models.CharField(max_length=40)
    is_free = models.BooleanField()
    amount = models.IntegerField()
    payment_structure = models.CharField(PaymentStructure.choices, max_length=20)
    
    class Meta:
        unique_together = ['name']
        
    def __str__(self):
        return self.name.upper()
    

class ExtraCurricularEnrollmentModel(models.Model):
    student = models.ForeignKey('accounts.StudentModel', on_delete=models.CASCADE)
    activity = models.ForeignKey(ExtraCurricularModel, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    enrollment_date_time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)
    academic_session = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTermModel, on_delete=models.CASCADE)
    