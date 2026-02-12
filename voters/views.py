from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm
import csv
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_superuser


def landing_page(request):
    return render(request, "voters/landing_page.html")


def verify_student(request):
    if request.method == "POST":
        matric = request.POST.get("matric")
        name = request.POST.get("name")  # Changed from last_name to name
        try:
            # Normalize the input name to title case and strip spaces
            normalized_name = name.title().strip()

            # Try to find student by matric
            student = Student.objects.get(matric=matric)

            # Check if normalized name matches either first or last name
            if (
                normalized_name == student.first_name
                or normalized_name == student.last_name
            ):
                return render(
                    request, "voters/student_details.html", {"student": student}
                )
            else:
                raise Student.DoesNotExist

        except Student.DoesNotExist:
            messages.error(request, "Student details not found. Please register.")
            return redirect("voters:register_student")
    return render(request, "voters/verify_student.html")


def register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            # Normalize names to title case
            student = form.save(commit=False)
            student.first_name = student.first_name.title().strip()
            student.last_name = student.last_name.title().strip()
            student.save()
            messages.success(
                request, "Registration successful. You can now verify your details."
            )
            return redirect("voters:verify_student")
    else:
        form = StudentForm()
    return render(request, "voters/register_student.html", {"form": form})


@user_passes_test(is_admin)
def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "Please upload a .csv file.")
            return redirect("voters:upload_csv")

        try:
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                Student.objects.update_or_create(
                    matric=row["matric"],
                    defaults={
                        "first_name": row["first_name"].title().strip(),
                        "last_name": row["last_name"].title().strip(),
                        "level": row["level"],
                        "sex": row["sex"],
                    },
                )
            messages.success(request, "Students uploaded successfully.")
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")

        return redirect("voters:upload_csv")

    return render(request, "voters/upload_csv.html")
