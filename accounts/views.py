from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.conf import settings
from django.contrib import messages
from .models import *
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import send_mail
from .tokens import activation_token 
from blog.models import *
from django.utils.dateparse import parse_date
# Create your views here.
def userSignup(request):
    if request.method == 'POST':
        try:
            user = User()
            user.name=request.POST['name']
            user.email=request.POST['email']
            user.gender=request.POST['gender']
            if User.objects.filter(email=user.email).exists():
                user = User.objects.get(email=user.email)
                if user.is_active is True:
                    messages.warning(request,'Account is already created')
                    return redirect('login')
                elif user.is_active is False:
                    messages.warning(request,'Check the mail sent on {} to activate your account'.format(user.creationTime))
                    return redirect('/')
            else:
                user.set_password(request.POST['password'])
                user.is_active = False
                user.save()
                site = get_current_site(request)
                print(site)
                mail_subject = 'Site Activation Link'
                message = render_to_string('email.html', {
                    'user': user,
                    'domain': site,
                    'uid':user.id,
                    'token':activation_token.make_token(user)
                })
                to_email=user.email
                to_list=[to_email]
                from_email=settings.EMAIL_HOST_USER
                send_mail(mail_subject,message,from_email,to_list,fail_silently=True)
                messages.success(request,'Check your mail to activate your account')
                return redirect('/')  
        except  Exception as problem:
            messages.error(request,'{}'.format(problem))
            return redirect('signup')
    else:
        return render(request,'signup.html')

def userLogin(request):
    if request.method=='POST':
        try:        
            email=request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active == False:
                    messages.warning(request,'Check your registered mail address to set up your profile and to Log in')
                    return redirect('/')
                else:
                    user = auth.authenticate(email=email,password=password)
                    if user is not None:
                        auth.login(request,user)
                        messages.success(request,'Successfully Loggedin')
                        return redirect('/')
                    else:
                        messages.error(request,'Password does not match')
                        return redirect('login')
            else:
                messages.error(request,'No Account registered with this mail')
                return redirect('login')
        except Exception as problem:
            messages.error(request,problem)
            return redirect('login')
    return render(request,'login.html')


def userLogout(request):
    try:
        auth.logout(request)
        messages.success(request,'Successfully Logged Out')
        return redirect('/')
    except Exception as problem:
        print(problem)
        messages.success(request,'Sorry, Internal Problem Occured')
        return redirect('/')
    
def activateProfile(request, uid, token):
    user = User.objects.get(id=uid)
    if user is not None and activation_token.check_token(user,token):
       return render(request,'profile.html',{'user':user})
    else:
        return HttpResponse("Forbidden")


def activateaccount(request,id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=id)
            user.name = request.POST.get('name')
            username = request.POST.get('username')
            profession = request.POST.get('profession')
            bdate = parse_date(request.POST.get('bdate'))
            country = request.POST.get('country')
            image = request.FILES.get('image')
            profile = UserProfile(user=user,username=username,picture=image, profession=profession,birthdate=bdate,country=country)
            profile.save()
            user.is_active = True
            user.save()
            messages.success(request,'Profile Created Explore Open Blog Forum')
            return redirect('login')
        except Exception as err:
            messages.error(request,err)
            return render('/')
    else:
        return HttpResponse('Bad Request')
   

def viewProfile(request,id):
    user = User.objects.get(id=id)
    profile = UserProfile.objects.get(user=user)
    followers = profile.followers.count()
    following = UserProfile.objects.filter(user_id=profile.user.id).count()
    totalblogpost = BlogPost.objects.filter(writer=user).count()
    is_following = False
    if profile.followers.filter(id=request.user.id).exists():
        is_following = True
    post = BlogPost.objects.filter(writer=user)
    context = {
        'Posts':post,
        'User':user,
        'Profile':profile,
        'followers':followers,
        'is_following':is_following,
        'following':following,
        'totalblogpost':totalblogpost
    }
    return render(request,'userprofile.html',context=context)


def myprofile(request,id):
    user = User.objects.get(id=id)
    if request.user == user:
        profile = UserProfile.objects.get(user=user)
        context = {
            'Profile':profile
        }
        return render(request,'editprofile.html',context=context)
    else:
        return HttpResponse("Bad Request")


def editProfile(request,id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        profile = UserProfile.objects.get(user=user)
        user.name = request.POST.get('name')
        user.gender = request.POST.get('gender')
        user.save()
        profile.username = request.POST.get('username')
        profile.bdate = request.POST.get('bdate')
        profile.bio = request.POST.get('bio')
        profile.profession = request.POST.get('profession')
        profile.country = request.POST.get('country')
        if request.FILES.get('image'):
            profile.picture = request.FILES.get('image')
            print(profile.picture)
        profile.save()
        messages.success(request,'Successfully Updated your information')
        return redirect('/accounts/myprofile/{}'.format(id))
    else:
        return HttpResponse("/")
        
def deleteProfile(request,id):
    user = User.objects.get(id=id)
    if request.user == user:
        try:
            user.delete()
            messages.success(request,'Account deleted')
            return redirect('/')
        except Exception as e:
            messages.error(request,e)
            return redirect('/')
    else:
        return HttpResponse('Bad Request')
        
        
def follow(request,id):
    try:
        user = User.objects.get(id=id)
        profile = UserProfile.objects.get(user=user)
        if profile.followers.filter(id=request.user.id).exists():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)
        return redirect('/accounts/viewprofile/{}'.format(user.id))
    except Exception as e:
        return HttpResponse("Bad Request")
        
        
        
    