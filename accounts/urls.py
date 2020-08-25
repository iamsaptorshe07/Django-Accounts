from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.userSignup,name='signup'),
    path('login',views.userLogin,name='login'),
    path('logout', views.userLogout,name='logout'),
    path('profile/user/<int:id>',views.follow,name='follow'),
    path('myprofile/<int:id>',views.myprofile,name='myprofile'),
    path('viewprofile/<int:id>',views.viewProfile,name='viewprofile'),
    path('editmyprofile/<int:id>',views.editProfile,name='editProfile'),
    path('deletemyprofile/<int:id>',views.deleteProfile,name='deleteProfile'),
    path('activateaccount/<int:id>',views.activateaccount,name='activateaccount'),
    path('activate/<uid>/<token>',views.activateProfile, name='activate'),
]