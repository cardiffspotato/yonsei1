from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator

from player_profile.models import Profile

# Create your models here.



class UserManager(BaseUserManager):
    user_in_migration = True
    
    def create_user(self,studentid,username,school,sports,major,idcard,password=False):
        if not studentid :
            raise ValueError('학번은 필수입니다')
        
        if not password :
            raise ValueError('비밀번호는 필수입니다')
        
        user=self.model(
            studentid=studentid, 
            username=username,
            school=school,
            sports=sports,
            major=major,
            idcard=idcard,
            
            )

        user.is_admin = False
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, studentid, username,password):
        user = self.create_user(
            studentid = studentid, 
            username=username,
            password=password,
            school='',
            sports='',
            major='',
            idcard='',
            
            )
        
        
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        
        user.save(using=self._db)
    
        return user

School_Choices = (
    ('Yonsei','연세대학교'),
    ('Korea','고려대학교'),
)

Sports_Choices = ( 
    ('soccer','축구'),
    ('basketball','농구'),
    ('baseball','야구'),
    ('icehockey','아이스하키'),
    ('rugby','럭비'),
)


class CustomUser(AbstractBaseUser,PermissionsMixin):

    objects=UserManager()

    studentid = models.CharField(max_length=10, null=False, unique=True, verbose_name="학번")
    username=models.CharField(max_length=20, null=False, unique=True, verbose_name="이름")
    
    school=models.CharField(max_length=20, null=False, choices=School_Choices, unique=False, verbose_name="학교", blank=True)
    sports=models.CharField(max_length=20, null=False, choices=Sports_Choices, unique=False, verbose_name="종목", blank=True)
    major=models.CharField(max_length=20, null=False, unique=False, verbose_name="학과", blank=True)
    
    profile=models.ForeignKey(Profile,on_delete=models.SET_DEFAULT, default='', blank=True, null=True, related_name='User_set')
    idcard=models.ImageField(upload_to="idcard/", blank=True, default='', verbose_name='학생증 확인')
    idprofile=models.ImageField(upload_to="idprofile/", blank=True, default='', verbose_name='프로필사진')
    info_1=models.CharField(max_length=5, null=False, unique=False, verbose_name="1_나이", blank=True)
    info_2=models.CharField(max_length=5, null=False, unique=False, verbose_name="2_키", blank=True)
    
    
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, verbose_name='승인완료')
    
    date_joined=models.DateTimeField(verbose_name="등록날짜",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="마지막로그인",auto_now=True)
    
    USERNAME_FIELD = 'studentid'     #고유식별자
    REQUIRED_FIELDS = ['username', 'password']
    
    class Meta:
        verbose_name = ("studentid")     # admin페이지 로그인 시 아이디창
        verbose_name_plural = ("users유저들")
        
