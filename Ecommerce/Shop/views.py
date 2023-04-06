from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product,Cart, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse



# Create your views here.
#def home(request):
#     return render(request, 'Shop/home.html')

class ProductView(View):
    def get(self, request):
        totalitem = 0
        gentspants = Product.objects.filter(category = 'GP')
        borkhas = Product.objects.filter(category = 'BK')
        babyfashions = Product.objects.filter(category = 'BF')
        if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'Shop/home.html', {'gentspants':gentspants, 'borkhas':borkhas, 'babyfashions': babyfashions, 'totalitem':totalitem})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('quary')
        totalitem =0
        if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
        if query:
            product = Product.objects.filter(title__icontains=query)
            return render(request, 'Shop/search.html', {'product': product, 'totalitem':totalitem})
        else:
            print('This product is not available')
            return render(request, 'Shop/search.html', {'totalitem':totalitem})
#def product_detail(request):
# return render(request, 'Shop/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'Shop/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})




@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
       if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 5.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        totalitem =0
        if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'Shop/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'Shop/emptycart.html')


@login_required
def gift_card(request):
       if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 5.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        totalitem =0
        if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'Shop/giftcard.html', {'amount':amount,'totalitem':totalitem})


@login_required
def delivery_dtl(request):
       if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 5.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        totalitem =0
        if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'Shop/delivery_dtl.html', {'amount':amount,'totalitem':totalitem})
     

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        amount = 0.0
        shipping_amount = 5.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data={
            'quantity': c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }

        return JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        shipping_amount = 5.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data={
            'quantity': c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 5.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data={
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }

        return JsonResponse(data)



def buy_now(request):
 return render(request, 'Shop/buynow.html')

# def profile(request):
# return render(request, 'Shop/profile.html')
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem =0
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'Shop/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})

   
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            division = form.cleaned_data['division']
            district = form.cleaned_data['district']
            thana = form.cleaned_data['thana']
            villorroad = form.cleaned_data['villorroad']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, division=division,district=district, thana=thana, villorroad=villorroad, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Profile Updated Successfully')
        return render(request, 'Shop/profile.html', {'form':form, 'active':'btn-primary'}) 
    

#def address(request):
# return render(request, 'Shop/address.html')
@login_required
def address(request):
    add = Customer.objects.filter(user = request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'Shop/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 totalitem =0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'Shop/orders.html', {'order_placed':op, 'totalitem':totalitem})

#def change_password(request):
# return render(request, 'Shop/changepassword.html')

#def lehenga(request):
# return render(request, 'Shop/lehenga.html')

def lehenga(request, data =None):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        lehengas = Product.objects.filter(category = 'L')
    elif data == 'lubnan' or data == 'infinity': 
        lehengas = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        lehengas = Product.objects.filter(category='L').filter(discounted_price__lt=10000)
    elif data == 'above':
        lehengas = Product.objects.filter(category='L').filter(discounted_price__gt=10000)
    return render(request, 'Shop/lehenga.html', {'lehengas':lehengas, 'totalitem':totalitem})



def saree(request, data =None):
    totalitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        sarees = Product.objects.filter(category = 'S')
    elif data == 'lubnan' or data == 'She'  or data == 'Shah-E-Nur': 
        sarees = Product.objects.filter(category='S').filter(brand=data)
    elif data == 'below':
        sarees = Product.objects.filter(category='S').filter(discounted_price__lt=1500)
    elif data == 'above':
        sarees = Product.objects.filter(category='S').filter(discounted_price__gt=1499)
    return render(request, 'Shop/saree.html', {'sarees':sarees, 'totalitem':totalitem})
#def login(request):
 #    return render(request, 'Shop/login.html')

#def customerregistration(request):
# return render(request, 'Shop/customerregistration.html')

class CustomerRegistrationView(View):
   def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'Shop/customerregistration.html',{'form':form})
   
   def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
           messages.success(request, 'Congratulations! Successfully Registration Done.')
           form.save()
        return render(request, 'Shop/customerregistration.html',{'form':form})
   
@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 5.0
 totalamount = 0.0
 totalitem =0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
    totalamount = amount + shipping_amount
 return render(request, 'Shop/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'totalitem': totalitem})


#payment_done
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid) 
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


