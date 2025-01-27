from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm

class LogInUserForm(AuthenticationForm):
    username  = forms.CharField(required=True, help_text='Enter your username and keep save', widget=forms.TextInput(attrs={'class':'form-control'}) )
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}), label='Password', help_text='min_lenght-8 mix characters [i.e Ayo1234@] ')

    
    
    class Meta:
        fields= ['username', 'password']


class CustomUserCreationForm(UserCreationForm):
    first_name  = forms.CharField(required=True, help_text='Enter your real  (Surname First)', widget=forms.TextInput(attrs={'class':'form-control'}) )
    last_name  = forms.CharField(required=True, help_text='Enter your real  (Surname First)', widget=forms.TextInput(attrs={'class':'form-control'}) )
    username  = forms.CharField(required=True, help_text='Enter your username and keep save', widget=forms.TextInput(attrs={'class':'form-control'}) )
    email  = forms.EmailField(required=True, help_text='Enter your valid email', widget=forms.TextInput(attrs={'class':'form-control'}) )
    password1 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}), label='Password', help_text='min_lenght-8 mix characters [i.e Ayo1234@] ')
    password2 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}),help_text='Enter same password as before',label='Confirm Password')
    Phone = forms.CharField(max_length = 11, min_length = 11,  widget=forms.NumberInput(attrs={'class':'form-control', 'type':'number', 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Enter numbers Only '}))
    referer_username = forms.CharField(required=False,help_text='Leave blank if no referral',label='Referral username [optional]')


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("first_name", 'last_name', 'username','email','Phone','Address','referer_username','password1','password2')
    


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}), label='Old Password', help_text='min_lenght-8 mix characters [i.e Ayo1234@] ')
    new_password1 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}), label='New Password', help_text='min_lenght-8 mix characters [i.e Ayo1234@] ')
    new_password2 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}), label='Confirm New Password', help_text='min_lenght-8 mix characters [i.e Ayo1234@] ')
    
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        
    


class UserProfileForm(ModelForm):
    

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'account_name', 'account_number']
        
  
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile 
#         fields = '__all__'
        
# class UserProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
        
        
    