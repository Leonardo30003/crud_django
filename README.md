# CRUD en Django (Crear, Recuperar, Actualizar y Borrar) usando vistas basadas en clases.

Utilizaremos Django y vistas basadas en clases para desarrollar una aplicación que permita crear una nueva tarea, recuperar una lista de tareas o una tarea individual, actualizar una tarea y eliminar una tarea. 

### Step 1: Crear una app "tasks" y agregarla a INSTALLED_APPS

Primero ejecuta `python manage.py startapp tasks` para crear una nueva aplicación llamada "tasks" y luego añádela a INSTALLED_APPS en `settings.py`.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
]
```

A continuación, añada las urls de la aplicación a las urls del proyecto.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls'))
]

```

### Paso 2: crear el modelo de Tarea y el formulario asociado

Nuestro modelo de Tarea es muy simple. También utilizamos Forms para crear un Formulario de Tareas que luego será necesario para crear o actualizar una tarea.

```python
# tasks/models.py

from django.db import models


# Create your models here.

class Status(models.TextChoices):
    UNSTARTED = 'u', "Tareas no iniciadas"
    ONGOING = 'o', "En Curso"
    FINISHED = 'f', "Finalizada"


class Task(models.Model):
    name = models.CharField(verbose_name="Nombre de la Tarea", max_length=65, unique=True)
    status = models.CharField(verbose_name="Estado de la Tarea", max_length=1, choices=Status.choices)

    def __str__(self):
        return self.name


# tasks/forms.py
#-*- coding:utf-8 -*-
from .models import Task
from django import forms

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"
```

### Step 3:  Escribir URLConfs y vistas basadas en clases

Crearemos 5 urls y 5 vistas basadas en clases para tratar las actividades CRUD.

``` from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')
```

```python
# tasks/views.py

# Class Based Views
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')
```

### Step 4:  Crear las plantillas

Creamos 4 plantillas: `task_list.html`, `task_detail.html`, `task_form.html` y `task_confirm_delete.html`. La vista `task_form.html` será compartida por `task_create` y `task_update`. 

```
# tasks/templates/tasks/task_list.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Task List</title>
</head>
<body>
<h3>Task List</h3>
{% for task in tasks %}
    <p>{{ forloop.counter }}. {{ task.name }} - {{ task.get_status_display }}
        (<a href="{% url 'tasks:task_update' task.id %}">Update</a> |
        <a href="{% url 'tasks:task_delete' task.id %}">Delete</a>)
    </p>
{% endfor %}

<p> <a href="{% url 'tasks:task_create' %}"> + Add A New Task</a></p>
</body>
</html>

# tasks/templates/tasks/task_detail.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Task Detail</title>
</head>
<body>
<p> Task Name: {{ task.name }} | <a href="{% url 'tasks:task_update' task.id %}">Update</a> |
    <a href="{% url 'tasks:task_delete' task.id %}">Delete</a>
</p>
<p> Task Status: {{ task.get_status_display }} </p>
<p> <a href="{% url 'tasks:task_list' %}">View All Tasks</a> |
    <a href="{% url 'tasks:task_create'%}">New Task</a>
</p>
</body>
</html>

# tasks/templates/tasks/task_form.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% if object %}Edit Task {% else %} Create New Task {% endif %}</title>
</head>
<body>
<h3>{% if object %}Edit Task {% else %} Create New Task {% endif %}</h3>
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <p><input type="submit" class="btn btn-success" value="Submit"></p>
    </form>
</body>
</html>
```

### Step 5:  Ejecutar el proyecto

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```