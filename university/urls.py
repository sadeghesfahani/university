from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('university/<int:id>', views.university, name="university"),
    path('student/<int:id>', views.student, name="student"),
    path('course/<int:id>', views.course, name="course"),
    path('course/delete/<int:student_id>/<int:course_id>', views.delete_course, name="delete"),
]
