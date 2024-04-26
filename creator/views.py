from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Creator
from .forms import CreatorForm


@login_required
def mypage(request):
    creator = request.user.creator
    context = {'creator': creator}
    return render(request, 'creator/mypage.html', context)


def signup(request):       
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are successfully signed up. Please continue to log in...')
            return redirect('creator:login')
        else:
            form = UserCreationForm()
            messages.success(request, 'Something wrong with the signup. Please try again...')
            return render(request, 'creator/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'creator/signup.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are successfully logged out...')    
    return redirect('creator:login')


def creators(request):
    # Get creators
    creators = Creator.objects.all()
    context = {'creators': creators}
    return render(request, 'creator/creators.html', context)


def creator(request, pk):
    creator = Creator.objects.get(pk=pk)
    context = {'creator': creator}
    return render(request, 'creator/creator.html', context)


def edit(request):
    try:
        creator = request.user.creator
        if request.method == 'POST':
            form = CreatorForm(request.POST, request.FILES, instance=creator)
            if form.is_valid():
                form.save()
                return redirect('core:index')
        else:
            form = CreatorForm(instance=creator)
    except Exception:
        if request.method == 'POST':
            form = CreatorForm(request.POST, request.FILES)
            if form.is_valid():
                creator = form.save(commit=False)
                creator.user = request.user
                creator.save()
                return redirect('core:index')
        else:
            form = CreatorForm()
    return render(request, 'creator/edit.html', {'form': form})