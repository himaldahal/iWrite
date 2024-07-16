from django.shortcuts import render,redirect
from courses.models import *
from django.shortcuts import get_object_or_404


def homepage(request):
    courses = Course.objects.all()
    return render(request,'homepage.html',{'courses':courses})

def course_details(request,slug):
    course = get_object_or_404(Course,slug=slug)
    return render(request,'course_details.html',{'course':course})