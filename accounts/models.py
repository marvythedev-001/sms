from django.db import models
from django.contrib.auth.models import User
from academics.models import SubjectsModel
from school_structure.models import AcademicSessionModel, AcademicTermModel, StudentClassArmModel, StudentClassModel

# Create your models here.
class Role(models.TextChoices):
        ADMIN = 'ADMIN'
        TEACHER = 'TEACHER'
        PARENT = 'PARENT'
        STUDENT = 'STUDENT'
        
class Gender(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
        

class StudentModel(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE'
        SUSPENDED = 'SUSPENDED'
        GRADUATED = 'GRADUATED'
        
    class Religion(models.TextChoices):
        CHRISTIANITY = 'CHRISTIANITY'
        ISLAM = 'ISLAM'
        OTHERS = 'OTHERS'
    
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    email = models.EmailField(unique=True)
    admission_number = models.CharField(max_length=25, unique=True)
    date_of_birth = models.DateField()
    is_disabled = models.BooleanField(default=False)
    disabilities = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default='ACTIVE')
    current_class = models.ForeignKey(StudentClassModel, on_delete=models.RESTRICT, related_name="students")
    current_class_arm = models.ForeignKey(StudentClassArmModel, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)
    registration_date = models.DateTimeField(auto_now_add=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    religion = models.CharField(choices=Religion.choices, max_length=15)
    photo = models.ImageField(upload_to='./student-img', null=True, blank=True)
    
    class Meta:
        unique_together = ['first_name', 'middle_name', 'last_name', 'email', 'admission_number']

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}" if self.middle_name else f"{self.first_name} {self.last_name}"
    

class StudentProfileModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    academic_session = models.ForeignKey(AcademicSessionModel, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTermModel, on_delete=models.CASCADE)
    is_active = models.BooleanField()
    

class ParentModel(models.Model):
    class Title(models.Choices):
        DR = 'DR'
        MR = 'MR.'
        MRS = 'MRS.'
        PROF = 'PROF.'
        
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    reg_number = models.CharField(max_length=25, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_of_children = models.IntegerField()
    occupation = models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=10, choices=Title.choices)
    children = models.ManyToManyField(StudentModel)
    role = models.CharField(max_length=20, choices=Role.choices)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['first_name', 'middle_name', 'last_name', 'email', 'phone']

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}" if self.middle_name else f"{self.first_name} {self.last_name}"
    

class TeacherModel(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE'
        LEAVE = 'LEAVE'
        SUSPENDED = 'SUSPENDED'
        
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    staff_number = models.CharField(max_length=25, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects_taught = models.ManyToManyField(SubjectsModel)
    classes_taught = models.ManyToManyField(StudentClassModel, related_name="classes")
    assigned_class = models.ForeignKey(StudentClassModel, on_delete=models.RESTRICT)
    role = models.CharField(max_length=20, choices=Role.choices)
    registration_date = models.DateTimeField(auto_now_add=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['first_name', 'middle_name', 'last_name', 'email', 'phone']

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}" if self.middle_name else f"{self.first_name} {self.last_name}"
