from django.shortcuts import render

# Create your views here.

def landing(request):
    return render(request, 'landing.html')
    

def about(request):
    return render(request, 'about.html')