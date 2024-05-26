"""
URL configuration for NEPHROVIR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='custom_login'), name='logout'),
    path('register/', views.register, name='register'),  
    path('login/', views.custom_login, name='custom_login'),
    path('welcome/', views.welcome, name='welcome'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='WEBAPP/password_reset_form.html',
        email_template_name='WEBAPP/password_reset_email.html',
        subject_template_name='WEBAPP/password_reset_subject.txt',
        success_url='/password_reset_done/'
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='WEBAPP/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='WEBAPP/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='WEBAPP/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('add_patient/', views.add_patient, name='add_patient'),
    
    path('add_patient_and_test/', views.add_patient_and_test, name='add_patient_and_test'),
    path('edit_patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),

    
    path('delete_patient_confirm/<int:patient_id>/', views.delete_patient_confirm, name='delete_patient_confirm'),
    path('patient/<int:patient_id>/read/', views.read_patient, name='read_patient'),
    path('patient/<int:patient_id>/add_test/', views.add_test, name='add_test'),
    path('test/<int:test_id>/edit/', views.edit_test, name='edit_test'),
    path('test/<int:test_id>/delete/', views.delete_test, name='delete_test'),
    path('test/<int:test_id>/', views.read_test, name='read_test'),
    path('test/<int:test_id>/pdf/', views.download_test_pdf, name='download_test_pdf'),


]
