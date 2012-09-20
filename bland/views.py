import os
import time
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response
from django.utils.http import http_date
from .models import Root, Resource, NotFound


def root(cms_root):
    """
    A view that will render a basic site based on the
    directory layout of the provided path
    """
    root = Root(cms_root)
    def view(request, path):
        status = 200
        try:
            page = root.lookup(os.path.join(cms_root, path))
            response = _response(page)
            response['Last-Modified'] = _http_date(page.date())
        except NotFound as e:
            response = _response(e.resource(root))
            response.status_code = 404
        return response
    return view


def _response(page):
    return render_to_response('bland/resource.html',
        {'page': page})


def _http_date(datetime):
    """
    the ludicrous amount of work required in python date/time libs
    """
    return http_date(time.mktime(datetime.timetuple()))
