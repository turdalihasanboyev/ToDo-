from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDo
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

        return redirect('/')

    return render(request, 'add_todo.html')

def delete_todo_view(request, slug):
    todo = get_object_or_404(ToDo, slug__iexact=slug)
    
    if request.method == 'POST':
        todo.delete()
        
        return redirect('home')
    
    return render(request, 'confirm_delete.html', {'todo': todo})