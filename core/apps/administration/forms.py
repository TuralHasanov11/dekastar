
from apps.main.models import (CompanyInfo, ContactEmail, ContactPhone,
                              SiteImage, SiteText, SocialMediaLink)
from apps.store.models import Brand, Category
from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from mptt.forms import TreeNodeChoiceField
from shared import custom_form_fields


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


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label=_('Username'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Username'), 'title': _('Please enter username')}))
    first_name = forms.CharField(label=_('First Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('First Name'), 'title': _('Please enter first name')}))
    last_name = forms.CharField(label=_('Last Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Last Name'), 'title': _('Please enter last name')}))
    email = forms.EmailField(label=_('Email'), max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Email'), 'title': _('Please enter email')}))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Password'), 'title': _('Please enter password')}))
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Password Confirm'), 'title': _('Please confirm password')}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('Please use another Email, that is already taken'))
        return email


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Username'), 'title': _('Please enter username')}))
    first_name = forms.CharField(label=_('First Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('First Name'), 'title': _('Please enter first name')}))
    last_name = forms.CharField(label=_('Last Name'), max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Last Name'), 'title': _('Please enter last name')}))
    email = forms.EmailField(label=_('Email'), max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Email'), 'title': _('Please enter email')}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']


class AboutTextForm(forms.ModelForm):
    language = custom_form_fields.LanguageField()
    about = custom_form_fields.TextField(label=_('About'))

    class Meta:
        model = SiteText
        fields = ['about', 'language']


AboutTextFormSet = forms.modelformset_factory(
    model=SiteText, form=AboutTextForm, max_num=len(settings.LANGUAGES))


class PrivacyPolicyTextForm(forms.ModelForm):
    language = custom_form_fields.LanguageField()
    privacy_policy = custom_form_fields.TextField(label=_('Privacy Policy'))

    class Meta:
        model = SiteText
        fields = ['privacy_policy', 'language']


PrivacyPolicyTextFormSet = forms.modelformset_factory(
    model=SiteText, form=PrivacyPolicyTextForm, max_num=len(settings.LANGUAGES))


class DeliveryPolicyTextForm(forms.ModelForm):
    language = custom_form_fields.LanguageField()
    delivery_policy = custom_form_fields.TextField(label=_('Delivery Policy'))

    class Meta:
        model = SiteText
        fields = ['delivery_policy', 'language']


DeliveryPolicyTextFormSet = forms.modelformset_factory(
    model=SiteText, form=DeliveryPolicyTextForm, max_num=len(settings.LANGUAGES))


class SocialMediaLinkForm(forms.ModelForm):
    platform = forms.ChoiceField(label=_("Platform"), widget=forms.Select(
        attrs={"class": "form-select form-select-sm"}), choices=SocialMediaLink.Platforms.choices)
    link = forms.URLField(label=_('Link'), widget=forms.URLInput(
        attrs={"class": "form-control form-control-sm"}))

    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'link']


class ContactEmailForm(forms.ModelForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(
        attrs={"class": "form-control form-control-sm",
               'placeholder': _("Email"), 'title': _('Please enter email')}))

    class Meta:
        model = ContactEmail
        fields = ['email']


class ContactPhoneForm(forms.ModelForm):
    phone = forms.CharField(label=_("Phone"), widget=forms.TextInput(
        attrs={"class": "form-control form-control-sm", 'placeholder': _("Phone"),
               'title': _('Please enter phone')}))

    class Meta:
        model = ContactPhone
        fields = ['phone']


class CompanyInfoForm(forms.ModelForm):
    language = custom_form_fields.LanguageField()
    address = forms.CharField(label=_('Address'), widget=forms.Textarea(
        attrs={"class": "form-control form-control-sm",
               'placeholder': _('Address'), 'rows': 5,
               'title': _('Please enter address')}))
    working_hours = forms.CharField(label=_('Working Hours'), widget=forms.TextInput(
        attrs={"class": "form-control form-control-sm",
               'placeholder': _('Working Hours'),
               'title': _('Please enter working hours')}))

    class Meta:
        model = CompanyInfo
        fields = ['address', 'language', 'working_hours']


CompanyInfoFormSet = forms.modelformset_factory(
    model=CompanyInfo, form=CompanyInfoForm, max_num=len(settings.LANGUAGES))


class SiteImageForm(forms.ModelForm):
    contact_image = forms.ImageField(label=_('Contact Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm',
               'placeholder': _('Contact Image'),
               'title': _('Please upload contact image'),
               'multiple': False}), required=False)
    about_image = forms.ImageField(label=_('About Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm',
               'placeholder': _('About Image'),
               'title': _('Please upload about image'),
               'multiple': False}), required=False)
    delivery_policy_image = forms.ImageField(label=_('Delivery Policy Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm',
               'placeholder': _('Delivery Policy Image'),
               'title': _('Please upload delivery policy image'),
               'multiple': False}), required=False)
    privacy_policy_image = forms.ImageField(label=_('Privacy Policy Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm',
               'placeholder': _('Privacy Policy Image'),
               'title': _('Please upload privacy policy image'),
               'multiple': False}), required=False)

    class Meta:
        model = SiteImage
        fields = ['contact_image', 'about_image',
                  'delivery_policy_image', 'privacy_policy_image']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': _('Name'), 'title': _('Please enter name')}))
    parent = TreeNodeChoiceField(label=_('Parent'),
                                 queryset=Category.objects.all(), required=False)
    cover_image = forms.ImageField(label=_('Cover Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm',
               'placeholder': _('Cover Image'),
               'title': _('Please upload cover Image'),
               'multiple': False}), required=False)

    class Meta:
        model = Category
        fields = ('name', 'parent', 'cover_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].widget.attrs.update(
            {"class": "form-select form-select-sm"})


class BrandForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm',
               'placeholder': _('Name'), 'title': _('Please enter name')}))
    cover_image = forms.ImageField(label=_('Cover Image'), widget=forms.ClearableFileInput(
        attrs={'class': 'form-control form-control-sm',
               'placeholder': _('Cover Image'),
               'title': _('Please upload cover Image'),
               'multiple': False}), required=False)

    class Meta:
        model = Brand
        fields = ('name', 'cover_image')
