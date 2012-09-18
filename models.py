import os
import markdown

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

    def body(self):
        source = open(self.path).read()
        return renderer.convert(source)
