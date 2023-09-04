from django.urls import path,include
from api_weather import views

urlpatterns = [
    path('api-weather/',views.index, name="index"),
]
