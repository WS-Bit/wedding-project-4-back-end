from django.shortcuts import render, redirect
from django.conf import settings

def enter_password(request):
    if request.method == 'POST':
        if request.POST.get('password') == settings.SITE_PASSWORD:
            request.session['is_authenticated'] = True
            return redirect('guests')  # Redirect to the guests page
    return render(request, 'enter_password.html')

def home(request):
    return render(request, 'home.html')