from crispy_forms.layout import Layout, Fieldset, Submit, ButtonHolder, Field, Hidden, Div, Button
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from site_app.models import User, Faculty, Topic, Thesis, Review, Defense
from crispy_forms.helper import FormHelper
from . import models


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
        fields = ('name', 'student', 'supervisor', 'short_description', 'level', 'voted_for', 'available', 'checked')


class TopicChangeForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'student', 'supervisor', 'short_description', 'level', 'voted_for', 'available', 'checked')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password. Attributes:
        password1, password2
    Class contains useful methods for the password processing:
        clean_password2(), save(commit)
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        """
        Meta class describes which (if any) this form represents. It is used by internal Django functions.
        """
        model = User
        fields = ('email', 'first_name', 'last_name', 'index_number')

    def clean_password2(self):
        # Check that the two passwords match
        """
        Checks if two given passwords match each other.

        :raises: ValidationError
        :return: Correct password
        :rtype: string
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        """
        Saves the passwords from the form

        :param commit: (bool) If True then the password is saved in database, if False it is only saved in form
        :return: User for which the passwords were given
        :rtype User
        """
        # Save the provided password
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
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


class ThesisCreationForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ('supervisor', 'student', 'topic', 'finished')


class ThesisChangeForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ('supervisor', 'student', 'topic', 'finished')


class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('author', 'thesis', 'file', 'finished_date')


class ReviewChangeForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('author', 'thesis', 'file', 'finished_date')


class DefenseCreationForm(forms.ModelForm):
    class Meta:
        model = Defense
        fields = ('thesis', 'date', 'successful', 'second_defense')


class DefenseChangeForm(forms.ModelForm):
    class Meta:
        model = Defense
        fields = ('thesis', 'date', 'successful', 'second_defense')


class StudentTopicProposalForm(forms.Form):
    name = forms.CharField(max_length=100)
    supervisor = forms.ChoiceField(choices=[(supervisor.id, supervisor.__str__()) for supervisor in
                                            models.User.objects.filter(groups__name='Supervisor')])
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(StudentTopicProposalForm, self).__init__(*args, *kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary btn-lg btn-block'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-default btn-lg btn-block'))


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper['username'].wrap(Field, placeholder='email@pwr.edu.pl')
        self.helper['password'].wrap(Field, placeholder='password')
        self.helper.error_text_inline = False
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-primary btn-lg btn-block'))
        self.helper.form_show_labels = False


class ReviewUploadForm(forms.Form):
    """
    Form for uploading files containing review of the thesis. Consists of attributes:
        review_file
    """
    review_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        """
        Constructor for the review file form. Arguments *args and **kwargs are not used but are required for correct
        implementation of this function.
        """
        super(ReviewUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper['review_file'].label = 'Upload a review'
        self.helper.add_input(Hidden('review_hidden_id', 'Review'))
        self.helper.add_input(Submit('submit', 'Upload review', css_class='btn btn-primary btn-lg btn-block'))
        self.helper.render_hidden_fields = True
