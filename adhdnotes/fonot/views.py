from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import Note
from .myforms import NoteForm

import random


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








def file_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'fonot/file_list.html', {'notes': notes})


def create_file(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.color = random.choice(['#FFFFCC', '#FFCCCC', '#CCE5FF', '#CCFFCC', '#FFD700', '#E6E6FA', '#FF9999', '#008080', '#E6E6FA', '#C0C0C0'])
            note.save()
            return redirect('file_list')
    else:
        form = NoteForm()
    return render(request, 'fonot/create_file.html', {'form': form})


def edit_file(request, file_id):
    note = get_object_or_404(Note, id=file_id, user=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('content')  # Correctly retrieve 'content'
        note.content = new_content
        note.save()

        # Redirect to the note detail page or another appropriate page
        return redirect('file_list')  # Replace 'note_detail' with your detail view name

    return render(request, 'fonot/edit_file.html', {'note': note})



def delete_file(request, file_id):
	note = get_object_or_404(Note, id=file_id, user=request.user)
	note.delete()

	return redirect('file_list')