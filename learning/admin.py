from django.contrib import admin
from .models import Course, Lesson, Progress

from django import forms
from django.contrib import admin
from .models import Lesson
from django_ckeditor_5.widgets import CKEditor5Widget

admin.site.register(Course)
# admin.site.register(Progress)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='default'),  # Use CKEditor5Widget for the content field
        }

class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm

