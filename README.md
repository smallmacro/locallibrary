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


5. `{{ form.as_table }}` will render them as table cells wrapped in <tr> tags
`{{ form.as_p }}` will render them wrapped in <p> tags
`{{ form.as_ul }}` will render them wrapped in <li> tags

6. Write automated tests. 
`Unit tests`: Verify functional behavior of individual components, often to class and function level.
`setUpTestData()` is called once at the beginning of the test run for class-level setup. You'd use this to create objects that aren't going to be modified or changed in any of the test methods.
`setUp() `is called before every test function to set up any objects that may be modified by the test (every test function will get a "fresh" version of these objects).

The most essential thing in writing a unit test is focusing on the desired design in code, not the  Django built-in function or third-party libraries.

One worth to mention is the relationship between some test functions may be recuresive. For example ,`fun1()` contains `step A`and `step B`, while `fun2()`may contains `step A`, `step B` and `step C`.

7. Before deploying the application, we need to:
- Make a few changes to your project settings.
- Choose an environment for hosting the Django app.
- Choose an environment for hosting any static files.
- Set up a production-level infrastructure for serving your website.

`python manage.py check --deploy` can automatically check settings security before deployment.

### Things need to be done:
1. automatically check the status of book instance
2. manage the borrowed books with due date, list them or remind the borrower with a email .
3. set the limitation number  of books a borrower can take. 
4. Need a good design for the website.

### Confused

1. how the `session` will be used in more complicated ways.
2. Writing `Unit Test` seems to be a boring and tedious job which may take much time. How it would be in real production?    