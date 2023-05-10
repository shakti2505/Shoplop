from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages
from. forms import CustomerProfileForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
 def get(self, request):
  total_items =0
  topwears = Product.objects.filter(catogary='TW')
  bottomwears = Product.objects.filter(catogary='BW')
  mobiles = Product.objects.filter(catogary='M')
  if request.user.is_authenticated:
   total_items = len(Cart.objects.filter(user = request.user))

  return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears':bottomwears,'mobiles':mobiles, 'total_items':total_items })


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
 def get(self, request, pk):
  total_items = 0
  product = Product.objects.get(pk=pk)
  # cheking if selected product already in cart or not ?
  item_already_in_cart = False
  if request.user.is_authenticated:
    total_items = len(Cart.objects.filter(user=request.user))
    item_already_in_cart = Cart.objects.filter(Q(product =product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart': item_already_in_cart, 'total_items':total_items})
  
  
  
@login_required()
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()

 return redirect('/show-cart/')

@login_required()
def show_cart(request):
 if request.user.is_authenticated:
  total_items = 0
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping = 0.0
  totalamount = 0.0
  
  cart_product = [p for p in Cart.objects.all() if p.user==user]
  if cart_product:
   for p in cart_product:
    shipping = 120.00
    tempamount = (p.quantity*p.product.discounted_price)
    amount += tempamount
    totalamount = amount+shipping
    total_items = len(Cart.objects.filter(user=user))
   return render(request, 'app/addtocart.html', {"carts":cart, 'total_amount':totalamount, 'amount':amount, 'shipping':shipping,'total_items':total_items})
  else:
    return render(request, 'app/empty_cart.html')


 

def plus_cart(request):
  if request.method  =="GET":
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.quantity+=1
   c.save()
   amount = 0.0
   shipping = 120.0
   cart_product = [p for p in Cart.objects.all() if p.user==request.user]
   for p in cart_product:
    tempamount = (p.quantity*p.product.discounted_price)
    amount += tempamount

  data = {
    'quantity':c.quantity,
    'amount': amount,
    'totalamount':amount + shipping
    }
  return JsonResponse(data)


def minus_cart(request):
  if request.method  =="GET":
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.quantity-=1
   c.save()
   amount = 0.0
   shipping = 120.0
   cart_product = [p for p in Cart.objects.all() if p.user==request.user]
   for p in cart_product:
    tempamount = (p.quantity*p.product.discounted_price)
    amount += tempamount

  data = {
    'quantity':c.quantity,
    'amount': amount,
    'totalamount':amount +  shipping
    }
  return JsonResponse(data)


def remove_cart(request):
  if request.method  =="GET":
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.delete()
   amount = 0.0
   shipping = 120.0
   cart_product = [p for p in Cart.objects.all() if p.user==request.user]
   for p in cart_product:
    tempamount = (p.quantity*p.product.discounted_price)
    amount += tempamount

  data = {
    'amount': amount,
    'totalamount': amount + shipping
    }
  return JsonResponse(data)
    
def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
 add  = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required()
def orders(request):
 user  = request.user
 orders = OrderPlaced.objects.filter(user=user)
 return render(request, 'app/orders.html', {'orders':orders})


@login_required()
def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(catogary='M')
 elif data=="Apple" or data == "Samsung":
  mobiles = Product.objects.filter(catogary='M').filter(brand=data)
 elif data=='below':
  mobiles = Product.objects.filter(catogary='M').filter(discounted_price__lt=20000)
 elif data=='above':
  mobiles = Product.objects.filter(catogary='M').filter(discounted_price__gt=25000)
  
 total_items  = 0
 if request.user.is_authenticated:
  total_items = len(Cart.objects.filter(user=request.user))


 return render(request, 'app/mobile.html', {'mobiles': mobiles, 'total_items':total_items})


def laptop(request, data=None):
 if data== None:
  laptop = Product.objects.filter(catogary='L')
 elif data=='Apple' or data=='Vivo' or data=="Lenovo" or data=="HP" or data=="Asus":
  laptop = Product.objects.filter(catogary="L").filter(brand=data)
 elif data =='below':
  laptop = Product.objects.filter(catogary="L").filter(discounted_price__lt=55000)
 elif data =='above':
  laptop = Product.objects.filter(catogary="L").filter(discounted_price__gt=35000)
 total_items  = 0
 if request.user.is_authenticated:
  total_items = len(Cart.objects.filter(user=request.user))

 return render(request, "app/laptop.html", {'laptop':laptop, 'total_items':total_items})


def topwear(request, data=None):
 if data == None:
  topwear = Product.objects.filter(catogary='TW')  
 elif data == 'below':
  topwear = Product.objects.filter(catogary='TW').filter(discounted_price__lt=1000)
 elif data == 'above':
  topwear = Product.objects.filter(catogary='TW').filter(discounted_price__gt=1000)
 total_items  = 0
 if request.user.is_authenticated:
  total_items = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/topwear.html', {'topwear':topwear, 'total_items':total_items})

def bottomwear(request, data=None):
 if data == None:
  bottomwear = Product.objects.filter(catogary='BW')  
 elif data == 'below':
  bottomwear = Product.objects.filter(catogary='BW').filter(discounted_price__lt=1000)
 elif data == 'above':
  bottomwear = Product.objects.filter(catogary='BW').filter(discounted_price__gt=1000)

  total_items  = 0
 if request.user.is_authenticated:
  total_items = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/bottomwear.html', {'bottomwear':bottomwear, 'total_items':total_items})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')\

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
 

 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'congratulations!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form':form})
 
@login_required()
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_item = Cart.objects.filter(user=user)
 amount = 0
 shipping= 120.0
 total_amount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user==request.user]
 if cart_product:
  for p in cart_product:
    tempamount = (p.quantity*p.product.discounted_price)
    amount += tempamount
  total_amount = amount+ shipping
 return render(request, 'app/checkout.html', {'add':add, "total_amount": total_amount, 'cart_item':cart_item})


@login_required()
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 #extracting Customer object using custid
 customer = Customer.objects.get(id=custid)
 # extracting cart of current user 
 cart = Cart.objects.filter(user=user)
# saving current user's cart object in OrderPlace module 
 for c_item in cart:
  OrderPlaced(user = user, customer=customer, product = c_item.product, quantity = c_item.quantity).save()
  #and deleting them from current user's cart
  messages.success(request,  'congratulations!! Your order is placed.')
  c_item.delete()
 return redirect("orders")



 
 
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
 

 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr =request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr,name =name, locality=locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulations!! profile updated successfully!!')

  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
