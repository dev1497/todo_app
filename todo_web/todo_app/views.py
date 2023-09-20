from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

from .forms import SignUpForm, ScheduleTaskForm
from .models import Task


# Create your views here.
def home(request):
    return redirect('login')


def signup_user(request):
    if request.user.is_authenticated:
        messages.success(request, "Cannot signup while logged in.")
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, "You have successfully registered.")
                return redirect('dashboard')
        else:
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form})
        return render(request, 'signup.html', {'form': form})


def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        tasks = Task.objects.filter(user_id=user)
        return render(request, 'dashboard.html', {'tasks': tasks})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('login')


def login_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect('dashboard')
            else:
                messages.success(request, "Error logging in. Please try again")
                return redirect('login')
        else:
            return render(request, 'login.html', {})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out!")
        return redirect('home')
    else:
        messages.success(request, "You are already logged out!")
        return redirect('login')


def schedule_task(request):
    form = ScheduleTaskForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_task = Task(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    expire_at=form.cleaned_data['expire_at'],
                    user_id=request.user
                )
                add_task.save()
                messages.success(request, "Task scheduled")
                return redirect('dashboard')
        return render(request, 'schedule.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('login')


def user_task(request, pk):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
            if request.user != task.user_id:
                messages.error(request, "Not authorized to see this task")
                return redirect('dashboard')
            else:
                return render(request, 'task.html', {'task': task})
        except ObjectDoesNotExist:
            print("nottttt user task found")
            messages.error(request, "Task not found.")
            return redirect('dashboard')
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('login')


def update_task(request, pk):
    if request.user.is_authenticated:
        # Check if the task exists or return a 404 error page if not found
        task = get_object_or_404(Task, id=pk)
        if request.user != task.user_id:
            messages.error(request, "Not authorized to update this task")
            return redirect('dashboard')
        else:
            if request.method == 'POST':
                form = ScheduleTaskForm(request.POST, instance=task)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Task updated successfully!")
                    return redirect('task', pk=pk)
            else:
                form = ScheduleTaskForm(instance=task)
            return render(request, 'update_task.html', {'form': form, 'task': task})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('login')


def mark_complete(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            new_status = request.POST.get("new_status")
            try:
                task = Task.objects.get(id=pk)
                if request.user != task.user_id:
                    messages.error(request, "Not authorized to update status of this task")
                    return redirect('dashboard')
                else:
                    task.status = new_status
                    task.save()
                    messages.success(request, "Task status updated!")
                    return render(request, 'task.html', {'task': task})
            except ObjectDoesNotExist:
                print("nottttt mark complete found")
                messages.error(request, "Task not found.")
                raise Http404("Task not found")
        else:
            return render(request, 'task.html', {})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('login')


def delete_task(request, pk):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
            if request.user != task.user_id:
                messages.error(request, "Not authorized to delete this task")
                return redirect('dashboard')
            else:
                task.delete()
                messages.success(request, "Task deleted successfully!")
        except ObjectDoesNotExist:
            print("nottttt")
            messages.error(request, "Task not found.")
        return redirect('dashboard')
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('login')

