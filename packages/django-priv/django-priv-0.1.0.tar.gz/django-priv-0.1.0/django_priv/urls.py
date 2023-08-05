from django.urls import path
from . import views

urlpatterns = [path('priv/<id>', views.download, name='download')]