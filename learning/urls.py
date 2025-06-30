from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_image

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('paths', views.paths, name='paths'),
    path('logout/', views.user_logout, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    # path('verify-email/', verify_email, name='verify_email'),
    path('email-verified/', views.email_verified, name='email_verified'),  # A simple confirmation page
    # path('email-verification-failed/', views.email_verification_failed, name='email_verification_failed'),
    path('courses', views.course_list, name='course_list'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    # path('course/<str:course_title>/', views.course_lessons, name='course_lessons'),
    path('course/<slug:course_title>/', views.course_lessons, name='course_lessons'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('upload_image/', upload_image, name='upload_image'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('ai-chat/', views.ai_chat_view, name='ai_chat'),
    path('assessment-report/', views.assessment_report_view, name='assessment_report'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)