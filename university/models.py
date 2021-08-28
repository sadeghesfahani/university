from datetime import date
from django.contrib.auth.models import User
from django.db import models
import random

# Create your models here.
from django.db.models import Sum


def generateStaffPersonalId():
    today = date.today()
    generated = random.randint(int(str(today.year) + "0001"), int(str(today.year) + "9999"))
    if Staff.objects.filter(personal_id=generated).count() == 0:
        return generated
    else:
        generateStaffPersonalId()


def generateTeacherPersonalId():
    today = date.today()
    generated = random.randint(int(str(today.year) + "0001"), int(str(today.year) + "9999"))
    if Teacher.objects.filter(personal_id=generated).count() == 0:
        return generated
    else:
        generateTeacherPersonalId()


def generateStudentPersonalId():
    today = date.today()
    generated = random.randint(int(str(today.year) + "0001"), int(str(today.year) + "9999"))
    if Student.objects.filter(student_id=generated).count() == 0:
        return generated
    else:
        generateStudentPersonalId()


class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='university_faculty')

    def __str__(self):
        return f"{self.university.name} - {self.name}"


class Teacher(User):
    personal_id = models.IntegerField(unique=True, default=generateTeacherPersonalId)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} - {self.personal_id}"


class Student(User):
    student_id = models.IntegerField(unique=True, default=generateStudentPersonalId)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    @property
    def units(self):
        return self.student_course.all().aggregate(Sum('unit'))['unit__sum']

    def __str__(self):
        return f"{self.last_name} - {self.student_id} - {self.faculty.name}"


class Staff(User):
    personal_id = models.IntegerField(unique=True, default=generateStaffPersonalId)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} - {self.personal_id}"


class ClassRoom(models.Model):
    name = models.CharField(max_length=60)
    capacity = models.SmallIntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="classroom_faculty")

    def __str__(self):
        return f"{self.name} - {self.capacity}"


class Course(models.Model):
    name = models.CharField(max_length=150)
    unit = models.SmallIntegerField(blank=False, null=False, default=1)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course')
    students = models.ManyToManyField(Student, related_name='student_course')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, blank=True, null=True)
    classroom = models.ManyToManyField(ClassRoom, related_name='classroom_course')

    def __str__(self):
        return f"{self.name}"
