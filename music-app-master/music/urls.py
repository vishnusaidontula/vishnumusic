from django.urls import path
from . import views

# app_name: For music application. Makes clear to user to which app he/she is working on.
app_name = 'music'
urlpatterns = [
    path('', views.publicsongs,name='publicsongs'),
    path('index', views.IndexView.as_view(), name='album_list'),
    path('register/', views.register, name='register'),
    path('login_user/', views.LoginView.as_view(), name='login_user'),
    path('logout_user/', views.LogoutView.as_view(), name='logout_user'),
    # /music/71/
    path('<int:pk>/', views.AlbumDetail.as_view(), name='detail'),
    path(r'songs/(?P<filter_by>[a-zA_Z]+)/', views.songs, name='songs'),
    # /music/album/add/
    path('album/add/', views.AlbumCreate.as_view(), name='create_album'),
    # /music/album/1
    path(r'album/<int:pk>/', views.AlbumUpdate.as_view(), name='update_album'),
    # /music/<album_id>/create_song/
    path('<int:album_id>/create_song/', views.create_song, name='create_song'),
    # /music/<int:album_id>/delete_song/<int:song_id>/
    path('<int:album_id>/delete_song/<int:song_id>/', views.delete_song, name='delete_song'),
    # /music/album/2/delete/
    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='delete_album'),
    path('publicsongs', views.publicsongs),
    path('publicalbums', views.publicalbum),
]
