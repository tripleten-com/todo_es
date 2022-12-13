from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from .forms import TaskCreateForm
from .models import Task


class Home(CreateView):
    """Форма добавления задания."""
    template_name = 'tasks/home.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('tasks:task_added')


class TaskList(LoginRequiredMixin, ListView):
    """Список всех доступных заданий."""
    login_url = '/admin/login/'
    model = Task
    template_name = 'tasks/task_list.html'



class TaskDetail(LoginRequiredMixin, DetailView):
    """Задание подробно."""
    login_url = '/admin/login/'
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskAddSuccess(TemplateView):
    """Задание успешно добавлено."""
    template_name = 'tasks/added.html'
