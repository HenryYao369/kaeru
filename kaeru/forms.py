__author__ = 'Hengzhi'

from django import forms

# change password
class changepasswordForm(forms.Form):
    oldpassword = forms.CharField(label=('Old Password'),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    newpassword = forms.CharField(label=("New Password"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    newpassword1 = forms.CharField(label=('New Password Confirm'),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))




