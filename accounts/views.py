from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from player_profile.models import Profile
from .models import CustomUser
from .forms import CustomUser_Form

from django.contrib.auth.decorators import login_required

import os
from config import settings

# Create your views here.

def Login(request):
    if request.method == 'POST':
            username = request.POST['studentid']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호가 일치하지 않습니다'}) #error빨간줄
    else:
        return render(request, 'accounts/login.html')

@login_required
def Logout(request):
    auth.logout(request)
    return redirect('/')

def Signin(request):
    if request.method == 'POST':
        model=CustomUser.objects.filter(studentid=request.POST['studentid']).all()
        if model.exists():
            return render(request, 'accounts/signin.html', {'error': '이미 존재하는 학번입니다.'})
        
        form = CustomUser_Form(request.POST)
        if form.is_valid():
            if request.FILES.get('fileUpload') == None:
                return render(request, 'accounts/signin.html',{'error': '학생증을 업로드해주세요'})
            else:
                if len(request.POST['password1']) >= 6:
                    
                    if request.POST['password1'] == request.POST['password2']:
                        user = CustomUser.objects.create_user(
                                                        studentid=request.POST['studentid'],
                                                        username=request.POST['username'],
                                                        password=request.POST['password1'],
                                                        school=request.POST['school'],
                                                        sports=request.POST['sports'],
                                                        major=request.POST['major'],
                                                        idcard=request.FILES.get('fileUpload'),
                                                        )
                        #auth.login(request, user)
                        return render(request,'accounts/signin_complete.html')
                    else:
                        return render(request, 'accounts/signin.html',{'error': '비밀번호가 일치하지 않습니다.'})
                else:
                    return render(request, 'accounts/signin.html',{'error': '비밀번호 길이가 너무 짧습니다'})
        else:
            return render(request, 'accounts/signin.html',{'error': '양식을 모두 입력해주세요.'})
    return render(request, 'accounts/signin.html')


@login_required
def Mypage(request):
    if request.user.school == 'Yonsei':
        request.user.school = '연세대학교'
    elif request.user.school == 'Korea':
        request.user.school = '고려대학교'
        
    if request.user.sports == 'soccer':
        request.user.sports = '축구'
    elif request.user.sports == 'basketball':
        request.user.sports = '농구'
    elif request.user.sports == 'baseball':
        request.user.sports = '야구'
    elif request.user.sports == 'icehockey':
        request.user.sports = '아이스하키'
    elif request.user.sports == 'rugby':
        request.user.sports = '럭비'
        
    if request.method == 'POST':
        model=CustomUser.objects.get(studentid=request.user.studentid)
        
        if model.idprofile != '':
            os.remove(os.path.join(settings.MEDIA_ROOT+'/idprofile',os.path.basename(model.idprofile.path)))
        
        model.info_1 = request.POST['info_1']
        model.info_2 = request.POST['info_2']
        model.idprofile = request.FILES.get('idprofile', '')
        model.save()
        
        request.user.info_1 = model.info_1
        request.user.info_2 = model.info_2
        request.user.idprofile = model.idprofile
        
        return render(request, 'accounts/mypage.html', {'primary': '변경 완료했습니다.'})
    else:
        return render(request, 'accounts/mypage.html')