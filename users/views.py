from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .forms import PostForm
from django.contrib import messages
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You are successfully registered.")
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    form = PostForm(request.POST, request.FILES)

    if form.is_valid():
        form = Post.objects.create(user=request.user, post_title=request.POST['post_title'],
                                   post_content=request.POST['post_content'],
                                   date_published=request.POST['date_published'],
                                   user_profile_link=request.POST['user_profile_link'],
                                   img=request.FILES['img'],
                                   )
        print(form)
        form.save()
        messages.success(request, "your post is uploaded successfully.")
        form = PostForm()
    return render(request, 'profile.html', {'form': form})


