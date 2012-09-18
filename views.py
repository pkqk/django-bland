import os
from django.http import HttpResponse, HttpResponseNotFound
from .models import Resource, NotFound


def root(cms_root):
    """
    A view that will render a basic site based on the
    directory layout of the provided path
    """
    def view(request, path):
        try:
            page = Resource.locate(os.path.join(cms_root, path))
        except NotFound as e:
            return HttpResponseNotFound(str(e))
        return HttpResponse(page.body())
    return view
