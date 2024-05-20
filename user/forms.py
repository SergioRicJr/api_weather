from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(max_length=255, required=True)
    # password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput())


class UserUpdateForm(forms.Form):
    username = forms.CharField(max_length=255, required=False)
    name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(max_length=255, required=False)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)
