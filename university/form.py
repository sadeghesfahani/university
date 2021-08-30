from django.forms import ModelForm
from django import forms
from .models import *


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'password']


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["name", "unit", "classroom"]


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['username', 'first_name', 'last_name', 'password']


class UserForm(forms.Form):
    username = forms.CharField(label="نام کاربری", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
