from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
class FilterForm(forms.Form):
    country = forms.CharField(max_length=100, required=False, label='Страна')
    min_latitude = forms.FloatField(required=False, label='Мин. широта')
    max_latitude = forms.FloatField(required=False, label='Макс. широта')
    min_longitude = forms.FloatField(required=False, label='Мин. долгота')
    max_longitude = forms.FloatField(required=False, label='Макс. долгота')


class AircraftFilterForm(forms.Form):
    icao24 = forms.CharField(max_length=6, required=False, label='Идентификатор воздушного судна')
    country = forms.CharField(max_length=100, required=False, label='Страна')
    min_latitude = forms.FloatField(required=False, label='Мин. широта')
    max_latitude = forms.FloatField(required=False, label='Макс. широта')
    min_longitude = forms.FloatField(required=False, label='Мин. долгота')
    max_longitude = forms.FloatField(required=False, label='Макс. долгота')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(label="Имя")  # Изменяем метку на "Имя"

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user