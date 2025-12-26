from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SubjectsModel)
admin.site.register(AssignmentModel)
admin.site.register(ExtraCurricularModel)
admin.site.register(AnnouncementModel)
admin.site.register(ExtraCurricularEnrollmentModel)