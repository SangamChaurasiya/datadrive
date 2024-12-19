from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import uuid

# Create your models here.
class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('name', 'parent', 'owner')
        ordering = ['name']

    
class File(models.Model):
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('shared', 'Shared'),
        ('public', 'Public')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='user_files/%Y/%m/%d/', validators=[FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'xlsx', 'xls', 'ppt', 'pptx']
    )])
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        Generate a URL for direct file access
        """
        return self.file.url 

    class Meta:
        unique_together = ('name', 'folder', 'owner')
        ordering = ['name']


class SharedFile(models.Model):
    shared_user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    file = models.ForeignKey(to=File,on_delete=models.CASCADE)
    