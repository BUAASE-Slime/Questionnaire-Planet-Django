from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128)
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="旧密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password_1 = forms.CharField(label="新密码1", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password_2 = forms.CharField(label="新密码2", max_length=256,
                                     widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label="旧邮箱", max_length=256)