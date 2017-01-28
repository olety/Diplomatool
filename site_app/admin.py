from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from site_app.models import User, UserType, Faculty, Topic, Thesis, Review, Defense


class UserTypeCreationForm(forms.ModelForm):
    class Meta:
        model = UserType
        fields = ('type_name',)


class UserTypeChangeForm(forms.ModelForm):
    class Meta:
        model = UserType
        fields = ('type_name',)


class UserTypeAdmin(admin.ModelAdmin):
    form = UserTypeChangeForm
    add_form = UserTypeCreationForm
    list_display = ('type_name',)


class FacultyCreationForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ('code', 'name')


class FacultyChangeForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ('code', 'name')


class FacultyAdmin(admin.ModelAdmin):
    form = FacultyChangeForm
    add_form = FacultyCreationForm
    list_display = ('code', 'name')


class TopicCreationForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'student', 'supervisor', 'level', 'voted_for', 'available', 'checked')


class TopicChangeForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'student', 'supervisor', 'level', 'voted_for', 'available', 'checked')


class TopicAdmin(admin.ModelAdmin):
    form = TopicChangeForm
    add_form = TopicCreationForm
    list_display = ('name', 'student', 'supervisor', 'level', 'voted_for', 'available', 'checked')


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


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'degree', 'faculty', 'type', 'department', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
            {'fields': ('first_name',
                        'last_name',
                        'degree',
                        'faculty',
                        'type',
                        'department')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    search_fields = ('email', 'first_name', 'last_name', 'degree', 'faculty', 'type', 'department')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()


class ThesisCreationForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ('supervisor', 'student', 'topic', 'finished', 'reviewed', 'short_description')


class ThesisChangeForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ('supervisor', 'student', 'topic', 'finished', 'reviewed', 'short_description')


class ThesisAdmin(admin.ModelAdmin):
    form = ThesisChangeForm
    add_form = ThesisChangeForm
    list_display = ('supervisor', 'student', 'topic', 'finished', 'reviewed', 'short_description')


class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('thesis', 'topic', 'is_finished', 'finished_date')


class ReviewChangeForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('thesis', 'topic', 'is_finished', 'finished_date')


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewChangeForm
    add_form = ReviewCreationForm
    list_display = ('thesis', 'topic', 'is_finished', 'finished_date')


class DefenseCreationForm(forms.ModelForm):
    class Meta:
        model = Defense
        fields = ('thesis', 'date', 'successful', 'second_defense')


class DefenseChangeForm(forms.ModelForm):
    class Meta:
        model = Defense
        fields = ('thesis', 'date', 'successful', 'second_defense')


class DefenseAdmin(admin.ModelAdmin):
    form = DefenseChangeForm
    add_form = DefenseCreationForm
    list_display = ('thesis', 'date', 'successful', 'second_defense')


# Registering models
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Defense, DefenseAdmin)
