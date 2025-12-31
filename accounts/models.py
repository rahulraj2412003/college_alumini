from django.db import models
from django.contrib.auth.models import User

DEPARTMENT_CHOICES = [
    ('MBA', 'Master of Business Administration'),
    ('BBA', 'Bachelor of Business Administration'),
    ('BCOM', 'Bachelor of Commerce'),
    ('BCA', 'Bachelor of Computer Applications'),
    ('MCOM', 'Master of Commerce'),
]

class Student(models.Model):
    register_number = models.CharField(max_length=20, unique=True,null=True, blank=True)
    department = models.CharField(max_length=5, choices=DEPARTMENT_CHOICES)
    passed_out_year = models.IntegerField()

    def __str__(self):
        return f"{self.register_number} - {self.department} ({self.passed_out_year})"


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher',
        null=True, blank=True
    )
    department = models.CharField(max_length=5, choices=DEPARTMENT_CHOICES)
    joining_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.username}) - {self.department}"
