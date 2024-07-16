from django.contrib import admin
from django.utils.text import slugify
from .models import UserProfile, Category, Blog, Comment, UserChange

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'bio', 'slug')
    search_fields = ('user__username', 'name', 'bio')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'slug')
    search_fields = ('name', 'created_by__username')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'added_by', 'added_on', 'updated_on', 'slug')
    search_fields = ('title', 'category__name', 'content', 'added_by__username')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'parent_comment', 'added_on', 'slug')
    search_fields = ('blog__title', 'user__username', 'content')
    list_filter = ('added_on', 'blog__category')

class UserChangeAdmin(admin.ModelAdmin):
    list_display = ('user', 'model', 'field', 'old_value', 'new_value', 'changed_at')
    search_fields = ('user__username', 'model', 'field', 'old_value', 'new_value')
    list_filter = ('changed_at',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserChange, UserChangeAdmin)
