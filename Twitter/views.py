from .models import Profile, Tweets
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .forms import TweetForm, SignUpForm,ProfilePictureForm
from django.contrib.auth import authenticate, login, logout

def hashtag(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            hashtag = request.POST.get('tag')
            tweet = Tweets.objects.filter( tag = hashtag)
           
            
            return render(request, 'hashtag.html', {'tweets':tweet })
        return redirect('home')
    return redirect('login')


def search_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            if  username:
                users = User.objects.filter(username__icontains= username)
                profile = Profile.objects.filter(user = users)
                return render(request, 'search.html', {'users': users, 'profiles':profile})
            else:
                return redirect('home')
        return redirect('home')
    messages.success(request, 'you must login first')
    return redirect('login')


def delete_tweet(request, id):

    tweet = get_object_or_404(Tweets , id= id )
    tweet.delete()
    return redirect(request.META.get("HTTP_REFERER"))

def register_user(request):
    form = SignUpForm()
    if request.method== 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username = username, password= password)
            login(request,user)
            messages.success(request,('Wellcome to Twitter!'))
            return redirect('home')
    
    return render(request, 'register.html',{'form':form})



def search(request):
    if request.user.is_authenticated:
        if request.method== 'POST':
            username = request.POST["username"]
            # users = User.objects.filter(username = username)
            users = get_object_or_404(User, username=username)
            user_profile = []
            user_profile_list = []

            for user in users:
                user_profile.append(user.id)
            for id in user_profile:
                profile_list = Profile.objects.filter(user_id = id)
                user_profile_list.append(profile_list)           
            # profiles = Profile.objects.filter(user = users)
            return render(request, 'search.html', { 'user_porfile_list':users})
        else:
            return render(request, 'search.html', {})
    else:
        messages.success(request,('You must Login!'))
        return redirect('home')
    


def tweet(request):
    if request.user.is_authenticated:
        # pic_form = TweetPictureForm(request.POST or None, request.FILES or None)
        form = TweetForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid() :
                tweet= form.save(commit= False)
                # pic = pic_form.save( commit=False)
                tweet.user = request.user
                # pic.user = request.user
                tweet.save()
                # pic.save()
                messages.success(request, "Your tweet is posted!")
                return redirect('home')
        else:
            return render(request, 'tweet.html' , {'form':form})
    else:
        messages.success(request,'You must be logged in to tweet!')
        return redirect('home')



def home(request):
    if request.user.is_authenticated:
        
        form= TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid:
                tweet= form.save(commit= False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Your tweet is posted!")
                return redirect('home')
       
        tweets = Tweets.objects.all().order_by("-created_at")
        
        
        return render(request, 'home.html', {"tweets":tweets,"form":form})
    else:
       
         messages.success(request,"You must login first!")
         return redirect('login')



def profile_list(request):
    if request.user.is_authenticated: 
        profile= Profile.objects.exclude(user= request.user)
        
        return render(request, 'profile_list.html', {"profiles" : profile})
    else:
        messages.success(request,("You must be logged in first to view profile list"))
        return redirect('login')
    


def profile(request, id):
    if request.user.is_authenticated:
        tweets= Tweets.objects.filter(user_id = id)[::-1]
        profile = Profile.objects.get(user_id = id)
        
        user_profile = request.user.profile
        if request.method == "POST":
            
            action = request.POST['follow']
            if action == "follow":
                user_profile.follows.add(profile)
            else:
                user_profile.follows.remove(profile)
            user_profile.save()    
        return render(request,'profile.html',{'profile':profile, "tweets":tweets, "current_user":user_profile})
    else:
        messages.success(request,('You must be logged in first'))
        return redirect('login')


def login_user(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            messages.success(request,('Login successful!'))
            return redirect('home')
        else:
            messages.success(request,('check your password and username please'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,('You have logged out!'))
    return redirect('login')



def edit_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id= request.user.id)
        current_user_profile = Profile.objects.get(user__id = request.user.id)
        form = SignUpForm(request.POST or None, request.FILES or None, instance = current_user)
        pic_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=current_user_profile)
        if request.method == 'POST':
            if form.is_valid() and pic_form.is_valid():
                form.save()
                pic_form.save()
                login(request, current_user)
                messages.success(request,('Your profile is updated!'))
                return redirect('home')
        else:    
            return render(request, 'edit_profile.html',{'form':form, 'pic_form':pic_form})
    else:
        messages.success(request,('you must be logged in to edit a profile'))
        return redirect('login')



def like_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweets , id= pk )
        # if tweet.likes.filter(id = request.user.id):
        if request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,('you must be logged in'))
        return redirect('login')