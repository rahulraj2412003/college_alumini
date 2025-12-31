from django.urls import path
from . import views

urlpatterns = [
    # --- STUDENT VIEW (The missing link) ---
    path('dashboard/', views.student_dashboard, name='student_home'),

    # --- ADMIN/TEACHER DASHBOARD ---
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # --- TEACHER MANAGEMENT ---
    path('manage-teachers/', views.manage_teachers, name='manage_teachers'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('teachers/edit/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
    
    # --- STUDENT MANAGEMENT ---
    path('manage-students/', views.manage_students, name='manage_students'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    
    # --- EVENT MANAGEMENT ---
    path('add-event/', views.add_event, name='add_event'),
    path('edit-event/<int:id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:id>/', views.delete_event, name='delete_event'),
    
    # --- REGISTRATIONS & FEEDBACK ---
    path('registrations/', views.registered_users, name='registered_users'),
    path('feedbacks/', views.view_feedback, name='view_feedback'),
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('feedback/<int:event_id>/', views.submit_feedback, name='submit_feedback'),
    
]