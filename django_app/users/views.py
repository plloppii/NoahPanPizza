from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
	if(request.method == 'POST'):
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get("username")
			# messages.success(request, f'Account created for {username}!')
			messages.success(request, f'Your account has been created! You are now able to login.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {"form": form})

#Decorator that adds functionality to the view. (This requires the user to be logged in to access the profile page)
#More complex with class based views.
@login_required
def profile(request):
	if(request.method == 'POST'):
		u_form = UserUpdateForm(request.POST, instance= request.user)
		p_form = ProfileUpdateForm(request.POST, 
									request.FILES,
								 	instance = request.user.profile)
		#Record the previous username
		prev_username = request.user.username
		prev_email = request.user.email
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!!')
			return redirect('profile')
		else:
			#Do not update template to show the modified username if it is not valid.
			request.user.username = prev_username
			request.user.email = prev_email
	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)

	print(request.user.username)
	context = {
		"u_form" : u_form,
		"p_form" : p_form 
	}
	return render(request, 'users/profile.html', context)


# different message options
# message.debug
# .info
# .success
# .warning
# .error