import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


def unique_slugify(instance, value, slug_field_name='slug', max_length=90):
    """
    Calculate a unique slug for the model instance if the default value exists.
    """
    slug = slugify(value)
    unique_slug = slug
    model_class = instance.__class__

    # Ensure the slug is unique by appending a number if necessary
    while model_class.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{uuid.uuid4().hex[:8]}"
        if len(unique_slug) > max_length:
            unique_slug = unique_slug[:max_length]
    
    return unique_slug

def upload_to(instance, filename):
    """
    Generate a unique file name for the uploaded image file.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex[:64]}.{ext}"
    return os.path.join('instructor/', filename)

class Subject(models.Model):
    subject_name = models.CharField(max_length=90, default='')
    subject_description = models.TextField(blank=True, null=True)
    subject_slug = models.SlugField(max_length=90, unique=True, blank=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
    
    def save(self, *args, **kwargs):
        if not self.subject_slug:
            self.subject_slug = unique_slugify(self, self.subject_name, slug_field_name='subject_slug')
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject_name

class Instructor(models.Model):
    profile_pic = models.ImageField(default='', upload_to=upload_to)
    user = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, default=0, on_delete=models.CASCADE)
    about = models.TextField()
    
    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True)
    instructors = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=0)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

def lecture_upload_to(instance, filename):
    """
    Generate a unique file name for the uploaded lecture file.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex[:64]}.{ext}"
    return os.path.join('lecture/', filename)

class Lecture(models.Model):
    title = models.CharField(max_length=500, default='')
    lecture = models.FileField(upload_to=lecture_upload_to)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    note = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    courses_enrolled = models.ManyToManyField(Course)

    def __str__(self):
        return self.user.username
