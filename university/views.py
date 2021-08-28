from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .form import StudentForm
from .models import *


# Create your views here.
def index(request):
    universities = University.objects.all()

    return render(request, 'university/index.html', {"universities": universities})


def university(request, id):
    try:
        faculties = Faculty.objects.filter(university_id=id)
    except Faculty.DoesNotExist:
        faculties = None

    # students = Student.objects.filter(faculty=faculties)
    # courses = Course.objects.filter(faculty=faculties)
    return render(request, 'university/university.html', {"faculties": faculties})


def student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        student = None
    return render(request, 'university/student.html', {"student": student})


def course(request, id):
    if request.method == "POST":
        error = False
        try:
            student = Student.objects.get(id=request.POST['student'])
            course = Course.objects.get(id=id)
            course.students.add(student)
            course.save()
        except Student.DoesNotExist:
            error = "there is no such a student"

        except Course.DoesNotExist:
            error = "there no such a course"
        try:
            exclude_students = Student.objects.filter(faculty=course.faculty).exclude(student_course=course)
        except Student.DoesNotExist:
            error = "there is no excluded students"
            exclude_students = None
        return render(request, 'university/course.html',
                      {"error": error, "course": course, 'students': exclude_students})


    else:
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            course = None
        exclude_students = Student.objects.filter(faculty=course.faculty).exclude(student_course=course)
        return render(request, "university/course.html", {"course": course, "students": exclude_students})


def delete_course(request, student_id, course_id):
    try:
        course = Course.objects.get(id=course_id)
        student = Student.objects.get(id=student_id)
        course.students.remove(student)
        return HttpResponseRedirect(reverse('course', args=(course_id,)))
    except Course.DoesNotExist:
        error = "there is no such a course"
    except Student.DoesNotExist:
        error = "there is no such a student"


def add_student(request, faculty_id):
    global faculty
    student_form = StudentForm()
    try:
        faculty = Faculty.objects.get(id=faculty_id)
        students = Student.objects.filter(faculty=faculty)

    except Faculty.DoesNotExist:
        students = None
    if request.method == "GET":
        return render(request, 'university/add_student.html',
                      {"students": students, 'form': student_form, "faculty": faculty})

    else:
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            print("it's validated")
            new_student = student_form.save(commit=False)
            new_student.faculty = faculty
            new_student.save()
            student_form = StudentForm()
            return render(request, 'university/add_student.html',
                          {"students": students, 'form': student_form, "faculty": faculty})
        else:
            return render(request, 'university/add_student.html',
                          {"students": students, "faculty": faculty, "form": student_form})
