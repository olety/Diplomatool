from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from site_app.models import User, Faculty, Topic, Thesis, Review, Defense
from site_app import forms


class FacultyAdmin(admin.ModelAdmin):
    form = forms.FacultyChangeForm
    add_form = forms.FacultyCreationForm
    list_display = ('code', 'name')


class TopicAdmin(admin.ModelAdmin):
    form = forms.TopicChangeForm
    add_form = forms.TopicCreationForm
    list_display = ('name', 'student', 'supervisor', 'level', 'short_description', 'voted_for', 'available', 'checked')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'index_number', 'degree',
                    'faculty', 'department', 'has_proposed_topic', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
            {'fields': ('first_name',
                        'last_name',
                        'degree',
                        'index_number',
                        'faculty',
                        'groups',
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


class ThesisAdmin(admin.ModelAdmin):
    form = forms.ThesisChangeForm
    add_form = forms.ThesisChangeForm
    list_display = ('supervisor', 'student', 'topic', 'finished', 'reviewed')


class ReviewAdmin(admin.ModelAdmin):
    form = forms.ReviewChangeForm
    add_form = forms.ReviewCreationForm
    list_display = ('author', 'thesis', 'file', 'finished_date', 'deadline')


class DefenseAdmin(admin.ModelAdmin):
    form = forms.DefenseChangeForm
    add_form = forms.DefenseCreationForm
    list_display = ('thesis', 'date', 'successful', 'second_defense')


# Registering models
admin.site.register(User, UserAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Defense, DefenseAdmin)
