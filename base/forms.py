from django.forms import ModelForm

from .models import Room
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ['username', 'email']

class passwordChangeForm(UserChangeForm):

    password = forms.CharField(
        required=True,  # now it's required
        widget=forms.PasswordInput,
        help_text="Enter a new password"
    )

    password2 = forms.CharField(
        required=True,  # now it's required
        widget=forms.PasswordInput,
        help_text="Enter a new password Again"
    )


    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("username", "email")


    def clean_password(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password")
        if password:

            if password == password2:
            # Use Django's built-in password validators
                validate_password(password, self.instance)
                return password
                
            
            raise ValidationError("Passwords doesn't match")
        raise ValidationError("Password cannot be empty")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
