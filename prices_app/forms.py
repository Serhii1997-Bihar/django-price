from django import forms
from allauth.account.forms import SignupForm, LoginForm
from prices_app.models import PersonModel

class PricesForm(forms.Form):
    mail = forms.EmailField(widget=forms.URLInput(attrs={
            'style': 'border-radius: 0; height: 50px; '
                     'background-color: transparent; '
                     'border: none; '
                     'border-bottom: 1px solid white; '
                     'color: white; '
                     'box-sizing: border-box; '
                     'outline: none; ',
            'type': 'search',
            'class': 'form-control',
            'id': 'autocomplete_basic',
            'aria-controls': 'autoComplete_list_1',
            'aria-autocomplete': 'both',
            'placeholder': 'Пошта...'}))

    URL_CHOICES = [
        ('', ''),
        ('allo', 'allo.com'),
        ('comfy', 'comfy.ua'),
        ('epicentr', 'epicentr.ua'),
        ('estro', 'estro.ua'),
        ('reserved', 'reserved.com'),
        ('prom', 'prom.ua'),
        ('kasta', 'kasta.ua'),
        ('women', 'mo-woman.com.ua'),
        ('ager', 'ager.ua'),
        ('issa', 'issaplus.com'),
        ('foxtrot', 'foxtrot.com.ua'),
        ('laluna', 'laluna.com.ua'),
        ('brain', 'brain.com.ua'),
        ('makeup', 'makeup.com.ua'),
        ('f', 'f.ua'),
        ('moyo', 'moyo.ua'),
        ('citrus', 'ctrs.com.ua'),
        ('intertop', 'intertop.ua'),
        ('stylus', 'stylus.ua'),
        ('yakaboo', 'yakaboo.ua'),
        ('deka', 'deka.ua'),
        ('eldorado', 'eldorado.ua'),
        ('answear', 'answear.ua'),

    ]
    site = forms.ChoiceField(
        choices=URL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select_date',
            'style': 'height: 50px; border-radius: 0; width: 10%; background-color: transparent; border: none;'
        })
    )

    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'type': 'search',
            'class': 'form-control',
            'id': 'autocomplete_basic',
            'aria-controls': 'autoComplete_list_1',
            'aria-autocomplete': 'both',
            'style': 'height: 50px; border-radius: 0;'
                     'background-color: transparent; '
                     'border: none; '
                     'border-bottom: 1px solid white; '
                     'color: white; '
                     'box-sizing: border-box; '
                     'outline: none; ',
            'placeholder': 'Посилання...'
        })
    )

class CustomSignupForm(SignupForm):
    telegram = forms.CharField(max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'style': 'background-color: transparent; border: none; border-bottom: 1px solid white; color: white; border-radius: 0;'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'example@example.com',
            'style': 'background-color: transparent; border: none; border-bottom: 1px solid white; color: white; border-radius: 0;'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••',
            'style': 'background-color: transparent; border: none; border-bottom: 1px solid white; color: white; border-radius: 0;'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••',
            'style': 'background-color: transparent; border: none; border-bottom: 1px solid white; color: white; border-radius: 0;'
        })
        self.fields['telegram'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Telegram',
            'style': 'background-color: transparent; border: none; border-bottom: 1px solid white; color: white; border-radius: 0;'
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
            'placeholder': 'Пошта',
            'style': 'background-color: transparent; border: none; border-bottom: 1px solid white; color: white; border-radius: 0;'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••••',
            'style': 'background-color: transparent; border: none; border-bottom: 1px solid white; color: white; border-radius: 0;'
        })

class UserPricesForm(forms.Form):
    URL_CHOICES = [
        ('', ''),
        ('allo', 'allo.com'),
        ('comfy', 'comfy.ua'),
        ('epicentr', 'epicentr.ua'),
        ('estro', 'estro.ua'),
        ('reserved', 'reserved.com'),
        ('prom', 'prom.ua'),
        ('kasta', 'kasta.ua'),
        ('women', 'mo-woman.com.ua'),
        ('ager', 'ager.ua'),
        ('issa', 'issaplus.com'),
        ('foxtrot', 'foxtrot.com.ua'),
        ('laluna', 'laluna.com.ua'),
        ('brain', 'brain.com.ua'),
        ('makeup', 'makeup.com.ua'),
        ('f', 'f.ua'),
        ('moyo', 'moyo.ua'),
        ('citrus', 'ctrs.com.ua'),
        ('intertop', 'intertop.ua'),
        ('stylus', 'stylus.ua'),
        ('yakaboo', 'yakaboo.ua'),
        ('deka', 'deka.ua'),
        ('eldorado', 'eldorado.ua'),
        ('answear', 'answear.ua'),

    ]
    site = forms.ChoiceField(
        choices=URL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select_date',
            'style': 'height: 50px; border-radius: 0; width: 10%; background-color: transparent; border: none; '
        })
    )

    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'type': 'search',
            'class': 'form-control',
            'id': 'autocomplete_basic',
            'aria-controls': 'autoComplete_list_1',
            'aria-autocomplete': 'both',
            'style': 'height: 50px; border-radius: 0;'
                     'background-color: transparent; '
                     'border: none; '
                     'border-bottom: 1px solid white; '
                     'color: white; '
                     'box-sizing: border-box; '
                     'outline: none; ',
            'placeholder': '  Посилання...'
        })
    )

class EditForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': (
                'border-radius: 0; height: 50px; '
                'background-color: transparent; '
                'border: none; '
                'border-bottom: 1px solid white; '
                'color: white; '
                'box-sizing: border-box; '
                'outline: none; '
            ),
            'class': 'form-control',
            'placeholder': "  Ім'я..."
        })
    )
    telegram = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': (
                'border-radius: 0; height: 50px; '
                'background-color: transparent; '
                'border: none; '
                'border-bottom: 1px solid white; '
                'color: white; '
                'box-sizing: border-box; '
                'outline: none; '
            ),
            'class': 'form-control',
            'placeholder': '  Телеграм (username)...'
        })
    )
    mail = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'style': (
                'border-radius: 0; height: 50px; '
                'background-color: transparent; '
                'border: none; '
                'border-bottom: 1px solid white; '
                'color: white; '
                'box-sizing: border-box; '
                'outline: none; '
            ),
            'class': 'form-control',
            'placeholder': 'Пошта...'
        })
    )



