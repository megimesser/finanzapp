from django.shortcuts import render
# myapp/views.py
from django.http import HttpResponse



# interface/views.py
def index(request):
    return render(request, 'index.html')  # Ohne "interface/"