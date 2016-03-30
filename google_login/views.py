import requests
import urllib2
import urllib
import json
import ast

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_backends, logout
from django.contrib.auth.decorators import login_required

from google_login.models import GoogleProfile
from google_login.utils import create_username


google_redirect_url = settings.SITE_URL + settings.GOOGLE_REDIRECT_URL


def google_login(request):
    """
        To send the request to Google API for the authorization code by the use of client id.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('%s%s' % (settings.SITE_URL, settings.LOGIN_REDIRECT_URL))

    url = 'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=%s&redirect_uri=%s&state=987654321&scope=https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.google.com/m8/feeds/' \
        % (settings.GOOGLE_CLIENT_ID, google_redirect_url)

    return HttpResponseRedirect(url)


def get_google_access_token(code):
    """
        Code is used to get the access token by use of client id and client secret.
    """
    access_token_url = 'https://www.googleapis.com/oauth2/v4/token'

    post_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': google_redirect_url,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
    }

    headers ={
        'Host': 'www.googleapis.com',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(access_token_url, data=post_data, headers=headers)

    response_dict = ast.literal_eval(response.text)

    access_token = response_dict['access_token']

    return access_token


def get_google_user_info(access_token):
    """
        Access token is use for getting the linkedin user info and email address.
    """
    query_string = urllib.urlencode({'access_token': access_token})
    profile_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    profile_response= urllib2.urlopen("%s?%s" % (profile_url, query_string))
    profile_response_dict = json.loads(profile_response.read())
    return (profile_response_dict)


def google_authentication(request):
    """
        It is the main function and view for the Google redirect uri for calling the other functions.
    """
    try:
        code = request.GET['code']
    except:
        messages.error(request, "Sorry we can't log you in. Please try again.")
        return HttpResponseRedirect(settings.ERROR_REDIRECT_URL)

    try:
        access_token = get_google_access_token(code)
    except:
        return HttpResponseRedirect(settings.ERROR_REDIRECT_URL)

    try:
        profile_response_dict = get_google_user_info(access_token)
    except:
        return HttpResponseRedirect(settings.ERROR_REDIRECT_URL)

    member_id = profile_response_dict['id']

    try:
        google_profile = GoogleProfile.objects.get(google_id=member_id)
        user = google_profile.user

        if access_token != google_profile.access_token:
            google_profile.access_token = access_token
            google_profile.save()

        google_profile.profile_data = json.dumps(profile_response_dict)
        google_profile.save()

    except GoogleProfile.DoesNotExist:
        try:
            user = User.objects.get(email__iexact=profile_response_dict['email'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=profile_response_dict['email'],
                username=create_username(profile_response_dict['given_name'].title() + ' ' + profile_response_dict['family_name'].title()),
                first_name = profile_response_dict['given_name'].title(),
                last_name = profile_response_dict['family_name'].title(),
            )

        GoogleProfile.objects.create(
            user=user,
            google_id=member_id,
            access_token=access_token,
            profile_data=json.dumps(profile_response_dict),
        )

    user.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, user)

    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
