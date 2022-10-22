from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Post
from .forms import PostForm
from .forms import RegisterForm



@login_required(login_url='login')
def index(request):
    posts = Post.objects.all()
    
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        user_id = request.POST.get('user-id')

        if post_id:
            post_to_delete = Post.objects.filter(id=post_id).first()
            if post_to_delete and (request.user ==post_to_delete.author or request.user.has_perm("main.delete_post")):
                post_to_delete.delete()
                return redirect("/")
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            
            
            if request.user.is_staff:
                try:
                    group = Group.objects.get(name="default")
                    group.user_set.remove(user)

                except:
                    pass
                try:
                    group = Group.objects.get(name="mod")
                    group.user_set.remove(user)
                except:
                    pass


    return render(request, 'main/index.html', {'posts':posts})


@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
        form = PostForm()
    
    return render (request, 'main/create-post.html',{'form':form})



def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form':form})

def logout(request):
    logout(request)
   

