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
def index(request):
    return render(request, 'index.html')
from .models import Order

def checkout(request):

    if request.method == 'POST':

        Order.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            total_amount=0
        )

        return redirect('success')

    return render(request,'checkout.html')
def success(request):
    return render(request,'success.html')
from .models import Product, Category

def home(request):
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })
from .models import Product, Cart

# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)

#     Cart.objects.create(
#         user=request.user,
#         product=product,
#         quantity=1
#     )

#     return redirect('cart')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()

    return redirect('cart')