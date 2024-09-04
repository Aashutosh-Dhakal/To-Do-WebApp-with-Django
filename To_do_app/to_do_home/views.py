from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_task = todo(user=request.user, title=task)
        new_task.save()

    all_todos = todo.objects.filter(user=request.user)
    return render(request, 'to_do_home/todo.html', {'todos': all_todos})


def login_user(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            messages.success(
                request, (f'Login in Successful!  Welcome {username} 😊'))
            return redirect('home')
        else:
            messages.error(request, 'Incorrect  Username or Password!')
            return redirect('login')

    return render(request, 'to_do_home/login.html', {})


def register_user(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        get_all_user_by_username = User.objects.filter(username=username)
        get_all_user_by_email = User.objects.filter(email=email)
        if get_all_user_by_username:
            messages.error(
                request, ('Username Already Exists, Try using different username.'))
            return redirect('register')
        elif get_all_user_by_email:
            messages.error(
                request, ('Provided Email has already been Used, Try another.'))
            return redirect('register')
        elif len(password) < 8:
            messages.error(
                request, ('Password should not be less than 8 characters'))
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                username=username, email=email, password=password)
            new_user.save()
            messages.success(
                request, ('The Account has been registered Successfully! Login Now'))

            return redirect('login')

    return render(request, 'to_do_home/register.html', {})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def delete_task(request, name):
    get_todo = todo.objects.get(user=request.user, title=name)
    get_todo.delete()
    return redirect('home')


@login_required
def update_task(request, name):
    get_todo = todo.objects.get(user=request.user, title=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home')
