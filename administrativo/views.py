from ast import mod
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

# importar las clases de models.py
from administrativo.models import Matricula, Estudiante
from administrativo.forms import MatriculaForm, MatriculaEditForm

# vista que permita presesentar las matriculas
# el nombre de la vista es index.

def index(request):
    # Obtiene todos los estudiantes y pre-carga sus módulos matriculados para optimizar las consultas
    estudiantes = Estudiante.objects.prefetch_related('lasmatriculas__modulo')

    # Llama al método del modelo para obtener el resumen de cada estudiante
    resumen_estudiantes = [estudiante.resumen_matriculas() for estudiante in estudiantes]

    # Prepara el contexto para enviar a la plantilla
    contexto = {
        'matriculas': Matricula.objects.select_related('estudiante', 'modulo'),  # Lista de todas las matrículas
        'resumen_estudiantes': resumen_estudiantes,                              # Datos agregados por estudiante
        'numero_matriculas': Matricula.objects.count(),                          # Número total de matrículas
        'mititulo': "Listado de matrículas"                                      # Título para la vista
    }

    # Renderiza la plantilla con el contexto
    return render(request, 'index.html', contexto)

def detalle_matricula(request, id):
    """

    """

    matricula = Matricula.objects.get(pk=id)
    informacion_template = {'matricula': matricula}
    return render(request, 'detalle_matricula.html', informacion_template)


def crear_matricula(request):
    """
    """
    if request.method=='POST':
        formulario = MatriculaForm(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save() # se guarda en la base de datos
            return redirect(index)
    else:
        formulario = MatriculaForm()
    diccionario = {'formulario': formulario}

    return render(request, 'crear_matricula.html', diccionario)

def editar_matricula(request, id):
    """
    """
    matricula = Matricula.objects.get(pk=id)
    print("----------matricula")
    print(matricula)
    print("----------matricula")
    if request.method=='POST':
        formulario = MatriculaEditForm(request.POST, instance=matricula)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = MatriculaEditForm(instance=matricula)
    diccionario = {'formulario': formulario}

    return render(request, 'crear_matricula.html', diccionario)

def detalle_estudiante(request, id):
    """

    """

    estudiante = Estudiante.objects.get(pk=id)
    informacion_template = {'e': estudiante}
    return render(request, 'detalle_estudiante.html', informacion_template)
