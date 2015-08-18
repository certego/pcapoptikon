from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from main.models import *
from main.forms import *

@login_required
def tasks(request):
    context = {
        'active_tab':   'tasks',
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
def task(request, task_id=None):
    context = {
        'active_tab':   'tasks',
        'task':         get_object_or_404(Task, pk=task_id),
    }

    return render(request, 'main/task.html', context)
