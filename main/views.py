from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
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
    }

    if request.method == 'POST':
        context['form'] = TaskForm(request.POST or None, request.FILES)
        if context['form'].is_valid():
            saved_task = context['form'].save(commit=False)
            saved_task.user = request.user
            saved_task.save()
            context['form'].save_m2m()

            return HttpResponseRedirect(
                reverse('main:tasks')
            )
    else:
        context['form'] = TaskForm(None)

    return render(request, 'main/new_task.html', context)

@login_required
def task(request, task_id):
    context = {
        'active_tab':   'tasks',
        'task':         get_object_or_404(Task, pk=task_id),
    }

    return render(request, 'main/task.html', context)
