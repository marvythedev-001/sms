from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@receiver(post_save, sender=StudentClassModel)
def get_number_of_students(sender, instance, created, **kwargs):
    student_class = instance
    if created:
        students_in_class = student_class.students.count()
        student_class.num_of_students = students_in_class
        student_class.save()
            