from django.contrib.auth.models import User
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
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
    content = RichTextUploadingField()
    order = models.PositiveIntegerField()  # To order lessons in a course

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

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