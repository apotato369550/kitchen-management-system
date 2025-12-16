from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


class UserCreateForm(UserCreationForm):
    """Form for creating new users (admin only)"""

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Management', 'Management'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})
        self.fields['email'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Add user to selected group
            role = self.cleaned_data['role']
            group = Group.objects.get(name=role)
            user.groups.add(group)
        return user


class UserEditForm(forms.ModelForm):
    """Form for editing existing users (admin only)"""

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Management', 'Management'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

        # Set initial role based on user's current group
        if self.instance and self.instance.pk:
            if self.instance.groups.filter(name='Admin').exists():
                self.fields['role'].initial = 'Admin'
            elif self.instance.groups.filter(name='Management').exists():
                self.fields['role'].initial = 'Management'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Update user's group
            role = self.cleaned_data['role']
            user.groups.clear()
            group = Group.objects.get(name=role)
            user.groups.add(group)
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with Tailwind styling"""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password'
        })
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form with Tailwind styling"""

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Current password'
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'New password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm new password'
        })
    )
