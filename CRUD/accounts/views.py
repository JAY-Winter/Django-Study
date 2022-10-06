from django.db import reset_queries
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserCreationForm

# Create your views here.

def login():
    pass

def logout():
    pass

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def delete():
    pass

def update():
    pass

def change_password():
    pass