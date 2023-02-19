from importlib.resources import path
from itertools import chain
import random
from unicodedata import name
from django import views
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from .models import follower, profile, post, like
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def index(request):
    #custom feed
    user_object = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user=user_object)

    follow_list = [follow.user for follow in follower.objects.filter(follower=request.user.username)]
    custom_feed = [post.objects.filter(user= name) for name in follow_list]   

    feed = list(chain(*custom_feed))

    #user suggestion
    all_users=User.objects.all()
    user_following = [User.objects.get(username=(name.user)) for name in follower.objects.filter(follower=request.user.username)]
    user_following.append(User.objects.get(username=request.user.username))
    suggestion_list= [user for user in list(all_users) if user not in list(user_following)]
    random.shuffle(suggestion_list)

    suggestion_profile=[user.id for user in suggestion_list]

    suggestion_ids = [profile.objects.filter(id_user=ids) for ids in suggestion_profile]
    display_suggestion= list(chain(*suggestion_ids))

    
    

    return render(request, 'index.html', {'user_profile':user_profile, 'feed':feed, 'display_suggestion':display_suggestion[:4]})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.info(request, 'Password don\'t match')
            return redirect('register')
        
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('register')

        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('register')

        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            #login user and redirect to settings page
            user_login = authenticate(username=username, password=password)
            login(request, user_login)

            #create a profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile= profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('login')
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def setting(request):
    user_profile = profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get('image'):
            user_profile.profileimg = request.FILES.get('image')
        if request.POST['bio']:
            user_profile.bio = request.POST['bio']
        if request.POST['location']:
            user_profile.location = request.POST['location']
        if request.POST['first_name']:
            user_profile.first_name = request.POST['first_name']
        if request.POST['last_name']:
            user_profile.last_name = request.POST['last_name']
        if request.POST['work']:
            user_profile.work = request.POST['work']
        if request.POST['relationship']:
            user_profile.relationship = request.POST['relationship']
        user_profile.save()
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile':user_profile})

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        if image:
            new_post = post.objects.create(user=user, image=image, caption=caption)
            new_post.save()

    return redirect('/')

@login_required(login_url='login')
def like_post(request):
    username= request.user.username
    post_id= request.GET.get('post_id')
    Post = post.objects.get(id=post_id)
    like_filter = like.objects.filter(post_id=post_id, username=username).first()
    if like_filter:
        like_filter.delete()
        Post.likes -= 1
        Post.save()
        return redirect('/')
    else:
        new_like= like.objects.create(post_id=post_id, username=username)
        new_like.save()
        Post.likes += 1
        Post.save()
        return redirect('/')

@login_required(login_url='login')
def Profile(request, un):
    user_object= User.objects.get(username=un)
    user_profile= profile.objects.get(user=user_object)
    user_posts= post.objects.filter(user=un)
    user_post_length=len(user_posts)
    followers = request.user.username
    user = un
    follower_count = len(follower.objects.filter(user=un))
    following_count = len(follower.objects.filter(follower=un))

    follow_button = 'Follow'
    if follower.objects.filter(follower=followers, user=user).first():
        follow_button = 'Unfollow'

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'follow_button': follow_button,
        'follower_count': follower_count,
        'following_count': following_count,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        followers= request.POST['follower']
        user= request.POST['user']

        if follower.objects.filter(follower=followers, user=user).first():
            delete_follower = follower.objects.get(follower=followers, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower= follower.objects.create(follower=followers, user=user)
            new_follower.save()
            if request.POST['index_page']:
                return redirect('/')
            else:
                return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user=user_object)
    if request.method == 'POST':
        search_user= request.POST['username']
        username_object= User.objects.filter(username__icontains=search_user)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            username_profile_list.append(profile.objects.filter(id_user=ids))

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list':username_profile_list})



