# google-auth
Authentication using Google

Quick start
-----------

1. Move to project directory run command::

    pip install git+https://github.com/technoarch-softwares/google-auth

2. Add "google_login" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'google_login',
    )
    
    SITE_URL = 'SITE DOMIAN' #like 'http://localhost:8000/'
    
    ERROR_REDIRECT_URL = 'SITE LOGIN URL'
    
    GOOGLE_CLIENT_ID = 'GOOGLE API KEY'
    
    GOOGLE_CLIENT_SECRET = 'GOOGLE API SECRET'
    
    GOOGLE_REDIRECT_URL = 'google/authentication'

3. Include the google_login URLconf in your project urls.py like this::

    url(r'^google/', include('google_login.urls')),

4. Run `python manage.py migrate` to create the google_login models.

5. It will create a table into database named by google_login_googleprofile.

6. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a google_login (you'll need the Admin app enabled).

7. Visit http://127.0.0.1:8000/google/ to participate in the google authentication.

