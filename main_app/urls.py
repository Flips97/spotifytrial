from django.urls import path
from .views import SpotifyRequestUserAuthorization, SpotifyCallback, SpotifyRequestAccessToken
urlpatterns = [
    path('api/spotify/request-authorization/', SpotifyRequestUserAuthorization.as_view({'get': 'list'}), name='spotify-request-authorization'),
    path('api/spotify/callback/', SpotifyCallback.as_view({'get': 'list'}), name='spotify-callback'),
    path('api/spotify/request-access-token/', SpotifyRequestAccessToken.as_view({'post': 'create'}), name='spotify-request-access-token'),
]

