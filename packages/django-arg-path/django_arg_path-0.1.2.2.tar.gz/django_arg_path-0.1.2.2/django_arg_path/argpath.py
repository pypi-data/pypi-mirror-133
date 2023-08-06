from functools import partial
from django.urls.resolvers import (URLPattern, URLResolver, RoutePattern, ResolverMatch)


def arg_path(static_arg, *args, **kwargs):

    class URLPatternMulti(URLPattern):
        def resolve(self, path):
            match = self.pattern.match(path)
            if match:
                new_path, args, kwargs = match
                # Pass any extra_kwargs as **kwargs.
                kwargs.update(self.default_args)
                return ResolverMatch(self.callback, args, {**kwargs, **{'static_arg':static_arg}}, self.pattern.name, route=str(self.pattern))


    def _path(route, view, kwargs=None, name=None, Pattern=None):
        from django.views import View

        if callable(view):
            pattern = Pattern(route, name=name, is_endpoint=True)
            return URLPatternMulti(pattern, view, kwargs, name)


    return partial(_path, Pattern=RoutePattern)(*args, **kwargs)


