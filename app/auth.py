from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import *

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect("/login")

def login(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "first_name" : log_user.first_name,
                    "last_name" : log_user.last_name,
                    "email": log_user.email,
                }

                request.session['usuario'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")

        return redirect("/login")
    else:
        return render(request, 'login.html')


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['register_first_name'] =  request.POST['first_name']
            request.session['register_last_name'] =  request.POST['last_name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_first_name'] = ""
            request.session['register_last_name'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email=request.POST['email'],
                password=password_encryp,
            )

            messages.success(request, "El usuario fue agregado con exito.")
            
            user = {
                "id" : usuario_nuevo.id,
                "first_name" : usuario_nuevo.first_name,
                "last_name" : usuario_nuevo.last_name,
                "email": usuario_nuevo.email
            }
            request.session['usuario'] = user
            return redirect("/")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')
