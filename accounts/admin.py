# accounts/admin.py
from django.contrib import admin
from .models import Student, Teacher

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('register_number', 'department', 'passed_out_year')
    list_filter = ('department', 'passed_out_year') # Adds a filter sidebar

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'joining_year', 'department')
    list_filter = ('department',)