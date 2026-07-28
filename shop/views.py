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
from django.shortcuts import get_object_or_404, redirect

def remove_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('cart')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        product = item.product

        product.stock -= item.quantity
        product.save()

    return redirect('success')
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Cart, OrderItem

def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():

            # Save Order
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            order.save()

            # Save Order Items and Update Stock
            for item in cart_items:

                # Save each product in OrderItem table
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                # Reduce Product Stock
                # Reduce Product Stock
                product = item.product
                if product.stock < item.quantity:
                    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'error': f"{product.name} is out of stock."
    })
                product.stock -= item.quantity
                product.save()

            # Clear Cart
            cart_items.delete()

            return redirect('order_success')

    else:
        form = OrderForm()

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })
def order_success(request):
    return render(request, 'order_success.html')