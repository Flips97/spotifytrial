import base64
import requests
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from rest_framework import status, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Create your views here.

class SpotifyRequestUserAuthorization(GenericViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        client_id = "83b44a7b22594e3887d5f9d79089f64b"

        response_type = "code"

        redirect_url = "http://localhost:8000/api/spotify/callback"

        scope = "user-read-private user-read-email"

        state = "your_user_id"

        base_url = "https://accounts.spotify.com/authorize"

        url = (
            f"{base_url}?response_type={response_type}&client_id{client_id}&redirect_url={redirect_url}&scope={scope}"
            f"&state={state}"
        ) 
        return redirect(url)
    
def store_code(code: str, user_id: str):
    raise NotImplementedError

class SpotifyCallback(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        code = request.query_params.get("code")

        state = request.query_params.get("state")

        store_code(code, state)
        # return Response(status=status.HTTP_200_OK, data={"code": code})
        return render(request, 'callback_template.html', {'code': code})

class SpotifyRequestAccessToken(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        code = request.data["code"]

        redirect_url = "http://localhost:8000/api/spotify/callback"

        grant_type = "authorization_code"

        client_id = "83b44a7b22594e3887d5f9d79089f64b"
        client_secret = "d221122007f7445c95bb8197fd32aadf"
        authorization = f"{client_id}:{client_secret}"
        authorization = base64.b64encode(authorization.encode()).decode()

        url = "http://accounts.spotify.com/api/token"
        data = {
            "form": {"grant_type": grant_type, "code": code, "redirect_url": redirect_url},
            "header": {"Authorization": f"Basic {authorization}"},
        }

        response = request.post(url, data=data["form"], headers=data["header"])

        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")
        expires_in = response.get("expires_in", 3600)

        # return Response(status=status.HTTP_200_OK, data=response)
        return redirect('/')

    def refresh_access_token(self, refresh_token):
        grant_type = "refresh_token"

        client_id = "83b44a7b22594e3887d5f9d79089f64b"
        client_secret = "d221122007f7445c95bb8197fd32aadf"
        authorization = f"{client_id}:{client_secret}"
        authorization = base64.b64encode(authorization.encode()).decode()

        url = "http://accounts.spotify.com/api/token"
        data = {
            "grant_type": grant_type,
            "refresh_token": refresh_token,
        }
        headers = {
            "Authorization": f"Basic {authorization}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url, data=urlencode(data), headers=headers)

        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")
        expires_in = response.get("expires_in", 3600)

        # return response.json()
        return redirect('/')
    

    


    



