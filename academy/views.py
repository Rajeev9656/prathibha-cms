from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# ---------- Dashboards ----------
def home(request):
    return render(request, 'home.html')

def admin_dashboard(request):
    return render(request, 'tutor_dashboard.html')

def staff(request):
    return render(request, 'staff.html')

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def batches(request):
    return render(request, 'batches.html')

def member_list(request):
    students = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'students_details.html')

def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')


def students_details(request):
    students = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'member_list.html',context={'students':students})


# ---------- Unified Login ----------
def unified_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Check role and redirect
            if user.is_superuser:  
                return redirect("tutor_dashboard")     # Admin
            elif user.is_staff:  
                return redirect("staff_dashboard")     # Staff/Tutor
            else:  
                return redirect("student_dashboard")   # Student

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# ---------- Logout ----------
def user_logout(request):
    logout(request)
    return redirect('home')  


# ---------- Student Registration ----------
def member_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            # 👇 Default student (not staff, not superuser)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            messages.success(request, "Registration successful! Please login.")
            return redirect("login")

    return render(request, "member_registration.html")


# ---------- Add Staff (by Admin only) ----------
def add_staff(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            # 👇 Make staff
            user.is_staff = True
            user.is_superuser = False
            user.save()

            messages.success(request, "Staff added successfully!")
            return redirect('staff_dashboard')

    return render(request, 'add_staff.html')

def schedule_view(request):
    # You can pass context like classes, events, exams if needed
    context = {
        "today_schedule": [],   # replace with your query
        "week_schedule": [],
        "exams": [],
        "events": [],
    }
    return render(request, 'schedule.html', context)
