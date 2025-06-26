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
from markdown import markdown
import requests
# import openai
import os
import httpx
# from openai import OpenAI
from django.views.decorators.http import require_POST
GROQ_API_KEY = settings.GROQ_API_KEY
GROQ_API_URL = settings.GROQ_API_URL
GROQ_MODEL = settings.GROQ_API_URL  # Use any preferred model from Groq list

# openai.api_key = settings.OPENAI_API_KEY
# client = OpenAI()
from .forms import SignUpForm
from .models import Course, Lesson, Progress, Profile, ChatLog

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
    # course = get_object_or_404(Course, title__iexact=course_title)
    course = get_object_or_404(Course, slug=course_title)
    # Fetch all lessons for the course
    lessons = course.lessons.all()  # Related name "lessons" is used here
    context = {
        'course': course,
        'lessons': lessons,
    }
    
    return render(request, 'lesson_detail.html', context)



conversation_memory = {}  # For dev only. Replace with DB in production.

@require_POST
@csrf_exempt
def ai_chat_view(request):
    from django.utils.datastructures import MultiValueDictKeyError

    try:
        message = request.POST['message']
        lesson_title = request.POST.get('lesson_title', '')
        lesson_content = request.POST.get('lesson_content', '')

        # Get or initialize chat history from session
        chat_history = request.session.get('chat_history', [])

        # Add user message to chat history
        chat_history.append({
            "role": "user",
            "content": f"You are an AI programming tutor for kids aged 10 to 17. Be friendly and explain clearly.\nLesson: {lesson_title} - {lesson_content}\n\nStudent: {message}"
        })

        # Prepare API request
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "llama3-8b-8192",
            "messages": chat_history,
            "temperature": 0.7
        }

        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
        res.raise_for_status()
        response_data = res.json()

        # Get AI message and add to history
        ai_markdown = response_data['choices'][0]['message']['content']
        chat_history.append({
            "role": "assistant",
            "content": ai_markdown
        })

        # Save back to session
        request.session['chat_history'] = chat_history

        # Convert Markdown to HTML
        ai_html = markdown(ai_markdown, extensions=['fenced_code'])

        return JsonResponse({"response": ai_html})

    except MultiValueDictKeyError as e:
        return JsonResponse({"error": f"Missing parameter: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
# @csrf_exempt
# @require_POST
# def ai_chat_view(request):
#     if request.method == "POST":
#         message = request.POST.get("message")
#         lesson_title = request.POST.get("lesson_title", "")
#         lesson_content = Lesson.objects.get(title=lesson_title).content
#         prompt = f"You are an AI programming tutor for kids aged 10 to 17. Explain clearly and use appropriate examples depending on the lesson when needed.\n Teachers lesson content for current lesson \nLesson: {lesson_title} is:{lesson_content}\n\nStudent question: {message}"
#         # prompt = f"You are an AI programming tutor for kids aged 10 to 17. Explain clearly and use Python examples when needed.\nLesson: {lesson_title}\nQuestion: {message}"

#         try:
#             response = requests.post(
#                 "https://api.groq.com/openai/v1/chat/completions",
#                 headers={
#                     "Authorization": f"Bearer {GROQ_API_KEY}",
#                     "Content-Type": "application/json"
#                 },
#                 json={
#                     "model": "llama3-8b-8192",
#                     "messages": [{"role": "user", "content": prompt}],
#                     "temperature": 0.6
#                 }
#             )

#             response_data = response.json()

#             ai_markdown = response_data['choices'][0]['message']['content']
#             ai_html = markdown(ai_markdown)  # ← Convert Markdown to HTML
#             ai_html = markdown(ai_markdown, extensions=['fenced_code'])
#             return JsonResponse({"response": ai_html})

#         except Exception as e:
#             return JsonResponse({"response": f"An error occurred: {str(e)}"})

#     return JsonResponse({"error": "Invalid request"}, status=400)

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