from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('university/<int:id>', views.university, name="university"),
    path('student/<int:id>', views.student, name="student"),
    path('course/<int:id>', views.course, name="course"),
    path('course/delete/<int:student_id>/<int:course_id>', views.delete_course, name="delete"),
    path('add-student/<int:faculty_id>', views.add_student, name="add_student"),
    path('add-course/<int:faculty_id>', views.add_course, name="add_course"),
    path('add-teacher/<int:personal_id>', views.add_teacher, name="add_teacher"),
    path('login', views.login_form, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('choose', views.choose, name="choose"),
    path('delete_course/<int:user_id>/<int:course_id>', views.delete_course_panel, name="delete_course_panel"),
]
