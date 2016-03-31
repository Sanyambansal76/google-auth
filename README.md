# Google-auth
Google-auth is an easy to setup google authentication/registration mechanism with support for the Django Framework



Quick start
-----------

1. Installation:

    `pip install git+https://github.com/technoarch-softwares/google-auth`

2. Add `"google_login"` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (
    
        ...
    
        'google_login',
    
    )
    
3.   Add this lines to your project settings file:   
    
    `SITE_URL = 'SITE DOMIAN' #like 'http://localhost:8000/'`
    
    `ERROR_REDIRECT_URL = 'SITE LOGIN URL'`

    `GOOGLE_REDIRECT_URL = 'google/authentication'`

4.  Add Google Secret Keys and Client Id    
    
    `GOOGLE_CLIENT_ID = 'GOOGLE API KEY'`
    
    `GOOGLE_CLIENT_SECRET = 'GOOGLE API SECRET'`
    

5. Include the google_login URLconf in your project urls.py like this::

    `url(r'^google/', include('google_login.urls')),`

6. Run `python manage.py migrate` to create the `google_login` models.

7. It will create a table into database named by `google_login_googleprofile`.

8. Visit http://127.0.0.1:8000/google/ to participate in the google authentication.

