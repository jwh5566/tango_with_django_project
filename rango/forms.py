from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name.",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category name'}))
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.",
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Page Title'}))
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.",
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Page Url'}))
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category', )

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False,
                             help_text="Please enter your website.",
                             widget=forms.TextInput(attrs={'class': 'form-control'})
                             )
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user',)
