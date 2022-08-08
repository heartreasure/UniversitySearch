from django.urls import path, include
from .views import *
urlpatterns = [
    path('', indexView, name='index'),
    path('login', userLogin, name='userLogin'),
    path('register', userRegister, name='userRegister'),
    path('logout', logoutView, name='logout'),
    path('contact', contactView, name='contact'),
    path('feature', featureView, name='feature'),
    path('reset_password', findpsView, name='findps'),
]
