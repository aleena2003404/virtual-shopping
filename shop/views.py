from django.shortcuts import render
from .models import Product
from .models import Cart
# Create your views here.



def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

from django.shortcuts import render, get_object_or_404




def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def cart(request):
    cart_items = Cart.objects.all()
    return render(request, 'cart.html', {
        'cart_items': cart_items
    })
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')
from django.contrib.auth import authenticate, login

def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')