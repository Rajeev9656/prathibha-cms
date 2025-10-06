from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Student
from .models import ClassSchedule, ExamSchedule, Event
from django.contrib.auth.hashers import make_password,check_password
from .models import Student, Staff


# ---------- Dashboards ----------
def home(request):
    return render(request, 'home.html')

def admin_dashboard(request):
    return render(request, 'tutor_dashboard.html')


def staff(request):
    return render(request, 'staff.html')

def staff_dashboard(request):
    return render(request, "staff_dashboard.html")

def batches(request):
    return render(request, 'batches.html')

def member_list(request):
     students = Student.objects.all().order_by('first_name')
     return render(request, "member_list.html", {"students": students})

def student_dashboard(request):
    classes = ClassSchedule.objects.all().order_by('date', 'time')
    exams = ExamSchedule.objects.all().order_by('date', 'time')
    events = Event.objects.all().order_by('date')
    return render(request, 'student_dashboard.html', {
        'classes': classes,
        'exams': exams,
        'events': events
    })



def students_details(request):
    students = Student.objects.all()
    return render(request, 'students_details.html', {'students': students})


# ---------- Unified Login ----------
def unified_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 1️⃣ Check Django User first (Admin/Staff)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("tutor_dashboard")
            elif user.is_staff:
                return redirect("staff_dashboard")

        # 2️⃣ If not found, check Student table
        try:
            student = Student.objects.get(username=username)
            if check_password(password, student.password):
                request.session['student_id'] = student.id
                return redirect("student_dashboard")
            else:
                messages.error(request, "Invalid student password.")
        except Student.DoesNotExist:
            pass

        # 3️⃣ If not found anywhere
        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# ---------- Logout ----------
def user_logout(request):
    logout(request)
    return redirect('home')  


# ---------- Student Registration ----------
from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages  # optional, to show success message

def member_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Save to the database
        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip=zip_code,
            username=username,
            password=make_password(password)  # 🔒 hash password
        )

        messages.success(request, "Student registered successfully!")
        return redirect('member_registration')  # Redirect to avoid duplicate submissions

    return render(request, 'member_registration.html')




# ---------- Add Staff (by Admin only) ----------
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def add_staff(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # ✅ Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect("add_staff")

        # Create the staff user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,  # gives access to staff dashboard
        )

        messages.success(request, f"Staff member {username} added successfully.")
        return redirect("tutor_dashboard")

    return render(request, "add_staff.html")

def schedule_view(request):
    # You can pass context like classes, events, exams if needed
    context = {
        "today_schedule": [],   # replace with your query
        "week_schedule": [],
        "exams": [],
        "events": [],
    }
    return render(request, 'schedule.html', context)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        student.city = request.POST.get("city")
        student.state = request.POST.get("state")
        student.batch = request.POST.get("batch")
        fees_paid = request.POST.get("fees_paid")
        # Convert string to boolean
        student.fees_paid = True if fees_paid == "True" else False

        student.save()
        return redirect("students_details")  # Redirect to student details page

    return render(request, "edit_member.html", {"student": student})


from .models import ClassSchedule, ExamSchedule, Event

def schedule_management(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "class":
            ClassSchedule.objects.create(
                batch=request.POST["batch"],
                topic=request.POST["topic"],
                date=request.POST["date"],
                time=request.POST["time"],
                room_or_link=request.POST.get("room_or_link", "")
            )

        elif form_type == "exam":
            ExamSchedule.objects.create(
                subject=request.POST["subject"],
                date=request.POST["date"],
                time=request.POST["time"]
            )

        elif form_type == "event":
            Event.objects.create(
                title=request.POST["title"],
                description=request.POST.get("description", ""),
                date=request.POST["date"]
            )

        return redirect("schedule")

    classes = ClassSchedule.objects.all().order_by("date", "time")
    exams = ExamSchedule.objects.all().order_by("date", "time")
    events = Event.objects.all().order_by("date")

    return render(request, "schedule.html", {
        "classes": classes,
        "exams": exams,
        "events": events,
    })





