from django.contrib.auth.models import User
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

from django_ckeditor_5.fields import CKEditor5Field
# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = CKEditor5Field(config_name='default')
    order = models.PositiveIntegerField()  # To order lessons in a course

    class Meta:
        ordering = ['order']  # Ensures lessons are always fetched in order
        indexes = [
            models.Index(fields=['course', 'order']),
        ]

    def __str__(self):
        return self.title
    
    def is_locked(self, user):
        """
        Determines whether the lesson is locked for the given user.
        A lesson is locked if the previous lesson is incomplete.
        """
        previous_lesson = Lesson.objects.filter(course=self.course, order__lt=self.order).last()
        if previous_lesson:
            previous_progress = Progress.objects.filter(user=user, lesson=previous_lesson).first()
            return not previous_progress or not previous_progress.completed
        return False

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')
        indexes = [
            models.Index(fields=['user', 'lesson']),
            models.Index(fields=['lesson', 'completed']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.lesson.title} - {"Completed" if self.completed else "Incomplete"}'

class StudentLevelAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=Course.LEVEL_CHOICES, default='beginner')

    class Meta:
        unique_together = ('user', 'level')

    def __str__(self):
        return f'{self.user.username} - {self.get_level_display()}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username