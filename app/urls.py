from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login/', auth.login),
    path('logout', auth.logout),

    path('mensaje/crear', views.mensaje_crear),
    path('mensaje/comentario', views.comentario_crear),
    path('comentario/<int:val>/borrar', views.comentario_borrar),
    path('mensaje/<int:val>/borrar', views.mensaje_borrar),
]
