
from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _


class LoginForm(auth_forms.AuthenticationForm):
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(
        attrs={'class': 'form-control mb-3 form-control-sm', 'placeholder': 'Username', 'title': _('Please enter username')}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Password', 'title': _('Please enter password')}))

    def confirm_login_allowed(self, user):
        pass


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(label=_('Current Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Current Password'), 'title': _('Please enter old password')}))
    new_password1 = forms.CharField(label=_('New Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('New Password'), 'title': _('Please enter new password')}),
        help_text=_("Password should have at least 12 characters"))
    new_password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Confirm Password'), 'title': _('Please confirm new password')}))
