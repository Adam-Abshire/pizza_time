from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Topping, Pizza


######## RENDERED WEB PAGES ###############
def login(request):
    return render(request, 'login.html')

def registration(request):
    return render(request, 'registration.html')

def menu(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'user' : this_user,
        'toppings' : Topping.objects.all(),
    }
    return render(request, 'menu.html', context)

def cart(request, pizza_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id = request.session['user_id'])
    this_pizza = Pizza.objects.get(id = pizza_id)
    context = {
        'pizza' : this_pizza,
        'user' : this_user,
    }
    return render(request, 'cart.html', context)

def success(request, pizza_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'pizza' : Pizza.objects.get(id = pizza_id),
        'user' : this_user,
    }
    return render(request, 'success.html', context)

def specific_user(request, member_id):
    if 'user_id' not in request.session:
        return redirect('/')
    the_user = User.objects.get(id=member_id)
    last_pizza_id = Pizza.objects.filter(ordered_by = User.objects.get(id = member_id)).last().id
    pizza1 = Pizza.objects.get(id = last_pizza_id)
    pizza2 = Pizza.objects.get(id = last_pizza_id-1)
    pizza3 = Pizza.objects.get(id = last_pizza_id-2)
    all_3 = [pizza1, pizza2, pizza3]
    context = {
        'user' : the_user,
        'pizza' : all_3,
    }
    return render(request, 'user.html', context)

def make_edits(request, member_id):
    if 'user_id' not in request.session:
        return redirect('/')
    the_user = User.objects.get(id=member_id)
    last_pizza_id = Pizza.objects.filter(ordered_by = User.objects.get(id = member_id)).last().id
    pizza1 = Pizza.objects.get(id = last_pizza_id)
    pizza2 = Pizza.objects.get(id = last_pizza_id-1)
    pizza3 = Pizza.objects.get(id = last_pizza_id-2)
    all_3 = [pizza1, pizza2, pizza3]
    context = {
        'user' : the_user,
        'pizza' : all_3,
    }
    return render(request, 'edit.html', context)
######## RENDERED WEB PAGES ###############
######## LOGIN & REGISTRATION #############
def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    pw_hash = bcrypt.hashpw(request.POST['pword'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        address = request.POST['address'],
        city = request.POST['city'],
        state = request.POST['state'],
        password = pw_hash,
    )
    request.session['user_id'] = new_user.id
    return redirect('/menu')

def login_user(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.loginval(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/login')
    user = User.objects.get(email = request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/menu')

def logout(request):
    request.session.flush()
    return redirect('/')
######## LOGIN & REGISTRATION #############
######## EDIT USER INFORMATION ############
def edit_user(request, member_id):
    if request.method == 'POST':
        errors = User.objects.editval(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect(f'/user/{member_id}')
        curr_user = User.objects.get(id=member_id)
        curr_user.first_name = request.POST['first_name']
        curr_user.last_name = request.POST['last_name']
        curr_user.email = request.POST['email']
        curr_user.address = request.POST['address']
        curr_user.city = request.POST['city']
        curr_user.state = request.POST['state']
        curr_user.save()
        return redirect(f'/user/{member_id}')
    return redirect(f'/user/{member_id}')
######## EDIT USER INFORMATION ############
######## CREATE NEW PIZZA & REORDER PIZZA##
def create_pizza(request):
    if request.method == 'POST':
        curr_user = User.objects.get(id = request.session['user_id'])
        curr_price = 0
        topping_amount = 0
        topping_list = request.POST.getlist('topping')
        for topping in topping_list:
            topping_amount += 1
        curr_price += topping_amount * .75
        this_pizza = Pizza.objects.create(
            method = request.POST['method'],
            size = request.POST['size'],
            crust = request.POST['crust'],
            ordered_by = curr_user,
        )
        this_pizza.save()
        if this_pizza.method == "Delivery":
            curr_price += 2.99
        if this_pizza.crust == "Chicago Style Deep Dish":
            curr_price += 1.99
        if this_pizza.size == "Small":
            curr_price += 12.99
        elif this_pizza.size == "Medium":
            curr_price += 14.99
        else:
            curr_price += 16.99
        curr_price = str(round(curr_price, 2))
        this_pizza.price = curr_price
        this_pizza.save()
        curr_toppings = request.POST.getlist('topping')
        for each_topping_id in curr_toppings:
            this_topping = Topping.objects.get(id=each_topping_id)
            this_pizza.toppings.add(this_topping)
            this_pizza.save()
        pizza_id = this_pizza.id
    return redirect(f'/cart/{pizza_id}')

def reorder(request, pizza_id):
    this_pizza = Pizza.objects.get(id=pizza_id)
    curr_user = User.objects.get(id = request.session['user_id'])
    curr_pizza = Pizza.objects.create(
        method = this_pizza.method,
        size = this_pizza.size,
        crust = this_pizza.crust,
        ordered_by = curr_user,
        price = this_pizza.price,
    )
    for each_topping in this_pizza.toppings.all():
        this_topping = Topping.objects.get(id = each_topping.id)
        curr_pizza.toppings.add(this_topping)
    curr_pizza.save()
    pizza_id = curr_pizza.id
    return redirect(f'/cart/{pizza_id}')
######## CREATE NEW PIZZA & REORDER PIZZA############
################LIKE & UNLIKE########################
def favorite(request, pizza_id):
    curr_pizza = Pizza.objects.get(id=pizza_id)
    curr_user = User.objects.get(id = request.session['user_id'])
    curr_pizza.favorited_by.add(curr_user)
    curr_pizza.save()
    user_id = curr_user.id
    return redirect(f'/user/{user_id}')

def unfavorite(request, pizza_id):
    curr_pizza = Pizza.objects.get(id=pizza_id)
    curr_user = User.objects.get(id= request.session['user_id'])
    curr_pizza.favorited_by.remove(curr_user)
    curr_pizza.save()
    user_id = curr_user.id
    return redirect(f'/user/{user_id}')
################LIKE & UNLIKE########################