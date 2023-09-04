from django.shortcuts import render
from .forms import WeatherForm
import requests


# Create your views here.


def index(request):
  api_key = '50c4eb3c6942ed0192e805a8048b3025'
  ville = "Paris"  # Valeur par défaut si l'utilisateur n'a pas saisi de ville
  erreur = ""

  if request.method == 'POST':
    form = WeatherForm(request.POST)
    if form.is_valid():
      ville = form.cleaned_data['city']

  url = f"http://api.openweathermap.org/geo/1.0/direct?q={ville}&appid={api_key}"

  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    
    meteo_coord = {
      'ville': data[0]['name'],
      'lat': data[0]['lat'],
      'lon': data[0]['lon'],
    }

    # Envoie des deonnées a la deuxieme url de l'API 
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={meteo_coord['lat']}&lon={meteo_coord['lon']}&appid={api_key}"
    response = requests.get(url)
    datas = response.json()
    print(datas)
    meteo_data = {
      'country': datas['sys']['country'],  # Utilisez 'sys' pour obtenir le pays
      'temperature': datas['main']['temp'],  # Utilisez 'main' pour obtenir la température
      'description': datas['weather'][0]['description'],  # Utilisez 'weather' pour obtenir la description
      'icone': datas['weather'][0]['icon'],  # Utilisez 'weather' pour obtenir la description
      'humidite': datas['main']['humidity'],  # Utilisez 'main' pour obtenir l'humidité
    }
    temp = meteo_data['temperature']-273.15
  else:
    # En cas d'erreur HTTP, affichez le code de statut
    print(f'Erreur HTTP : {response.status_code}')

    meteo_data = None
    erreur = "La ville n'existe pas ou il y a eu une erreur dans la recherche."

  form = WeatherForm(initial={'city': ville})  # Pré-remplir le formulaire avec la ville saisie

  context = {
    "meteo_coord": meteo_coord,
    "meteo_data": meteo_data,
    "temp": temp,
    'form': form,
    "erreur":erreur
  }

  return render(request, 'index.html', context)
