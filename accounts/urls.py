# from django.urls import path
# from . import views

# urlpatterns = [
#     path('student/', views.student_login, name='student_login'),
#     path('teacher/', views.teacher_login, name='teacher_login'),
#     path('admin-login/', views.admin_login, name='admin_login'),
#     # path('student-profile/', views.student_profile, name='student_profile'),
#     path('teacher-profile/', views.teacher_profile, name='teacher_profile'),
#     path('logout/', views.user_logout, name='logout'),
#     # path('dashboard/', views.event_views.student_dashboard, name='student_home'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/', views.student_login, name='student_login'),
    path('teacher/', views.teacher_login, name='teacher_login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    
    # UNCOMMENTED AND FIXED THESE:
    path('student-profile/', views.student_profile, name='student_profile'),
    path('dashboard/', views.student_dashboard, name='student_home'),
    
    path('teacher-profile/', views.teacher_profile, name='teacher_profile'),
    path('logout/', views.user_logout, name='logout'),
    
    
    # Add registration and feedback URLs if not in a separate file
    # path('events/register/<int:event_id>/', views.register_event, name='register_event'),
]