from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
import pricesua_project.settings
from prices_app.forms import PricesForm, UserPricesForm, EditForm
from prices_app.models import ProductModel, PersonModel, PriceModel
from modules.telegram_send import send_message
from modules.site_functions import site_functions
from django.core.mail import send_mail
from django.db import connection
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.db.models import Q


def get_prices(request):
    user = request.user
    product_data = PriceModel.objects.select_related('product').order_by('-date')[:6]

    if request.method == 'POST':
        form = PricesForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            site_name = cd['site']
            price_function = site_functions.get(site_name)

            if not request.user.is_authenticated:

                user = User.objects.filter(email=cd['mail']).first()

                if not user:

                    base_username = cd['mail'].split('@')[0]
                    username = base_username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}{counter}"
                        counter += 1

                    password = get_random_string(12)
                    user = User.objects.create_user(
                        username=username,
                        email=cd['mail'],
                        password=password)

                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)

                    send_mail(
                        subject="Дякуємо за реєстрацію!",
                        message=(
                            f"Ваші реєстраційні дані:\n"
                            f"Електронна пошта: {cd['mail']}\n"
                            f"Пароль: {password}\n\n"
                            f"Щоб отримувати сповіщення в Telegram — відкрийте @priser_2025_bot та натисніть 'Start'."),
                        from_email=pricesua_project.settings.EMAIL_HOST_USER,
                        recipient_list=[cd['mail']],
                        fail_silently=False)

                else:

                    return render(request, 'prices_templates/main.html', {
                        'form': form,
                        'product_data': product_data,
                        'user': request.user,
                        'error': 'Користувач з такою поштою вже існує. Увійдіть у свій акаунт.'})

                telegram_value = cd.get('telegram', '')
                person, _ = PersonModel.objects.get_or_create(
                    user=user,
                    defaults={'telegram': telegram_value}
                )
            else:
                user = request.user
                person = getattr(user, 'person', None)

            if price_function:
                product_name, price, old_price, discount, icon, image = price_function(cd['link'])

                old_price_str = f"{old_price} UAH" if old_price else "-"
                discount_str = f"{discount}%" if discount else "-"

                message = (
                    f"🔗 {cd['link']}\n"
                    f"{'-' * 66}\n"
                    f"📦 {product_name}\n"
                    f"💰 Ціна: {price} UAH\n"
                    f"🔻 Попередня: {old_price_str}\n"
                    f"🎯 Знижка: {discount_str}"
                )

                send_mail(
                    subject="Discount information",
                    message=message,
                    from_email=pricesua_project.settings.EMAIL_HOST_USER,
                    recipient_list=[cd['mail']],
                    fail_silently=False)

                product, _ = ProductModel.objects.get_or_create(
                    link=cd['link'],
                    defaults={
                        'image': ContentFile(image, name='image.png') if image else None,
                        'icon': ContentFile(icon, name='favicon.png') if icon else None,
                        'product_name': product_name})
                product.users.add(user)

                PriceModel.objects.create(
                    price=price,
                    old_price=old_price,
                    discount=discount,
                    person=person,
                    product=product)

            return redirect('success')
    else:
        form = PricesForm()

    context = {
        'form': form,
        'product_data': product_data,
        'user': user
    }
    return render(request, 'prices_templates/main.html', context)

def product_info(request, id):
    product = ProductModel.objects.get(id=id)
    prices = PriceModel.objects.filter(product=product).order_by('-date')
    price = prices.first()
    context = {'product': product, 'prices': prices, 'price': price}
    return render(request, 'prices_templates/product_info.html', context)

def history(request):
    products = ProductModel.objects.all()
    product_data = []
    for product in products:
        latest_price = PriceModel.objects.filter(product=product).order_by('-date').first()
        product_data.append({
            'product': product,
            'price': latest_price,
        })

    context = {'product_data': product_data}
    return render(request, 'prices_templates/history.html', context)

@login_required()
def username_products(request, username):
    user = get_object_or_404(User, username=username)
    person = get_object_or_404(PersonModel, user=user)
    products = ProductModel.objects.filter(users=user).prefetch_related('prices')
    for product in products:
        latest_price = product.prices.filter(person=person).order_by('-date').first()
        product.price = latest_price

    if request.method == 'POST':
        form = UserPricesForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            site_name = cd['site']

            price_function = site_functions.get(site_name)

            if price_function:
                product_name, price, old_price, discount, icon, image = price_function(cd['link'])

                old_price_str = f"{old_price} UAH" if old_price else "-"
                discount_str = f"{discount}%" if discount else "-"

                caption = (
                    f"🔗 {cd['link']}\n"
                    f"📦 {product_name}\n"
                    f"💰 Ціна: {price} UAH\n"
                    f"🔻 Попередня: {old_price_str}\n"
                    f"🎯 Знижка: {discount_str}\n"
                )

                chat_id = person.chat_id
                if chat_id:
                    send_message(chat_id, image, caption)
                else:
                    print("Відсутній ID чату.")

                send_mail(
                    subject=f"Discount information",
                    message=caption,
                    from_email=pricesua_project.settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False)

                product, _ = ProductModel.objects.get_or_create(
                    link=cd['link'],
                    defaults={
                        'image': ContentFile(image, name='image.png') if image else None,
                        'icon': ContentFile(icon, name='favicon.png') if icon else None,
                        'product_name': product_name})

                product.users.add(user)

                PriceModel.objects.create(
                    price=price,
                    old_price=old_price,
                    discount=discount,
                    person=person,
                    product=product)

            return redirect('username_products', username=user.username)


    else:
        form = UserPricesForm()

    context = {
        'products': products,
        'user': user, 'form': form
    }
    return render(request, 'account/username_products.html', context)

@login_required()
def username_info(request, username):
    user = get_object_or_404(User, username=username)
    person = get_object_or_404(PersonModel, user=user)

    if request.method == 'POST':
        form = EditForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            telegram = cd['telegram']
            mail = cd['mail']

            user.username = username
            person.telegram = telegram
            user.email = mail

            user.save()
            person.save()

            return redirect('prices')
    else:
        form = EditForm(initial={
            'username': user.username,
            'mail': user.email,
            'telegram': person.telegram
        })

    context = {'user': user, 'form': form}
    return render(request, 'account/username_info.html', context)

@login_required()
def success(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account/success.html', context)

def contacts(request):
    return render(request, 'prices_templates/contacts.html')

def about(request):
    return render(request, 'prices_templates/about.html')








