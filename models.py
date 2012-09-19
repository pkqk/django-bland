import os
import codecs
import datetime
from django.utils.safestring import mark_safe
import markdown
import yaml


class NotFound(Exception):
    def __init__(self, message):
        super(NotFound, self).__init__("Missing: %s" % message)

class Resource(object):
    renderer = markdown.Markdown()

    @classmethod
    def locate(cls, path):
        if not path or path.endswith('/'):
            path += 'index'
        path += '.txt'
        if os.path.exists(path):
            return cls(path)
        else:
            raise NotFound(path)

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
        return mark_safe(self.renderer.convert(self.source))

    def __getitem__(self, key):
        return self.meta[key]

    def title(self):
        try:
            return self['title']
        except KeyError:
            return self['heading']

    def date(self):
        if 'date' in self.meta:
            return self.meta['date']
        else:
            return datetime.date.fromtimestamp(os.stat(self.path).st_mtime)

