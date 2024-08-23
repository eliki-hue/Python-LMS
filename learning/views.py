# learning/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .forms import SignUpForm
from .models import Course, Lesson, Progress


def signup(request):
    """
    Handle user signup.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # Optionally, set user.is_active=False for email verification
            # user.is_active = False
            # user.save()
            
            # Automatically log the user in after successful signup
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}! Your account was created successfully.')
                return redirect('course_list')
            else:
                messages.error(request, 'Authentication failed. Please try logging in.')
                return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Extract cleaned data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('course_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')


@login_required
def course_list(request):
    """
    Display the list of courses, grouped by levels.
    """
    courses_by_level = {
        'Beginner': Course.objects.filter(level='beginner'),
        'Intermediate': Course.objects.filter(level='intermediate'),
        'Advanced': Course.objects.filter(level='advanced'),
    }

    context = {
        'courses_by_level': courses_by_level,
    }

    return render(request, 'course_list.html', context)

@login_required
def course_detail(request, course_id):
    """
    Display details of a specific course along with its lessons.
    """
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')
    print("courses:{course} lesson:{lesson}")
    print(".......................................")
    context = {
        'course': course,
        'lessons': lessons,
    }
    
    return render(request, 'course_detail.html', context)


@login_required
def lesson_detail(request, course_id, lesson_id):
    """
    Display details of a specific lesson within a course.
    """
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    print("courses:{course} lesson:{lesson}")
    print(".......................................")

    # Track progress
    progress, created = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()


    context = {
        'course': course,
        'lesson': lesson,
    }
    
    return render(request, 'lesson_detail.html', context)