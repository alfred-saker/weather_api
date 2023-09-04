from django import forms

class WeatherForm(forms.Form):

    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Entrer le nom de la ville'}))
