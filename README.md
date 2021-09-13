# locallibrary

Locallibrary application with Django 
This code pratice follows the tutorial of [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)



### New Concepts learned:

1. `session` attribute can be accessed from the `request` parameter.
```python
# Get a session value by its key (e.g. 'my_car'), raising a KeyError if the key is not present
my_car = request.session['my_car']

# Get a session value, setting a default if it is not present ('mini')
my_car = request.session.get('my_car', 'mini')

# Set a session value
request.session['my_car'] = 'mini'

# Delete a session value
del request.session['my_car']

def index(request):
    ...

    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)

```

2. `path('accounts/', include('django.contrib.auth.urls'))` adds the following URLs with names in square brackets:
```python
accounts/ login/ [name='login']
accounts/ logout/ [name='logout'] #default template name 'logged_out.html'
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset'] #password_reset_form.html
accounts/ password_reset/done/ [name='password_reset_done'] #password_reset_done.html
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm'] #password_reset_confirm.html
accounts/ reset/done/ [name='password_reset_complete']  #password_reset_complte.html

```

3.  Authentication and permissions(Authorization)

Model :Defining permissions is done on the model "class Meta" section, using the permissions field.

Template:The current user's permissions are stored in a Template variable called {{ perms }}

Views:Django use `decorator` (`login_required`, `permission_required`) in function base view to implement the authentication and permission while use `mixins` (`LoginRequiredMixin`, `PermissionRequiredMixin`)in class base view.

```python
#function base view 
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')
def my_function(request):
    pass 


#class base view 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class MyClassView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = ('catalog.can_mark_returned','catalog.can_edit')
    pass

```

4. `admin.py`can control the `list_display` and `list_filter`in admin site by `decorators`.
