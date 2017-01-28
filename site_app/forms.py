from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from site_app.models import User, UserType, Faculty, Topic


class UserTypeCreationForm(forms.ModelForm):
    class Meta:
        model = UserType
        fields = ('type_name',)


class UserTypeChangeForm(forms.ModelForm):
    class Meta:
        model = UserType
        fields = ('type_name',)


class FacultyCreationForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ('code', 'name')


class FacultyChangeForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ('code', 'name')


class TopicCreationForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'student', 'supervisor', 'level', 'voted_for', 'available', 'checked')


class TopicChangeForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'student', 'supervisor', 'level', 'voted_for', 'available', 'checked')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']

