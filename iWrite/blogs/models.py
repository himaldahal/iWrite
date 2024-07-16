import random
import string
from django.contrib.auth.models import User
from django.db import models

def generate_random_slug(length=10):
    """Generates a random slug of given length."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    slug = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_random_slug(10)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    slug = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_random_slug(10)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')
    labels = models.CharField(max_length=2000, blank=True)
    slug = models.CharField(max_length=10, unique=True, blank=True)
    content = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_random_slug(10)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def word_count(self):
        """Returns the word count of the blog content."""
        return len(self.content.split())

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    slug = models.CharField(max_length=10, unique=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_random_slug(10)
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'

    def comment_depth(self):
        """Returns the depth of the comment in the thread."""
        depth = 0
        comment = self
        while comment.parent_comment:
            depth += 1
            comment = comment.parent_comment
        return depth

class UserChange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='changes')
    model = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    old_value = models.TextField()
    new_value = models.TextField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Change by {self.user.username} on {self.changed_at}'

def user_categories(user):
    """Returns categories created by the given user."""
    return Category.objects.filter(created_by=user)

def user_blogs(user):
    """Returns blogs added by the given user."""
    return Blog.objects.filter(added_by=user)
