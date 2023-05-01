from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('tweet/', views.tweet, name = "tweet"),
    path('search/', views.search_user, name = "search"),
    path('like_tweet/<int:pk>', views.like_tweet, name = "like_tweet"),
    path('profile_list/',views.profile_list, name="profile_list"),
    path('profile/<int:id>', views.profile, name = "profile"),
    path('',views.login_user, name= "login"),
    path('logout',views.logout_user, name="logout"),
    path('register/',views.register_user, name="register"),
    path('edit_profile/',views.edit_profile, name="edit"),
    path('hashtags/', views.hashtag, name='hashtag'),
    path('delete_tweet/<int:id>',views.delete_tweet, name='delete_tweet')
    
    
]
