from django.contrib import admin
from .models import Course, Lesson

admin.site.register(Course)
# admin.site.register(Lesson)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)