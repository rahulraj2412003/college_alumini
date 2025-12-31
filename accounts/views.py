# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Student, Teacher

# Import what is in the events app models
from events.models import Event, EventRegistration, Feedback
# --- VIEWS ---

# 1. HOME VIEW
def home(request):
    return render(request, 'home.html')

# 2. STUDENT LOGIN
def student_login(request):
    if request.method == 'POST':
        reg_no = request.POST.get('register_number')
        dept = request.POST.get('department')
        year = request.POST.get('passed_out_year')

        student = Student.objects.filter(
            register_number=reg_no, 
            department=dept, 
            passed_out_year=year
        ).first()

        if student:
            request.session['user'] = 'student'
            request.session['id'] = student.id
            messages.success(request, "Welcome back!")
            return redirect('student_home') 
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            
    return render(request, 'student_login.html')

# 3. TEACHER LOGIN
def teacher_login(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        
        user = authenticate(request, username=u_name, password=p_word)
        
        if user is not None:
            if hasattr(user, 'teacher'):
                login(request, user)
                request.session['user'] = 'teacher'
                request.session['id'] = user.teacher.id
                messages.success(request, f"Welcome Prof. {user.username}")
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Not a Teacher account')
    return render(request, 'teacher_login.html')

# 4. ADMIN LOGIN
def admin_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'admin_login.html')

# 5. LOGOUT
def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect('home')

# 6. STUDENT DASHBOARD
def student_dashboard(request):
    if request.session.get('user') != 'student':
        return redirect('student_login')
    
    events = Event.objects.all()
    return render(request, 'dashboard.html', {'events': events})

# 7. STUDENT PROFILE
def student_profile(request):
    if request.session.get('user') != 'student':
        return redirect('student_login')
    
    student = get_object_or_404(Student, id=request.session['id'])
    
    # Correctly using EventRegistration from events.models
    registrations = EventRegistration.objects.filter(student=student).select_related('event')
    
    for reg in registrations:
        reg.feedback_given = Feedback.objects.filter(
            student=student, 
            event=reg.event
        ).exists()

    return render(request, 'student_profile.html', {
        'student': student,
        'registrations': registrations
    })

# 8. TEACHER PROFILE
def teacher_profile(request):
    if request.session.get('user') != 'teacher':
        return redirect('home')

    teacher = get_object_or_404(Teacher, id=request.session['id'])
    return render(request, 'teacher_profile.html', {'teacher': teacher})