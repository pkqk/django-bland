import os
import codecs
import datetime
from django.utils.safestring import mark_safe
import markdown
import yaml

renderer = markdown.Markdown()

class NotFound(Exception):
    def __init__(self, message):
        super(NotFound, self).__init__("Missing: %s" % message)

class Resource(object):
    @classmethod
    def locate(cls, path):
        if not path or path.endswith('/'):
            path += 'index'
        print "test path: %s" % (path+ '.txt')
        if os.path.exists(path + '.txt'):
            return cls(path, 'txt')
        else:
            raise NotFound(path + '.txt')

    def __init__(self, path, processor):
        self.path = '.'.join([path, processor])
        data = codecs.open(self.path, encoding='utf-8').read()
        try:
            meta, self.source = data.split('---\n', 1)
            self.meta = yaml.load(meta)
        except ValueError:
            self.meta = {}
            self.source = data

    def body(self):
        return mark_safe(renderer.convert(self.source))

    def __getitem__(self, key):
        return self.meta[key]

    def date(self):
        if 'date' in self.meta:
            return self.meta['date']
        else:
            return datetime.date.fromtimestamp(os.stat(self.path).st_mtime)

