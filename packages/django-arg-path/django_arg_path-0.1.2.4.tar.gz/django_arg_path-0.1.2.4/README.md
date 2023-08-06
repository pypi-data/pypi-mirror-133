
This package helps you write shorter and cleaner codes by supporting the useage of one views with multiple urls in django. 
These urls and views are static but supports any extra dynamic slug, str, int etc.


Useage is simple

Here is our urls.py file


```sh

from django_arg_path import arg_path

urlpatterns = [
  arg_path('en', '', home, name='home_en',
  arg_path('ru', 'ru', home, name='home_ru',
  arg_path('es', 'es', home, name='home_es',
]

```


Here is our views.py file

```sh

def home(request, static_arg=''):
    # static_arg variable gives us en, ru and es as a string which we included in the beginning of our path
    return render(request, static_arg+'.html')

```

So this one views.py file creates 3 pages named '', 'ru' and 'es'

Something like that
127.0.0.1:8000/,
127.0.0.1:8000/ru,
127.0.0.1:8000/es,

