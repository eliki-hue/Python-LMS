from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            # user.profile.first_name = form.cleaned_data.get('first_name')  # Example if you have a profile
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('course_list')  # Redirect to course list after registration
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
