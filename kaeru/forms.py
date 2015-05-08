__author__ = 'Hengzhi'

from django import forms

# change password
class changepasswordForm(forms.Form):
    oldpassword = forms.CharField(label=('Old Password'),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    newpassword = forms.CharField(label=("New Password"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    newpassword1 = forms.CharField(label=('New Password Confirmation'),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))


class Change_user_data_Form(forms.Form):
    new_first_name = forms.CharField(label=('Your First Name'),
                                     max_length=20,widget=forms.TextInput(attrs={'size': 20,})
                                     )
    new_last_name = forms.CharField(label=('Your Last Name'), max_length=20,)
    new_email = forms.EmailField(label=('Your Email'), min_length=3)


