from django import forms
from django.forms import ModelForm 
from django.contrib.auth.models import User
from .models import Idea,DataUser,SubIdea

class FormSignin(ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
        labels = {'username':'Email'}
        widgets = {
            'username':forms.EmailInput(attrs={
                'id':'input_signin',
                'placeholder':'email address',
            }),
            'password':forms.PasswordInput(attrs={
                'id':'input_signin',
                'placeholder':'password'
            })
        }

class FormSignup(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id':'input_signin','placeholder':'username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'id':'input_signin','placeholder':'email address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id':'input_signin','placeholder':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id':'input_signin','placeholder':'confirm password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class FormIdea(ModelForm):
    class Meta:
        model = Idea
        fields = ['idea_name','idea_description','idea_image']

class FormEditUser(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        widgets = {
            'email':forms.EmailInput(attrs={
                'readonly':'true'
            })
        }

class FormEditDatauser(ModelForm):
    class Meta:
        model = DataUser
        fields = ['image_profile']

class Formsubidea(ModelForm):
    class Meta:
        model = SubIdea
        fields = ['sub_idea','sub_body','sub_image','sub_file']
        labels = {'sub_idea':'heading','sub_body':'description','sub_image':'image','sub_file':'file'}
        widgets = {
            'sub_idea':forms.TextInput(attrs={
                'id':'form-new-method',
            }),
            'sub_body':forms.Textarea(attrs={
                'id':'form-new-method',
            }),
            'sub_image':forms.FileInput(attrs={
                'id':'form-new-method',
                'accept':'.png,.jpg,',
            }),
            'sub_file':forms.FileInput(attrs={
                'id':'form-new-method',
                'accept':'.pdf'
            })
        }