
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

default_context = {'section': 'accounts'}

def login_view(request):
	if request.user.is_authenticated:
		return redirect('profile')
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('profile')
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/login.html', {'form': form, **default_context})

def logout_view(request):
	logout(request)
	return redirect('login')

def register_view(request):
	if request.user.is_authenticated:
		return redirect('profile')
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('profile')
	else:
		form = UserCreationForm()
	return render(request, 'accounts/register.html', {'form': form, **default_context})

@login_required
def profile_view(request):
	return render(request, 'accounts/profile.html', {'user': request.user, **default_context})
