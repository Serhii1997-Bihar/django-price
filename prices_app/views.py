from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
import pricesua_project.settings
from prices_app.forms import PricesForm, UserPricesForm
from prices_app.models import ProductModel, PersonModel, PriceModel, DepartmentRozetkaModels, ProductRoz
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

    product_data = PriceModel.objects.select_related('product').order_by('-date')[:5]

    if request.method == 'POST':
        form = PricesForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            site_name = cd['site']

            price_function = site_functions.get(site_name)

            if request.user.is_authenticated:
                user = request.user
                person = user.person if hasattr(user,
                                                'person') else None
            else:
                user, created_user = User.objects.get_or_create(
                    username=cd['name'],
                    defaults={
                        'email': cd['mail'],
                        'password': get_random_string(10)})

                if created_user:
                    password = get_random_string(12)
                    user.set_password(password)
                    user.save()
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)

                person, _ = PersonModel.objects.get_or_create(
                    user=user,
                    defaults={'telegram': cd['telegram']})

                send_mail(
                    subject=f"Дякуємо за реєстрацію!",
                    message=(
                        f"Ваші реєстраційні дані:\n"
                        f"Електронна пошта: {cd['mail']}\n"
                        f"Пароль: {password}\n\n"
                        f"Надалі оновлення по вашому товару автоматично надходитимуть на вашу електронну пошту.\n"
                        f"Щоб також отримувати сповіщення в Telegram — перейдіть у діалог з ботом і натисніть 'Start' у @priser_2025_bot."
                    ),
                    from_email=pricesua_project.settings.EMAIL_HOST_USER,
                    recipient_list=[cd['mail']],
                    fail_silently=False)

            if price_function:
                product_name, price, old_price, discount, icon, image = price_function(cd['link'])

                message = f"Товар: {product_name}\nЦіна: {price} UAN"

                chat_id = person.chat_id
                if chat_id:
                    send_message(chat_id, message)
                else:
                    print("Відсутній ID чату.")

                send_mail(
                    subject=f"Ціна для {product_name}",
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

    context = {'form': form, 'product_data': product_data, 'user': user}
    return render(request, 'prices_templates/main.html', context)

def product_history(request, id):
    product = ProductModel.objects.get(id=id)
    prices = PriceModel.objects.filter(product=product).order_by('-date')
    price = prices.first()
    context = {'product': product, 'prices': prices, 'price': price}
    return render(request, 'prices_templates/product_history.html', context)

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

                message = f"Товар: {product_name}\nЦіна: {price} UAN"

                chat_id = person.chat_id
                if chat_id:
                    send_message(chat_id, message)
                else:
                    print("Відсутній ID чату.")

                send_mail(
                    subject=f"Ціна для {product_name}",
                    message=message,
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
def success(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account/success.html', context)

def get_rozetka(request):
    departments = DepartmentRozetkaModels.objects.all().order_by('id')
    return render(request, 'prices_templates/rozetka.html', {'departments': departments})

def get_rozetka_category(request, name):
    department = get_object_or_404(DepartmentRozetkaModels, name=name)
    products_qs = ProductRoz.objects.filter(department_foreign_key=department).order_by('id')

    query = request.GET.get('q')
    if query:
        products_qs = products_qs.filter(
            Q(name__icontains=query))

    paginator = Paginator(products_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'prices_templates/rozetka_category.html', {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'category_name': department.name,
        'category_icon': department.icon.url if department.icon else None,
        'query': query,
    })

def get_discounts(request):
    discount_filter = request.GET.get('discount_range')

    if discount_filter == 'lt25':
        products = ProductRoz.objects.filter(discount__isnull=False, discount__lt=25)
    elif discount_filter == '25to50':
        products = ProductRoz.objects.filter(discount__isnull=False, discount__gte=25, discount__lte=50)
    elif discount_filter == 'gt50':
        products = ProductRoz.objects.filter(discount__isnull=False, discount__gt=50)
    else:
        products = ProductRoz.objects.all()

    paginator = Paginator(products.order_by('-discount'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'prices_templates/discounts_products.html', {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'discount_filter': discount_filter,
    })








