import os
import codecs
import datetime
from django.utils.safestring import mark_safe
from django.http import Http404
import markdown
import yaml


class NotFound(Exception):
    def __init__(self, message):
        super(NotFound, self).__init__("Missing: %s" % message)

    def resource(self, root):
        try:
            return root.lookup('not-found')
        except NotFound:
            raise Http404


class Root(object):

    def __init__(self, basedir):
        self.base = basedir

    def lookup(self, path):
        path = os.path.join(self.base, path)
        if not path or path.endswith('/'):
            path += 'index'
        path += '.txt'
        if os.path.exists(path):
            return Resource(path)
        else:
            raise NotFound(path)


class Resource(object):
    """
    An object to represent a resource at a specific url

    maps to a file on disk and renders it from markdown to html
    """

    renderer = markdown.Markdown()

    def __init__(self, path):
        self.path = path
        data = codecs.open(path, encoding='utf-8').read()
        try:
            meta, self.source = data.split('---\n', 1)
            self.meta = yaml.load(meta)
        except ValueError:
            self.meta = {}
            self.source = data

    def body(self):
        """
        Convert the source of the page from markdown to html
        """
        return mark_safe(self.renderer.convert(self.source))

    def __getitem__(self, key):
        return self.meta[key]

    def title(self):
        return self.meta.get('title') or self.meta.get('heading')

    def date(self):
        """
        If the page data contains a date use that otherwise use
        the mtime of the file
        """
        if 'date' in self.meta:
            return self.meta['date']
        else:
            return datetime.datetime.fromtimestamp(
                os.stat(self.path).st_mtime)
