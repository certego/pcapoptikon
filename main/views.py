from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main.models import *
from main.forms import *

@login_required
def tasks(request, status='any', pagination_start=0, pagination_len=50):
    pagination_start    = int(pagination_start)
    pagination_len      = int(pagination_len)

    context = {
        'active_tab':   'tasks',
        'tasks':        Task.objects.all().order_by('-id')[pagination_start:pagination_start+pagination_len],
        'total':        Task.objects.all().count(),
        'start':        pagination_start,
        'len':          pagination_len,
    }

    return render(request, 'main/tasks.html', context)

@login_required
def new_task(request):
    context = {
        'active_tab':   'new_task',
        'form':         TaskForm(request.POST or None),
    }

    if request.method == 'POST':
        if context['form'].is_valid():

            saved_task = context['form'].save()

            return HttpResponseRedirect(
                reverse(
                    'main:tasks',
                    kwargs={'task_id': saved_task.id}
                )
            )

    return render(request, 'main/new_task.html', context)

@login_required
def task(request, task_id):
    context = {
        'active_tab':   'tasks',
        'task':         get_object_or_404(Task, pk=task_id),
    }

    return render(request, 'main/task.html', context)
