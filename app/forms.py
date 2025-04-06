from django import forms
from .models import *

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['phone']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password']:
            raise forms.ValidationError('Passwords are not the same')
        return data['password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_Confirmation'])
        if commit:
            user.save()
        return user
    
class LoginPhoneForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['phone']

        
class CodePhoneForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['verify_code']

