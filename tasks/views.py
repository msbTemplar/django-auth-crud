from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def helloworld(request):
    # return HttpResponse('<h1>salamulakimum</h1>')
    title = 'Salam sidi'
    return render(request, 'signup.html', {
        # 'mytitle':title
        'form': UserCreationForm
    })


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        print(request.POST)
        print('obteniendo datos')
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                #return HttpResponse('Usuario creado correctamente')
                return redirect('tasks')

            except IntegrityError:
                # return HttpResponse('Usuario ya existe en la base de datos')
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe en la base de datos'
                })
        
        # return HttpResponse('password no coinciden')
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'password no coinciden'
        })
@login_required      
def tasks(request):
    #tareas=Task.objects.all()
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks':tasks})

@login_required
def tasks_completed(request):
    #tareas=Task.objects.all()
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks':tasks})

@login_required
def create_task(request):
    if request.method=='GET':
        return render(request, 'create_task.html', {
        'form':TaskForm
        })
    else:
        try:
            print(request.POST)
            form=TaskForm(request.POST)
            print(form)
            new_task=form.save(commit=False)
            new_task.user=request.user
            print(new_task)
            new_task.save()
            return redirect('tasks')
            #return render(request, 'create_task.html', {
            #'form':TaskForm
            #})
        
        except ValueError:
            return render(request, 'create_task.html', {
            'form':TaskForm,
            'error':'Introduzca datos correctos '
            })
            
@login_required            
def task_detail(request, task_id):
    print(task_id)
    #tarea=Task.objects.get(pk=task_id)
    if request.method == 'GET':
        task=get_object_or_404(Task,pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task,'form': form})
    else:
        try:
            print(request.POST)
            task=get_object_or_404(Task,pk=task_id, user=request.user)
            form=TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        
        except ValueError:
            error="Error actualizando la tarea"
            return render(request, 'task_detail.html', {'task': task,'form': form, 'error':error})

@login_required            
def complete_task(request, task_id):
    task=get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required        
def delete_task(request, task_id):
    task=get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        
        task.delete()
        return redirect('tasks')
    
    
@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{
        'form':AuthenticationForm
        })
    else:
        print(request.POST)
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
            'form':AuthenticationForm,
            'error':'Usuario o contraseña incorrectos'
            })
        else:
            login(request,user)
            return redirect('tasks')   
       # return render(request,'signin.html',{
        #    'form':AuthenticationForm
        #})


        