from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from .forms import TaskCreateForm
from .models import Task


class Home(CreateView):
    """Formulario para añadir una tarea."""
    template_name = 'tasks/home.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('tasks:task_added')


class TaskList(LoginRequiredMixin, ListView):
    """Lista de todas las tareas disponibles."""
    login_url = '/admin/login/'
    model = Task
    template_name = 'tasks/task_list.html'



class TaskDetail(LoginRequiredMixin, DetailView):
    """Detalles de la tarea."""
    login_url = '/admin/login/'
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskAddSuccess(TemplateView):
    """La tarea se agregó correctamente."""
    template_name = 'tasks/added.html'
