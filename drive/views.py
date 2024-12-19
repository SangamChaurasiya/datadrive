from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from drive.models import Folder, File
from urllib.parse import urlencode
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
import uuid


# View For SignUp the user
def SignUp(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['cpassword']
            fname = request.POST['fname']
            lname = request.POST['lname']
            if username and password and email and cpassword and fname and lname:
                if password == cpassword:
                    user = User.objects.create_user(username,email,password)
                    user.first_name = fname
                    user.last_name = lname
                    user.save()
                    if user:
                        messages.success(request,"User Account Created")
                        return redirect("login")
                    else:
                        messages.error(request,"User Account Not Created")
                else:
                    messages.error(request,"Password Not Matched")
                    redirect("signup")
        return render(request,'signup.html')


# View For Log in the user
def Login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('index')
        return render(request,'login.html')


# User logout function
def Logout(request):
    logout(request)
    return redirect("home")


def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id

        if request.method == "POST":
            folder_name = request.POST.get('folder_name', None)
            create_folder(folder_name=folder_name, parent_folder_id=None, owner_id=user_id)

        folders = Folder.objects.filter(parent=None, owner_id=user_id)
        return render(request, 'index.html', {'folders': folders})
    else:
        return redirect('signup')


def get_folders(request, folder_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        parent_folders = Folder.objects.filter(id=folder_id)
        if not parent_folders:
            # Handle invalid request
            pass
        if request.method == "POST":
            folder_name = request.POST.get('folder_name', None)
            create_folder(folder_name=folder_name, parent_folder_id=folder_id, owner_id=user_id)
        folders = Folder.objects.filter(parent_id=folder_id)
        files = File.objects.filter(folder_id=folder_id)

        return render(request, 'index.html', {'folders': folders, 'files': files, 'folder_id': folder_id, 'path': parent_folders.first()})
    else:
        return redirect('login')


def create_folder(folder_name, owner_id, parent_folder_id=None):
    if not folder_name:
        return
    try:
        parent = Folder.objects.get(id=parent_folder_id) if parent_folder_id else None
    except (Folder.DoesNotExist, ValueError):
        parent = None
    
    Folder.objects.create(
        name=folder_name, 
        owner_id=owner_id, 
        parent=parent
    )


def upload_file(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Retrieve the uploaded file
            file_name = request.POST.get('file_name', None)   # The file input name in the form
            folder_id = request.POST.get('folder_id')  # Additional hidden input
            file = request.FILES.get('file')
            user_id = request.user.id
            if file_name:
                file = File(id=uuid.uuid4(), folder_id=folder_id, owner_id=user_id, file=file, name=file_name)
                file.save()
                
                return redirect('/')   

        return redirect('/')
    else:
        return redirect('login')


# def edit_file(request, file_id):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             # Retrieve the uploaded file
#             file_name = request.POST.get('file_name', None)   # The file input name in the form
#             folder_id = request.POST.get('folder_id')  # Additional hidden input
#             file = request.FILES.get('file')
#             user_id = request.user.id
#             if file_name:
#                 try:
#                     file = File.objects.get(id=file_id)
#                     file.name=file_name
#                     file.file=file
#                     file.folder=Folder.objects.get(id=folder_id)
#                     file.owner=User.objects.get(pk=user_id)
#                     file.save()
#                     messages.success(request, 'File Updated Successfully!')
#                 except Exception as e:
#                     print(e)
#                     messages.error(request, 'File does not exists!')
#                 return redirect(f'http://127.0.0.1:8000/folder/{folder_id}/')   

#         return redirect('/')
#     else:
#         return redirect('login')



def shared_file(request):
    if request.method == 'POST':
        share_option = request.POST.get("shareOption")
        file_id = request.POST.get("file_id")
        emails = request.POST.get("emails", "").strip()
        redirect_url = request.META.get('HTTP_REFERER', '/')
        redirect_url = "/".join(redirect_url.split("/")[:-1])

     
        if not emails:
            is_public = make_public_file(file_id=file_id)
            params = {
                "link" : f" http://127.0.0.1:8000/file/access/{file_id}"
            }

            if not is_public:
                params['error'] ='Could not make file public',
                     
            query_string = urlencode(params)
            return redirect(f"{redirect_url}?{query_string}")
            
        
    return redirect('/')


def make_public_file(file_id):
    file = get_file_by_id(file_id=file_id).first()
    if not filter:
        return False
    file.visibility = 'public'
    file.save()
    return True


def file_access(request,id):
    files = get_file_by_id(file_id=id)
    if not files:
        return render(request, 'index.html', { 'error': "not such file."})
    return render(request, 'index.html', { 'files': files,"is_file_shared":True})


def get_file_by_id(file_id):
    return File.objects.filter(id=file_id)


def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    folder.delete()
    messages.error(request, 'Folder Deleted Successfully.')
    return redirect('index')


def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    file.delete()
    messages.error(request, 'File Deleted Successfully.')
    return redirect('index')
