__author__ = 'Hengzhi'

from django import forms

# change password
class changepasswordForm(forms.Form):
    oldpassword = forms.CharField(label=('Old Password'),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    newpassword = forms.CharField(label=("New Password"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    newpassword1 = forms.CharField(label=('New Password Confirm'),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))


class change_user_data_Form(forms.Form):
    new_first_name = forms.CharField(label=('New First Name:'), max_length=20,widget=forms.TextInput(attrs={'size': 20,}))
    new_last_name = forms.CharField(label=('New Last Name'), max_length=20,)
    new_email = forms.EmailField(label=('New Email'), min_length=3)


