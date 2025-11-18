# authz/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View

class LoginView(View):
    """Einfacher Login - Username & Passwort"""
    
    def get(self, request):
        # Zeigt das Login-Formular
        return render(request, 'login/login.html')
    
    def post(self, request):
        # Verarbeitet den Login
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Nach Login zur Home-Seite
            return redirect('/home/')
        else:
            # Login fehlgeschlagen
            context = {'error': 'Username oder Passwort falsch'}
            return render(request, 'login/login.html', context)


class LogoutView(View):
    """Einfacher Logout"""
    
    def get(self, request):
        logout(request)
        return redirect('/login/')