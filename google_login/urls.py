from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', 'google_login.views.google_login', name="google_login"),
    url(r'^authentication/$', 'google_login.views.google_authentication', name="google_authentication"),
    ]
