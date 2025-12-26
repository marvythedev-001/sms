from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AcademicSessionModel)
admin.site.register(AcademicTermModel)
admin.site.register(SchoolInfoModel)
admin.site.register(CurrentStateModel)
admin.site.register(StudentClassModel)
admin.site.register(StudentClassArmModel)
admin.site.register(StudentClassTypeModel)