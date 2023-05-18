from django.db import models

# Create your models here.

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


class Profile(models.Model):
    
    username=models.CharField(max_length=5, blank=False)
    school=models.CharField(max_length=10, choices=School_Choices, blank=False)
    sports=models.CharField(max_length=10, choices=Sports_Choices, blank=False)
    position=models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        name = self.username + ' / ' + self.school +' / ' + self.sports
        return str(name)
    
    class Meta:
        ordering=['username']
        

class Message(models.Model):
    
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    text=models.CharField(max_length=250, blank=False)
    
    class Meta:
        ordering=['-id']