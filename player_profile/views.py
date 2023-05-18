from django.shortcuts import render, redirect
from .models import Profile, Message
from accounts.models import CustomUser

from django.contrib.auth.decorators import login_required

# Create your views here.


def Main(request):
    return render(request, 'main.html')


def Profile_list(request, sports, school):
    profile_list=Profile.objects.filter(sports=sports).filter(school=school).all()
            
    data = {'profile_list':profile_list, 'school':school}
    return render(request,'player_list.html', data)


def Profile_detail(request, sports, school, profile_id):
    message_list=Message.objects.filter(profile=Profile.objects.get(id=profile_id)).all()
    profile_detail = Profile.objects.get(id=profile_id)
    
    temp = CustomUser.objects.filter(is_staff=True).filter(profile=profile_detail).all()
    if temp.exists():
        user_detail = CustomUser.objects.filter(is_staff=True).get(profile=profile_detail)
    else:
        user_detail = None
    
    if profile_detail.school == 'Yonsei':
        profile_detail.school = '연세대'
    elif profile_detail.school == 'Korea':
        profile_detail.school = '고려대'
        
    if profile_detail.sports == 'soccer':
        profile_detail.sports = '축구'
    elif profile_detail.sports == 'basketball':
        profile_detail.sports = '농구'
    elif profile_detail.sports == 'baseball':
        profile_detail.sports = '야구'
    elif profile_detail.sports == 'icehockey':
        profile_detail.sports = '아이스하키'
    elif profile_detail.sports == 'rugby':
        profile_detail.sports = '럭비'
    
    data = {'profile_detail':profile_detail, 'user_detail': user_detail, 'message_list':message_list, 'sports':sports, 'school':school, 'profile_id':profile_id}
    
    return render(request,'player_profile.html', data)

def SendMessage(request, sports, school, profile_id):
    if request.method == 'POST':
        
        model=Message()
        model.profile=Profile.objects.get(id=profile_id)
        model.text=request.POST['message-text']
        model.save()
        
        
    
    profile_detail = Profile.objects.get(id=profile_id)
    
    data = {'profile_detail':profile_detail}
    return redirect('profile:detail', sports, school, profile_id)

@login_required
def DeleteMessage(request, sports, school, profile_id):
    if request.method == 'POST':
        model=Message.objects.get(id=request.POST['message_id'])
        model.delete()
    
    
    profile_detail = Profile.objects.get(id=profile_id)
    
    data = {'profile_detail':profile_detail}
    return redirect('profile:detail', sports, school, profile_id)