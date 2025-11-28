from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Producto, Venta, Cliente


# -----------------------------
# ROLES
# -----------------------------
def es_admin(user):
    return user.is_superuser


def es_vendedor(user):
    return not user.is_superuser


# -----------------------------
# LOGIN
# -----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Redirección según rol
            if user.is_superuser:
                return redirect('home')  # Admin va al HOME
            else:
                return redirect('ventas')  # Vendedor va directo a VENTAS

        messages.error(request, "Credenciales incorrectas.")
        return redirect('login')

    return render(request, "login.html")


# -----------------------------
# LOGOUT
# -----------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------------
# HOME – SOLO ADMIN
# -----------------------------
@login_required
@user_passes_test(es_admin, login_url='/ventas/')
def home(request):
    total_productos = Producto.objects.count()
    total_ventas = Venta.objects.count()
    productos_bajo_stock = Producto.objects.filter(stock__lt=10).count()
    
    context = {
        'total_productos': total_productos,
        'total_ventas': total_ventas,
        'productos_bajo_stock': productos_bajo_stock,
    }
    return render(request, "home.html", context)


# -----------------------------
# PRODUCTOS – ADMIN Y VENDEDOR
# -----------------------------
@login_required
def productos(request):
    lista = Producto.objects.all()
    return render(request, "productos.html", {"productos": lista})


# -----------------------------
# INVENTARIO – SOLO ADMIN
# -----------------------------
@login_required
@user_passes_test(es_admin, login_url='/')
def inventario(request):
    lista = Producto.objects.all()
    return render(request, "inventario.html", {"productos": lista})


# -----------------------------
# VENTAS – ADMIN Y VENDEDOR
# -----------------------------
@login_required
def ventas(request):
    # Si es vendedor, solo ve sus propias ventas
    if request.user.is_superuser:
        lista = Venta.objects.all()
    else:
        lista = Venta.objects.filter(vendedor=request.user)
    
    return render(request, "ventas.html", {"ventas": lista})


# -----------------------------
# CLIENTES – TODOS
# -----------------------------
@login_required
def clientes(request):
    lista = Cliente.objects.all()
    return render(request, "clientes.html", {"clientes": lista})