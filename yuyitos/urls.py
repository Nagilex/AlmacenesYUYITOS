from django.contrib import admin
from django.urls import path
from mainApp import views

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # Login/Logout
    path('', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    # Home (Solo Admin)
    path('home/', views.home, name="home"),

    # Productos e Inventario
    path('productos/', views.productos, name="productos"),
    path('inventario/', views.inventario, name="inventario"),

    # Ventas y Clientes
    path('ventas/', views.ventas, name="ventas"),
    path('clientes/', views.clientes, name="clientes"),
]

