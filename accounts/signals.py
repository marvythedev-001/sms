from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from school_structure.models import CurrentStateModel
from .models import *


@receiver(post_save, sender=StudentModel)
def student_profile_create(sender, instance, created, **kwargs):
    student = instance
    if created:
        query = CurrentStateModel.objects.first()
        student_profile = StudentProfileModel.objects.create(student=student, academic_session=query.academic_session, academic_term=query.academic_term, is_active=True)
        student_profile.save()
            