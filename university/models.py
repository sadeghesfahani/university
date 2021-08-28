from datetime import date
from django.contrib.auth.models import User
from django.db import models
import random


# Create your models here.


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


class Staff(User):
    personal_id = models.IntegerField(unique=True, default=generateStaffPersonalId)

    def __str__(self):
        return f"{self.first_name} - {self.personal_id}"


class Teacher(User):
    personal_id = models.IntegerField(unique=True, default=generateTeacherPersonalId)

    def __str__(self):
        return f"{self.first_name} - {self.personal_id}"


class Student(User):
    student_id = models.IntegerField(unique=True, default=generateStudentPersonalId)

    def __str__(self):
        return f"{self.first_name} - {self.student_id}"


class University(models.Model):
    name = models.CharField(max_length=100)
    staff = models.ManyToManyField(Staff, blank=True, null=True)
    students = models.ManyToManyField(Student, blank=True, null=True)
    teachers = models.ManyToManyField(Teacher, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculty')
    staff = models.ManyToManyField(Staff, blank=True, null=True)
    students = models.ManyToManyField(Student, blank=True, null=True)
    teachers = models.ManyToManyField(Teacher, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    name = models.CharField(max_length=150)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course')
    students = models.ManyToManyField(Student, blank=True, null=True)
    teachers = models.ManyToManyField(Staff, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
