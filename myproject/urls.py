"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from academy import views 

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('', views.home, name='home'),
    path('batches', views.batches, name='batches'),
    path('members', views.member_list, name='member_list'),

    # Dashboards
    path('tutor-dashboard', views.admin_dashboard, name='tutor_dashboard'),
    path('student-dashboard', views.student_dashboard, name='student_dashboard'),

    # Authentication (names as per home.html)
    path('login', views.unified_login, name='login'),
    path("register", views.member_register, name="member_registration"),
    path('logout/', views.user_logout, name='logout'),
    path('students-details/', views.students_details, name='students_details'),
    path("staff/", views.staff, name="staff"),
    path('add-staff/', views.add_staff, name='add_staff'),
    path("staff-dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path('schedule/', views.schedule_view, name='schedule'), 
    path('students/', views.students_details, name='students_details'),
    path('student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
]