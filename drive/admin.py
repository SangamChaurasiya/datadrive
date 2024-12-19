from django.contrib import admin
from drive.models import Folder, File


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
