from courses.views import *
from django.urls import path

urlpatterns = [
        path('', homepage, name='homepage'),
        path('course/<str:slug>', course_details, name='course_details')
]
