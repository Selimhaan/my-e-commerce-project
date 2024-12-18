from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import Product, Cart, Order, OrderItem
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CheckoutForm
from django.http import HttpResponseForbidden
# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product' : product})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        # Kalıcı sepet
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        # Oturum tabanlı sepet
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart_item, created = Cart.objects.get_or_create(session_key=request.session.session_key, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('product_detail', pk=product.pk)



def cart_view(request):
    # Kullanıcı oturum açmışsa kullanıcıya ait sepeti al
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        # Oturum açmamış kullanıcılar için session'daki sepete bak
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    cart_details = []
    total_price = 0

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        total_price += subtotal
        cart_details.append({
            "product": item.product,
            "quantity": item.quantity,
            "price": item.product.price,
            "subtotal": subtotal,
            "pk": item.pk,
        })

    return render(request, "store/cart.html", {
        "cart_details": cart_details,
        "total_price": total_price,
    })


def update_cart(request, pk):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, pk=pk)
        new_quantity = int(request.POST.get("quantity", 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_view')



def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    cart_item.delete()
    return redirect('cart_view')



def search_products(request):
    query = request.GET.get('q', '')
    results = []
    if query :
        results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains = query))
        return render(request, 'store/search_results.html' , {'query' : query, 'results' : results})
    
    

def filter_products(request):
    categories = Product.CATEGORY_CHOICES  
    selected_category = request.GET.get("category", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    products = Product.objects.all()

    if selected_category:
        products = products.filter(category=selected_category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, "store/filter_results.html", {
        "products": products,
        "categories": categories,  
        "selected_category": selected_category,  
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
        
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})



def logout_user(request):
    logout(request)
    return redirect('product_list')

@login_required
def add_product(request):
    if not request.user.is_staff:  # Admin olmayan kullanıcıları engelle
        return HttpResponseForbidden("You do not have permission to add products.")
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Ürünü ekleyen kullanıcı
            product.save()
            return redirect('product_list') 
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form})


@login_required
def checkout(request):
    # Kullanıcı oturum açmışsa kullanıcıya ait sepeti al
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        # Oturum açmamış kullanıcılar için session'daki sepete bak
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    # Sepet formu gönderildiyse işleme başla
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Siparişi oluştur
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
            )
            
            # Sepetteki ürünleri siparişe ekle
            for item in cart_items:
                product = item.product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity
                )
                
            # Sepeti temizle
            if request.user.is_authenticated:
                cart_items.delete()  # Kullanıcı sepetini veritabanından sil
            else:
                request.session['cart'] = []  # Oturum bazlı sepeti temizle
                
            return redirect('order_confirmation', order_id=order.id)
    
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form})


@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})