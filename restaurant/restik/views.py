from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login   
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import *
from .forms import *


def add_dish_basket(request, id):
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import Product

def add_to_cart(request, id):
    """
    View для додавання продукту до корзини.
    
    Args:
        request: HttpRequest об'єкт, який містить дані про запит користувача.
        product_id: ID продукту, який потрібно додати до корзини.
    
    Returns:
        JsonResponse або перенаправлення на попередню сторінку.
    """
    # Отримуємо продукт по його id або повертаємо 404, якщо не знайдено
    product = get_object_or_404(Food, id=id)
    
    # Ініціалізуємо корзину в сесії, якщо вона ще не існує
    cart = request.session.get('cart', {})
    if str(id) in cart:
        # Якщо продукт вже в корзині, збільшуємо кількість
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1
        }
    request.session['cart'] = cart
    previous_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(previous_url)



def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Ви не авторизовались.")
        
        if not request.user.is_staff:
            return HttpResponseForbidden("Hey buddy I think you got the wrong door, leather club’s two blocks down")
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def food_list(request):
    food = Food.objects.all()
    return render(request, 'food_list.html', {'dishes': food, 'category': "страви"})


@staff_required
def new_food(request):
    if request.method == 'POST':
        form = FoodCreationForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.save()  # Сохранение ManyToMany поля
            return redirect('food_list')
    else:
        form = FoodCreationForm()

    return render(request, 'new_food.html', {'form': form})


@staff_required
def edit_food(request, id):
    dish = get_object_or_404(Food, id=id)
    if request.method == 'POST':
        form = FoodCreationForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('food_list')  # Редірект на список страв
    else:
        form = FoodCreationForm(instance=dish)
    return render(request, 'dish_edit.html', {'form': form})


@staff_required
def delete_food(request, id):
    food = Food.objects.get(id = id)
    food.delete()
    return redirect('food_list')


def filtered_food_list(request, category):
    dishes = Food.objects.filter(category=category)
    category_name = dict(Food.STATUS_CHOICES).get(category, 'Невідома категорія') 
    return render(request, 'food_list.html', {'dishes': dishes, 'category': category_name})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем пользователя в базе данных
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} был успешно создан!')
            return redirect('login')  # Перенаправляем пользователя на страницу входа
        else:
            messages.error(request, 'Исправьте ошибки в форме регистрации.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)  # Выход из системы
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('food_list')  # Перенаправляем на страницу входа


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # Проверка пользователя
        if user is not None:
            login(request, user)  # Вход пользователя в систему
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('food_list')  # Перенаправляем на главную страницу или другую целевую страницу
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'login.html')





