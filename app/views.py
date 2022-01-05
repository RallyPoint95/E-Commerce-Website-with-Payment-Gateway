from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View 
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # for function based view
from django.utils.decorators import method_decorator  # for class based view

#def home(request):
# return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')

        return render(request, 'app/home.html', {
            'topwears':topwears, 'bottomwears':bottomwears, 'mobile':mobile
        })

#def product_detail(request):
# return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    prod_id = Product.objects.get(id=product_id) #for creating instance of product id otherwise it will give you an error
    Cart(user=user, product=prod_id).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amt = 0.0
        shipping_amt = 70.0
        total_amt = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.discounted_price)
                amt += temp_amt
                total_amt = amt + shipping_amt
            return render(request, 'app/addtocart.html', {'carts':cart,'total_amt':total_amt, 'amt':amt, 'shipping_amt':shipping_amt})
        else:
            return render(request, 'app/emptycart.html')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amt = 0.0
        shipping_amt = 70.0
        total_amt = 0.0
        user = request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amt = (p.quantity * p.product.discounted_price)
            amt += temp_amt
            total_amt = amt + shipping_amt

        data = {
            'quantity': c.quantity,
            'amt': amt,
            'total_amt':total_amt,
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amt = 0.0
        shipping_amt = 70.0
        total_amt = 0.0
        user = request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amt = (p.quantity * p.product.discounted_price)
            amt += temp_amt
            total_amt = amt + shipping_amt

        data = {
            'quantity': c.quantity,
            'amt': amt,
            'total_amt':total_amt,
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        #c.quantity -= 1
        c.delete()
        amt = 0.0
        shipping_amt = 70.0
        total_amt = 0.0
        user = request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amt = (p.quantity * p.product.discounted_price)
            amt += temp_amt
            total_amt = amt + shipping_amt

        data = {
            'quantity': c.quantity,
            'amt': amt,
            'total_amt':total_amt,
        }
        return JsonResponse(data)

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

#def profile(request):
# return render(request, 'app/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

#def change_password(request):
# return render(request, 'app/changepassword.html')

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Dell' or data == 'Asus' or data == 'Lenovo' or data == 'Apple':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=70000)  #__lt it is less than
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=70000)   #__gt it is greater than
    elif data == 'above85000':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=85000) 
    return render(request, 'app/laptop.html', {'laptops':laptops})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)  #__lt it is less than
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=5000)   #__gt it is greater than
    elif data == 'above10000':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000) 
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def topwears(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Xemberg' or data == 'Buffalo':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=500)  #__lt it is less than
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)   #__gt it is greater than
    elif data == 'above600':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=600) 
    return render(request, 'app/topwears.html', {'topwears':topwears})

def bottomwears(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Denim' or data == 'Lee':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=600)  #__lt it is less than
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=700)   #__gt it is greater than
    elif data == 'above800':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=800) 
    return render(request, 'app/bottomwears.html', {'bottomwears':bottomwears})

#def login(request):
# return render(request, 'app/login.html')

#def customerregistration(request):
# return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
       form = CustomerRegistrationForm(request.POST)
       if form.is_valid():
           messages.success(request, 'Congratulations!! You Registered Successfully. Kindly Login Now!')
           form.save()
       return render(request, 'app/customerregistration.html', {'form':form}) 

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    #discounted_price = Product.objects.filter(user=user)
    amt = 0.0
    shipping_amt = 70.0
    total_amt = 0.0
    user = request.user
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            temp_amt = (p.quantity * p.product.discounted_price)
            amt += temp_amt
        total_amt = amt + shipping_amt
    return render(request, 'app/checkout.html', {'add':add, 'total_amt':total_amt, 'cart_items':cart_items, 'amt':amt, 'shipping_amt':shipping_amt})

@login_required # this will restrict the user if he/she try to access the profile without logging
def payment_done(request):  #function based
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

@method_decorator(login_required, name='dispatch') # this will restrict the user if he/she try to access the profile without logging
class ProfileView(View):                           #class based
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully !!')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
