from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('verify-email/', verify_email, name='verify_email'),
    path('email-verified/', views.email_verified, name='email_verified'),  # A simple confirmation page
    # path('email-verification-failed/', views.email_verification_failed, name='email_verification_failed'),
    path('', views.course_list, name='course_list'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]