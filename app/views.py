from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import *
from datetime import datetime, time, timedelta
from django.utils import timezone
import re

@login_required
def index(request):
    context = {
        'mensajes': Mensaje.objects.all(),
        'comentarios': Comentario.objects.all(),
    }
    return render(request, 'index.html', context)

@login_required
def mensaje_crear(request):
    print(request.POST)
    errors= Mensaje.objects.validador_basico_mensaje(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        mensaje_creado = request.POST['mensaje']
        user_id_creador = request.session['usuario']['id']

        mensaje = Mensaje.objects.create(
            mensaje = mensaje_creado, 
            user = User.objects.get(id = user_id_creador),
        )
        messages.success(request, "Mensaje agregado correctamente")
        return redirect(f"/")

def calculate_minutos(fecha):
    today = timezone.now()
    print(today, "today")
    print(fecha, "fecha")
    print("años", (today.year - fecha.year), (today.year - fecha.year)*365*24*60)
    print("meses", (today.month - fecha.month), (today.month - fecha.month)*30*24*60)
    print("dias", (today.day - fecha.day), (today.day - fecha.day)*24*60)
    print("horas", (today.hour-fecha.hour), (today.hour-fecha.hour)*60)
    print("minutos", (today.minute-fecha.minute))
    resultado = (today.year - fecha.year)*365*24*60 + (today.month - fecha.month)*30*24*60 + (today.day - fecha.day)*24*60 + (today.hour-fecha.hour)*60 + (today.minute-fecha.minute)
    print(resultado)
    return resultado

@login_required
def mensaje_borrar(request, val):
    errors = {}
    print(request.GET, 'Entró a borrar mensaje')
    borr = Mensaje.objects.get(id = val)
    print("Aqui se va a borrar el mensaje ID=", val)
    calc = calculate_minutos(borr.created_at)
    if calc > 30:
        messages.warning(request, "No se borró el mensaje. Tiempo expirado máximo 30 min")
    else: 
        print("Autorizado para borrar el mensaje")
        messages.success(request, "Mensaje borrado exitosamente")
        borr.delete()
    return redirect("/")

@login_required
def comentario_crear(request):
    print(request.POST)

    errors= Comentario.objects.validador_basico_comentario(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        comentario_creado = request.POST['comentario']
        id_mensaje = request.POST['id_mensaje_comentario']
        comentario_user_id = request.session['usuario']['id']

        comentario = Comentario.objects.create(
            comentario = comentario_creado, 
            user = User.objects.get(id=comentario_user_id),
            mensaje = Mensaje.objects.get(id=id_mensaje),
        )
        messages.success(request, "Comentario agregado correctamente")
        return redirect(f"/")

@login_required
def comentario_borrar(request, val):
    print(request.GET)
    borr = Comentario.objects.get(id = val)
    print("Aqui se va a borrar el comentario ID=", val)
    calc = calculate_minutos(borr.created_at)
    if calc > 30:
        messages.warning(request, "No se borró el comentario. Tiempo expirado máximo 30 min")
    else: 
        print("Autorizado para borrar el comentario")
        messages.success(request, "Comentario borrado exitosamente")
        borr.delete()
    return redirect("/")