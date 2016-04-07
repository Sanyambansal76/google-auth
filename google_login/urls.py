from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', 'google_login.views.google_login', name="google_login"),
    url(r'^authentication/$', 'google_login.views.google_authentication', name="google_authentication"),
    url(r'^email-form/$', 'google_login.views.google_email_form', name="google_email_form"),
    ]
