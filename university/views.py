from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .form import StudentForm, CourseForm, TeacherForm, UserForm
from .models import *


# Create your views here.
def index(request):
    universities = University.objects.all()
    # if request.user.student_set.filter(username=request.user.username).count() !=0:
    #     print("hi")

    return render(request, 'university/index.html', {"universities": universities})


def university(request, id):
    try:
        faculties = Faculty.objects.filter(university_id=id)
    except Faculty.DoesNotExist:
        faculties = None

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
    student_form = StudentForm()

    try:
        faculty = Faculty.objects.get(id=faculty_id)
        students = Student.objects.filter(faculty=faculty)
        university_id = faculty.university_id
    except Faculty.DoesNotExist:
        students = None
    if request.method == "GET":
        return render(request, 'university/add_student.html',
                      {"students": students, 'form': student_form, "faculty": faculty, "university": university_id})

    else:
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            new_student = student_form.save(commit=False)
            new_student.faculty = faculty
            new_student.save()
            student_form = StudentForm()
            return render(request, 'university/add_student.html',
                          {"students": students, 'form': student_form, "faculty": faculty, "university": university_id})
        else:
            return render(request, 'university/add_student.html',
                          {"students": students, "faculty": faculty, "form": student_form, "university": university_id})


def add_course(request, faculty_id):
    faculty = Faculty.objects.get(id=faculty_id)
    courses = Course.objects.filter(faculty=faculty)
    course_form = CourseForm()
    teachers = Teacher.objects.filter(faculty=faculty)

    if request.method == "POST":
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            new_course = course_form.save(commit=False)
            new_course.faculty = faculty
            new_course.teacher = Teacher.objects.get(id=request.POST['teacher'])
            new_course.save()
            course_form.save_m2m()
            return render(request, 'university/add_course.html',
                          {"courses": courses, "teachers": teachers, "form": course_form, "faculty": faculty})
        else:
            return render(request, 'university/add_course.html',
                          {"courses": courses, "form": course_form, "teachers": teachers, "faculty": faculty})
    else:
        pass
    return render(request, 'university/add_course.html',
                  {"courses": courses, "form": course_form, "teachers": teachers, "faculty": faculty})


def add_teacher(request, faculty_id):
    faculty = Faculty.objects.get(id=faculty_id)
    form = TeacherForm()
    university_id = faculty.university_id
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.faculty = faculty
            new_form.save()
            return render(request, 'university/add_teacher.html', {'form': form, 'university_id': university_id})
        else:
            return render(request, 'university/add_teacher.html', {'form': form, 'university_id': university_id})
    else:
        return render(request, 'university/add_teacher.html', {'form': form, 'university_id': university_id})


def login_form(request):
    login_form = UserForm()
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])
            if user is not None:
                print(user)
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'university/login.html', {"form": login_form})


def choose(request):
    faculty = Student.objects.get(username=request.user.username).faculty
    courses = Course.objects.filter(faculty=faculty)
    return render(request, 'university/choose.html', {"faculty": faculty, "courses": courses})
