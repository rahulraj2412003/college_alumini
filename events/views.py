from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import Student, Teacher
from .models import Event, EventRegistration, Feedback

# --- SECURITY HELPERS ---
def is_admin(user):
    return user.is_superuser

# --- DASHBOARDS ---


@login_required
def admin_dashboard(request):
    user = request.user
    
    # GLOBAL COUNTS - No filtering, so they won't be 0
    events = Event.objects.all().order_by('-date')
    student_count = Student.objects.count()
    reg_count = EventRegistration.objects.count()
    feedback_count = Feedback.objects.count()
    teacher_count = Teacher.objects.count()

    # Role identification for the sidebar
    if user.is_superuser:
        user_role = "System Administrator"
    else:
        try:
            profile = Teacher.objects.get(user=user)
            user_role = f"Faculty - {profile.department}"
        except Teacher.DoesNotExist:
            user_role = "Faculty Member"

    context = {
        'events': events,
        'student_count': student_count,
        'reg_count': reg_count,
        'feedback_count': feedback_count,
        'teacher_count': teacher_count,
        'user_role': user_role,
    }
    return render(request, 'admin_dashboard.html', context)

def student_dashboard(request):
    """Dashboard for Students using session-based login."""
    if not request.session.get('user') == 'student':
        return redirect('home')
    events = Event.objects.all().order_by('-date')
    return render(request, 'dashboard.html', {'events': events})

# --- EVENT MANAGEMENT (Admin & Teacher) ---
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Event
from datetime import datetime

@login_required
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        image = request.FILES.get('image')

        # Handle timezone warning
        naive_date = datetime.strptime(date_str, '%Y-%m-%d')
        aware_date = timezone.make_aware(naive_date)

        Event.objects.create(
            title=title,
            description=description,
            date=aware_date,
            image=image
        )

        # Success message
        messages.success(request, f'Event "{title}" published successfully!')
        
        # REDIRECT TO THE CORRECT NAME FROM YOUR URLS.PY
        return redirect('admin_dashboard') 

    return render(request, 'add_event.html')

@login_required
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.department = request.POST.get('department')
        
        # Only update the image if a new one was uploaded
        if 'image' in request.FILES:
            event.image = request.FILES['image']
            
        event.save()
        return redirect('admin_dashboard')
    return render(request, 'edit_event.html', {'event': event})

@login_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('admin_dashboard')

# --- STUDENT MANAGEMENT (Admin & Teacher) ---
@login_required
def manage_students(request):
    students = Student.objects.all().order_by('-passed_out_year')

    reg_no = request.GET.get('search')
    dept = request.GET.get('department')
    year = request.GET.get('year')

    if reg_no:
        students = students.filter(register_number__icontains=reg_no)
    if dept:
        students = students.filter(department=dept)
    if year:
        students = students.filter(passed_out_year=year)

    return render(request, 'manage_students.html', {'students': students})
@login_required
def add_student(request):
    if request.method == 'POST':
        Student.objects.create(
            register_number=request.POST['register_number'],
            department=request.POST['department'],
            passed_out_year=request.POST['passed_out_year']
        )
        return redirect('manage_students')
    return render(request, 'add_student.html')

@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.register_number = request.POST['register_number']
        student.department = request.POST['department']
        student.passed_out_year = request.POST['passed_out_year']
        student.save()
        return redirect('manage_students')
    return render(request, 'edit_student.html', {'student': student})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('manage_students')

# --- TEACHER MANAGEMENT (ADMIN ONLY) ---

from django.db.models import Q
from accounts.models import Teacher

@user_passes_test(is_admin)
def manage_teachers(request):
    # Start with all teachers
    teachers = Teacher.objects.all().select_related('user')

    # Get search and filter parameters
    search_query = request.GET.get('search')
    dept_filter = request.GET.get('department')

    # Apply Text Search (Name, Username, or Email)
    if search_query:
        teachers = teachers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )

    # Apply Department Filter
    if dept_filter:
        teachers = teachers.filter(department=dept_filter)

    return render(request, 'manage_teachers.html', {'teachers': teachers})

@user_passes_test(is_admin)
def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher.user.delete() 
    return redirect('manage_teachers')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    user = teacher.user

    if request.method == 'POST':
        # Update User model
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('email')
        user.save()

        # Update Teacher model - Replace employee_id with department
        teacher.department = request.POST.get('department')
        teacher.save()

        return redirect('manage_teachers')

    return render(request, 'edit_teacher.html', {'teacher': teacher})

# --- REGISTRATIONS & FEEDBACK (Shared) ---

# accounts/views.py (or wherever registered_users is defined)
from events.models import Event, EventRegistration

def registered_users(request):
    # Get all registrations initially
    registrations = EventRegistration.objects.all().select_related('student', 'event')
    
    # Get filter values from GET request
    event_id = request.GET.get('event')
    dept = request.GET.get('department')

    # Apply filters if values exist
    if event_id:
        registrations = registrations.filter(event_id=event_id)
    
    if dept:
        registrations = registrations.filter(student__department=dept)

    # We need all events for the dropdown list
    all_events = Event.objects.all()

    context = {
        'registrations': registrations,
        'all_events': all_events,
        'user_role': request.session.get('user', 'Admin')
    }
    return render(request, 'registered_users.html', context)

@login_required
def view_feedback(request):
    # FIXED: Fetch all feedback
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'view_feedback.html', {'feedbacks': feedbacks})
# --- STUDENT ACTIONS (Session Based) ---

def register_event(request, event_id):
    if request.session.get('user') != 'student':
        messages.error(request, "Please login as a student to register.")
        return redirect('student_login')

    event = get_object_or_404(Event, id=event_id)
    student = get_object_or_404(Student, id=request.session['id'])

    if request.method == 'POST':
        # This part happens when they click "Confirm" on the registration page
        if not EventRegistration.objects.filter(student=student, event=event).exists():
            EventRegistration.objects.create(student=student, event=event)
            messages.success(request, f"Successfully registered for {event.title}")
        return redirect('student_profile')

    # This part happens when they click "REGISTER NOW" on the dashboard
    return render(request, 'event_register.html', {'event': event})


from django.http import JsonResponse

def submit_feedback(request, event_id):
    if request.session.get('user') != 'student':
        return redirect('home')
        
    event = get_object_or_404(Event, id=event_id)
    student = get_object_or_404(Student, id=request.session['id'])
    
    if request.method == 'POST':
        Feedback.objects.update_or_create(
            student=student, 
            event=event,
            defaults={
                'rating': request.POST.get('rating'), 
                'comment': request.POST.get('comment')
            }
        )
        # If AJAX, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
            
        return redirect('student_profile')
        
    return render(request, 'submit_feedback.html', {'event': event})

from django.contrib.auth.models import User
from accounts.models import Teacher

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

@login_required
def add_teacher(request):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied.")
        return redirect('admin_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        # Prevent duplicate usernames (Multiple users fix)
        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered.")
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
            )
            Teacher.objects.create(
                user=user,
                department=request.POST.get('department'),
                joining_year=request.POST.get('joining_year')
            )
            messages.success(request, "Faculty added successfully!")
            return redirect('manage_teachers')

    return render(request, 'add_teacher.html', {'departments': Teacher._meta.get_field('department').choices})