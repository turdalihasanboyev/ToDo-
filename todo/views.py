from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ToDo, CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def home_page_view(request):
    query = request.POST.get('query')

    todos = ToDo.objects.all().order_by('-id')

    if query:
        todos = todos.filter(title__icontains=query)
    
    return render(request, 'home.html', {"todos": todos})

def todo_detail_view(request, slug):
    todo = get_object_or_404(ToDo, slug__iexact=slug)

    return render(request, 'todo_detail.html', {"todo": todo})

def is_done_view(request, pk):
    todo = get_object_or_404(ToDo, id=pk)
    
    if todo.is_done:
        todo.is_done = False
    else:
        todo.is_done = True

    todo.save()

    return redirect('home')

def is_active_view(request, pk):
    todo = get_object_or_404(ToDo, id=pk)
    
    if todo.is_active:
        todo.is_active = False
    else:
        todo.is_active = True 

    todo.save()

    return redirect('home')

def update_todo_view(request, slug):
    todo = get_object_or_404(ToDo, slug__iexact=slug)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title', todo.title)
        todo.sub_title = request.POST.get('sub_title', todo.sub_title)
        todo.description = request.POST.get('description', todo.description)
        todo.priority = request.POST.get('priority', todo.priority)
        todo.deadline = request.POST.get('deadline', todo.deadline)
        todo.is_done = 'is_done' in request.POST
        todo.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            todo.image = request.FILES['image']
        if request.FILES.get('video'):
            todo.video = request.FILES['video']

        todo.save()
        
        messages.success(request, 'ToDo item updated successfully!')
        return redirect(todo.get_absolute_url())

    return render(request, 'update_todo.html', {'todo': todo})

def add_new_todo_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        sub_title = request.POST.get('sub_title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        todo = ToDo(
            title=title,
            sub_title=sub_title,
            description=description,
            priority=priority,
            deadline=deadline,
            image=image,
            video=video,
        )
        todo.save()

        messages.success(request, 'ToDo item created successfully!')

        return redirect('/')

    return render(request, 'add_todo.html')

def delete_todo_view(request, slug):
    todo = get_object_or_404(ToDo, slug__iexact=slug)
    
    if request.method == 'POST':
        todo.delete()
        
        messages.success(request, 'ToDo item deleted successfully!')

        return redirect('home')
    
    return render(request, 'confirm_delete.html', {'todo': todo})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        user = CustomUser.objects.create_user(email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully')
        login(request, user)
        return redirect('profile')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')