from django.db import models


# Create your models here.

class Status(models.TextChoices):
    UNSTARTED = 'u', "Curso no iniciado"
    ONGOING = 'o', "En Curso"
    FINISHED = 'f', "Finalizada"


class Task(models.Model):
    name = models.CharField(verbose_name="Nombre del Curso", max_length=65, unique=True)
    status = models.CharField(verbose_name="Estado del Curso", max_length=1, choices=Status.choices)
    """descripcion = models.CharField(verbose_name="Descripccion del curso", max_length=65, unique=False)
    date = models.CharField(verbose_name="Fecha del curso", max_length=65, unique=False)"""
    #Estos campos no me permite visualizar
    
   

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