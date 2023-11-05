from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .myforms import UserFileForm
from .models import UserFile
from django.core.files.base import ContentFile




def home(request):
    return render(request, 'fonot/home.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to a success page or home page
            return redirect('file_list')  # Change 'home' to your desired URL name
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = UserCreationForm()
    
    return render(request, 'fonot/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page or home page
            return redirect('file_list')  # Change 'home' to your desired URL name
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'fonot/login.html', {'form': form})


def user_logout(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('home')


def upload_file(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user  # Associate the file with the logged-in user
            user_file.save()
            return redirect('file_list')  # Redirect to a file list page
    else:
        form = UserFileForm()
    return render(request, 'fonot/upload_file.html', {'form': form})

def file_list(request):
    files = UserFile.objects.filter(user=request.user)
    return render(request, 'fonot/file_list.html', {'files': files})


def edit_file(request, file_id):
    user_file = get_object_or_404(UserFile, id=file_id, user=request.user)

    if request.method == 'POST':
        new_file_content = request.POST['file_content']
        
        # Use ContentFile to update file content
        user_file.file.save(user_file.file.name, ContentFile(new_file_content))

    return render(request, 'fonot/edit_file.html', {'user_file': user_file})
