from django import forms
from game.models import Game, Category, UserProfile
from django.contrib.auth.models import User

# Form for Category
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                          help_text="Please enter the category name.")

    amount = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class GameForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the game title.")
    publisher = forms.CharField(max_length=128,
                            help_text="Please enter the game publisher.")
    url = forms.URLField(help_text="Please enter the url.")
    picture = forms.ImageField(help_text="Please choose the picture.")
    mark = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Game
        exclude = ('category',)
        fields = ('title','publisher','url','picture',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('https://'):
            url = 'https://' + url
            cleaned_data['url'] = url

        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('picture',)



