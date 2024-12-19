from django.urls import path
from drive import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.Login, name="login"),
    path("signup/",views.SignUp,name="signup"),
    path("folder/<str:folder_id>/",views.get_folders, name="folders"),
    path('upload-file/', views.upload_file, name='upload'),
    path('shared_file/', views.shared_file, name='share'),
    path('file/access/<str:id>/', views.file_access),
    path('delete-folder/<str:folder_id>/', views.delete_folder, name='delete_folder'),
    # path('edit-file/<str:file_id>/', views.edit_file, name='edit_file'),
    path('delete-file/<str:file_id>/', views.delete_file, name='delete_file'),
    path("logout/", views.Logout, name="logout"),
]
