# learning/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Course, Progress, StudentLevelAccess
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from verify_email.email_handler import send_verification_email
# ckeditor imports
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.cache import cache


from .forms import SignUpForm
from .models import Course, Lesson, Progress, Profile

def home(request):
    return render(request, "home_page.html" )

def paths(request):
    return render(request, "paths.html" )

# ckeditor view to handle file import
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        image = request.FILES['upload']
        image_path = default_storage.save(f'uploads/{image.name}', ContentFile(image.read()))
        image_url = f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{image_path}"
        
        return JsonResponse({
            'url': image_url,  # CKEditor expects 'url' as the response key
            'uploaded': True
        })
    return JsonResponse({'uploaded': False}, status=400)


def signup(request):
    if request.method == 'POST':
        print('ggfhhhkhfjhfjhhhfhfdjhhfgghh')
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('saving the data')
            form.save()  # Save user to the database
            messages.success(request, 'Account created successfully!')
            print('saving the data')
            return redirect('login')  # Redirect to the login page
        else:
            print('not valid')
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def email_verified(request):
    return render(request, 'email_verified.html')

def email_verification(request, token):
    try:
        email_object = VerifyEmailToken.objects.get(token=token)
        user = email_object.user
        user.is_active = True  # Activate the user's account
        user.save()
        email_object.delete()  # Delete the token once used
        login(request, user)  # Optionally log the user in
        return redirect('email_verified')  # Redirect to a success page
    except VerifyEmailToken.DoesNotExist:
        return redirect('email_verification_failed')  # Redirect to a failure page

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
                return redirect('paths')
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
def course_lessons(request, course_title):
    # Get the course by title
    course = get_object_or_404(Course, title__iexact=course_title)
    # Fetch all lessons for the course
    lessons = course.lessons.all()  # Related name "lessons" is used here
    context = {
        'course': course,
        'lessons': lessons,
    }
    
    return render(request, 'lesson_detail.html', context)






@login_required
# @cache_page(60)  # Cache for 1 minute
def lesson_detail(request, course_id, lesson_id):
     # Get the course and all lessons in the correct order
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')

    # Fetch current lesson
    lesson = get_object_or_404(lessons, id=lesson_id)

    # Preload progress for all lessons in the course
    user_progress = Progress.objects.filter(user=request.user, lesson__course=course).select_related('lesson')
    progress_dict = {progress.lesson.id: progress.completed for progress in user_progress}

    # Handle "Mark as Done"
    current_progress, _ = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    if request.method == 'POST' and 'mark_done' in request.POST:
        if not current_progress.completed:
            current_progress.completed = True
            current_progress.save()
        return redirect('lesson_detail', course_id=course_id, lesson_id=lesson_id)

    # Calculate progress percentage
    total_lessons = lessons.count()
    completed_count = sum(progress_dict.values())
    progress_percentage = (completed_count / total_lessons) * 100 if total_lessons > 0 else 0

    # Determine locking for lessons
    previous_completed = True  # Assume the first lesson is unlocked
    for lesson_item in lessons:
        lesson_item.is_locked = not previous_completed
        previous_completed = progress_dict.get(lesson_item.id, False)

    # Determine the previous and next lessons
    lesson_index = list(lessons).index(lesson)
    previous_lesson = lessons[lesson_index - 1] if lesson_index > 0 else None
    next_lesson = lessons[lesson_index + 1] if lesson_index < len(lessons) - 1 else None
    next_lesson_is_locked = next_lesson and next_lesson.is_locked

    return render(request, 'lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
        'completed_count':completed_count,
        'progress_percentage': progress_percentage,
        'is_completed': current_progress.completed,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'next_lesson_is_locked': next_lesson_is_locked,
    })
    
def mark_lesson_done(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    user = request.user

    # Get or create Progress entry for the current lesson
    progress, created = Progress.objects.get_or_create(user=user, lesson=lesson)

    if not progress.completed:
        # Mark current lesson as completed
        progress.completed = True
        progress.completed_at = now()
        progress.save()

        # Unlock the next lesson (if it exists)
        next_lesson = Lesson.objects.filter(course=lesson.course, order=lesson.order + 1).first()
        if next_lesson:
            Progress.objects.get_or_create(user=user, lesson=next_lesson)

    return redirect('lesson_detail', lesson_id=lesson.id)

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:  # Ensure only admin users can access this view
        return redirect('course_list')
    
    if request.method == 'POST':
        # Handle the form submission to update access levels
        user_id = request.POST.get('user_id')
        level = request.POST.get('level')

        user = User.objects.get(id=user_id)
        StudentLevelAccess.objects.update_or_create(user=user, level=level)

        return redirect('admin_dashboard')

    # Load all students and their access levels
    students = User.objects.all()
    access_levels = StudentLevelAccess.objects.all()

    level_choices = Course.LEVEL_CHOICES

    # Aggregate student progress
    courses = Course.objects.all()
    progress_data = {}

    for student in students:
        student_progress = {}
        for course in courses:
            lessons = course.lessons.all()
            completed_lessons = Progress.objects.filter(user=student, lesson__in=lessons, completed=True).count()
            total_lessons = lessons.count()
            student_progress[course] = {
                'completed_lessons': completed_lessons,
                'total_lessons': total_lessons,
                'percentage': (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0,
            }
        progress_data[student] = student_progress

    context = {
        'students': students,
        'level_choices': level_choices,
        'progress_data': progress_data,
        'access_levels': access_levels,
    }

    return render(request, 'admin_dashboard.html', context)