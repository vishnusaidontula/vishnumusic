from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Album, Song
from .forms import AlbumForm, UserForm, SongForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# *
# Index Function is used render index page that the user views.
# Is_authenticated: Is used to to authenticate the user and if he is not, then render to Login Page again.
# albums: Returns a new QuerySet containing objects that match the given lookup parameters. (With the help of filter)
# songs: Retreiving all the objects in the database.
# query: Search at index page has access to the q value in request.GET. Hence show results accordingly
#


class IndexView(LoginRequiredMixin, ListView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    template_name = 'music/album_list.html'
    context_object_name = 'albums'

    ''' get_queryset: Get the list of items for this view '''
    def get_queryset(self):
        return Album.objects.filter(user = self.request.user) 

def index(request):
     if not request.user.is_authenticated:
         return render(request, 'music/login.html')
     else:
         albums = Album.objects.filter(user=request.user)
         song_results = Song.objects.all()
         query = request.GET.get("q")
         if query:
             albums = albums.filter(Q(album_title__icontains=query) | Q(artist__icontains=query)).distinct()
             song_results = song_results.filter(Q(song_title__icontains=query)).distinct()
             return render(request, 'music/publicsongs.html', {
                 'albums': albums,
                 'songs': song_results,
             })
         else:
             return render(request, 'music/publicsongs.html', {'albums': albums})




    



class AlbumDetail(LoginRequiredMixin, DetailView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    template_name = 'music/detail.html'

    def detail(request, album_id):
        if not request.user.is_authenticated:
            return render(request, 'music/login.html')
        else:
            user = request.user
            album = get_object_or_404(Album, pk=album_id)
            return render(request, 'music/detail.html', {'album': album, 'user': user})


class AlbumCreate(LoginRequiredMixin, CreateView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    fields = ['album_title','artist','genre','album_logo']

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(AlbumCreate, self).form_valid(form)


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    fields = ['album_title','artist','genre','album_logo']

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(AlbumUpdate, self).form_valid(form)


    def create_album(request):
     if not request.user.is_authenticated:
         return render(request, 'music/login.html')
     else:
         form = AlbumForm(request.POST or None, request.FILES or None)
         if form.is_valid():
             album = form.save(commit=False)
             album.user = request.user
             album.album_logo = request.FILES['album_logo']
             file_type = album.album_logo.url.split('.')[-1]
             file_type = file_type.lower()
             if file_type not in IMAGE_FILE_TYPES:
                 context = {
                     'album': album,
                     'form': form,
                     'error_message': 'Image file must be PNG, JPG, or JPEG',
                 }
                 return render(request, 'music/create_album.html', context)
             album.save()
             return render(request, 'music/detail.html', {'album': album})
         context = {
             "form": form,
         }
         return render(request, 'music/create_album.html', context)



class AlbumDelete(LoginRequiredMixin, DeleteView):
    login_url = 'login_user/'
    redirect_field_name = 'redirect_to'
    model = Album
    success_url = reverse_lazy('music:album_list')

    def delete_album(request, album_id):
        album = Album.objects.get(pk=album_id)
        album.delete()
        albums = Album.objects.filter(user=request.user)
        return render(request, 'music/index.html', {'albums': albums})



def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)




def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})






class LoginView(View):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/album_list.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})


    def get(self, request):
        return render(request, 'music/login.html')

    def login_user(request):
     if request.method == "POST":
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(username=username, password=password)
         if user is not None:
             if user.is_active:
                 login(request, user)
                 albums = Album.objects.filter(user=request.user)
                 return render(request, 'music/index.html', {'albums': albums})
             else:
                 return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
         else:
             return render(request, 'music/login.html', {'error_message': 'Invalid login'})
     return render(request, 'music/login.html')


class LogoutView(View):
	def get(self, request):
		logout(request)
		form = UserForm(request.POST or None)
		context = {
			"form": form,
		}
		return render(request, 'music/login.html', context)

def logout_user(request):
        logout(request)
        form = UserForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, 'music/login.html', context)

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/album_list.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)



def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'q':
                users_songs = users_songs.filter(filter_by)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


def publicsongs(request):
    songs=Song.objects.filter(type='ty1')
    return render(request,'music/publicsongs.html',{'songs':songs})


def publicalbum(request):
    al=Album.objects.filter(type='ty1')
    return render(request,'publicalbum.html',{'album':al})