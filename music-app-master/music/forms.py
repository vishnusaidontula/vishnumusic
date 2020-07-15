from django.contrib.auth.models import User
from django import forms
from .models import Album, Song

# *
# [AlbumForm]: Form for Album creation.


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo','type']

# *
# [UserForm]: Form for User signup.


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Display password

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# *
# [SongForm]: Form for song creation.


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file','type']
