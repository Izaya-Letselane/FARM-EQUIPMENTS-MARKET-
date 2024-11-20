from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import json
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
#Search/query multiple items on search bar
from django.db.models import Q
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

from .models import Product, Profile
# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
def shop(request):
    return render(request, 'shop.html', {})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(
                request, "User Profile Has Been Updated Successfully")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, "You must be logged in....")
        return redirect('home')

##################################################################


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated...")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
    
def update_info(request):
     if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        #Get current user shipping info
        #shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #get user's original form
        form = UserInfoForm(request.POST or None, instance=current_user)
        #get user's shipping form
        #shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid():
            form.save()
            
            messages.success(
                request, "User Information Has Been Updated Successfully")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
     else:
        messages.success(request, "You must be logged in....")
        return redirect('home')


def about(request):
    return render(request, 'about.html', {})


def checkout(request):
     cart = Cart(request)
     totals = cart.cart_total()
     
     return render(request, 'checkout.html', {'totals': totals})
   
def invoice(request):
    return render(request, 'invoice.html')

def cartitem(request):
    return render(request, 'cartItem.html', {})


def product(request, pk):
    product = Product.objects.get(id=pk)
    #prods= Product.objects.all()
    
        
    return render(request, 'product.html', {'product': product})#,{'prods': prods})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #deal with shopping cart functionalities
            current_user = Profile.objects.get(user__id=request.user.id) 
            #obtain users' saved cart from the database
            saved_cart = current_user.prev_card
            #convert database string to python Dictionary
            if saved_cart:
                #convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #add the loaded cart dictionar to our session
                cart = Cart(request)
                # loop through cart and add items from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            
            messages.success(request, ("You have logged in !!"))
            return redirect('home')
        else:
            messages.success(request, ("You have entered wrong details !!"))
            return redirect('login')
    else:

        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Logged out..."))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("User Account Created Successfully...Fill out the information Below"))
            #return redirect('home')
            return redirect('update_info')
        else:
            messages.success(
                request, ("There was a problem registering please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def search(request):
    #check if they filled the form
    if request.method == "POST":
        searched = request.POST['searched']
        #Query the product DB Model
        searched = Product.objects.filter(Q(productName__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "Unfortunately we don't have that product!!")
            return render(request, 'search.html', {})
        else: 
           
            return render(request, "search.html", {"searched": searched})
    else:
        return render(request, 'search.html', {})