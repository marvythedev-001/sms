from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ParentModel)
admin.site.register(StudentModel)
admin.site.register(TeacherModel)
admin.site.register(StudentProfileModel)