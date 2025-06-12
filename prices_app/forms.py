from django import forms
from allauth.account.forms import SignupForm, LoginForm
from prices_app.models import PersonModel

class PricesForm(forms.Form):
    name = forms.CharField(widget=forms.URLInput(attrs={
            'style': 'border-radius: 0;',
            'type': 'search',
            'class': 'form-control',
            'id': 'autocomplete_basic',
            'aria-controls': 'autoComplete_list_1',
            'aria-autocomplete': 'both',
            'placeholder': "  Iм'я..."}))
    telegram = forms.CharField(widget=forms.URLInput(attrs={
            'style': 'border-radius: 0;',
            'type': 'search',
            'class': 'form-control',
            'id': 'autocomplete_basic',
            'aria-controls': 'autoComplete_list_1',
            'aria-autocomplete': 'both',
            'placeholder': '  Телеграм (username)...'}))
    mail = forms.EmailField(widget=forms.URLInput(attrs={
            'style': 'border-radius: 0;',
            'type': 'search',
            'class': 'form-control',
            'id': 'autocomplete_basic',
            'aria-controls': 'autoComplete_list_1',
            'aria-autocomplete': 'both',
            'placeholder': '  Пошта...'}))

    URL_CHOICES = [
        ('', 'магазин'),
        ('allo', 'allo.com'),
        ('comfy', 'comfy.ua'),
        ('epicentr', 'epicentr.ua'),
        ('foxtrot', 'foxtrot.com.ua'),
        ('rozetka', 'rozetka.ua'),
        ('brain', 'brain.com.ua'),
        ('makeup', 'makeup.com.ua'),
        ('f', 'f.ua'),
        ('moyo', 'moyo.ua'),
        ('citrus', 'ctrs.com.ua'),
        ('eva', 'eva.ua'),
        ('intertop', 'intertop.ua'),
        ('stylus', 'stylus.ua'),
        ('yakaboo', 'yakaboo.ua'),
        ('deka', 'deka.ua'),
        ('bookye', 'book-ye.com.ua'),
        ('zara', 'zara.com'),
        ('eldorado', 'eldorado.ua'),
        ('telemart', 'telemart.ua'),
        ('osport', 'osport.ua'),
        ('bi', 'bi.ua'),
        ('sinsay', 'sinsay.com'),
        ('reserved', 'reserved.com'),
    ]
    site = forms.ChoiceField(
        choices=URL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select_date',
            'style': 'height: 50px; border-radius: 0;'
        })
    )

    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'type': 'search',
            'class': 'form-control',
            'id': 'autocomplete_basic',
            'aria-controls': 'autoComplete_list_1',
            'aria-autocomplete': 'both',
            'style': 'height: 50px; border-radius: 0;',
            'placeholder': '  Посилання на товар...'
        })
    )

class CustomSignupForm(SignupForm):
    telegram = forms.CharField(max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'example@example.com',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••',
        })
        self.fields['telegram'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Telegram',
        })

    def save(self, request):
        user = super().save(request)
        telegram = self.cleaned_data.get('telegram')

        if hasattr(user, 'person'):
            person = user.person
            person.telegram = telegram
            person.save()
        else:
            person = PersonModel.objects.create(user=user, telegram=telegram)

        return user

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'Email'
        self.fields['login'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••••'
        })

class UserPricesForm(forms.Form):
    URL_CHOICES = [
        ('', 'магазин'),
        ('allo', 'allo.com'),
        ('comfy', 'comfy.ua'),
        ('epicentr', 'epicentr.ua'),
        ('foxtrot', 'foxtrot.com.ua'),
        ('rozetka', 'rozetka.ua'),
        ('brain', 'brain.com.ua'),
        ('makeup', 'makeup.com.ua'),
        ('f', 'f.ua'),
        ('moyo', 'moyo.ua'),
        ('citrus', 'ctrs.com.ua'),
        ('eva', 'eva.ua'),
        ('intertop', 'intertop.ua'),
        ('stylus', 'stylus.ua'),
        ('yakaboo', 'yakaboo.ua'),
        ('deka', 'deka.ua'),
        ('bookye', 'book-ye.com.ua'),
        ('zara', 'zara.com'),
        ('eldorado', 'eldorado.ua'),
        ('telemart', 'telemart.ua'),
        ('osport', 'osport.ua'),
        ('bi', 'bi.ua'),
        ('sinsay', 'sinsay.com'),
        ('reserved', 'reserved.com'),
    ]
    site = forms.ChoiceField(
        choices=URL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select_date',
            'style': 'height: 50px; border-radius: 0;'
        })
    )

    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'type': 'search',
            'class': 'form-control',
            'id': 'autocomplete_basic',
            'aria-controls': 'autoComplete_list_1',
            'aria-autocomplete': 'both',
            'style': 'height: 50px; border-radius: 0;',
            'placeholder': '  Посилання на товар...'
        })
    )



