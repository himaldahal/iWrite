from django.contrib import admin

from .models import Course, Instructor, Lecture, Student, Subject

admin.site.site_header = 'iSchool Administration'
admin.site.site_title = 'iSchool Admin Portal'
admin.site.index_title = 'Welcome to iSchool Admin'


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'subject_description', 'subject_slug')
    search_fields = ('subject_name', 'subject_description')
    prepopulated_fields = {'subject_slug': ('subject_name',)}
    list_filter = ('subject_name',)
    fieldsets = (
        (None, {'fields': ('subject_name', 'subject_description', 'subject_slug')}),
    )

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'profile_pic')
    search_fields = ('user__username', 'subject__subject_name', 'about')
    list_filter = ('subject', 'user__is_staff')
    autocomplete_fields = ('user', 'subject')
    fieldsets = (
        (None, {'fields': ('user', 'subject', 'profile_pic', 'about')}),
    )

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'instructors', 'slug')
    search_fields = ('name', 'description', 'instructors__user__username')
    list_filter = ('instructors__subject',)
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('instructors',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'instructors', 'slug')}),
    )

class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'instructor', 'uploaded_on')
    search_fields = ('title', 'course__name', 'instructor__user__username', 'note')
    list_filter = ('course', 'instructor', 'uploaded_on')
    autocomplete_fields = ('course', 'instructor')
    fieldsets = (
        (None, {'fields': ('title', 'lecture', 'course', 'note', 'instructor', 'uploaded_on')}),
    )
    date_hierarchy = 'uploaded_on'

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    list_filter = ('courses_enrolled',)
    autocomplete_fields = ('user', 'courses_enrolled')
    filter_horizontal = ('courses_enrolled',)
    fieldsets = (
        (None, {'fields': ('user', 'courses_enrolled')}),
    )

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Student, StudentAdmin)
