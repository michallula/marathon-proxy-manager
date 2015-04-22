__author__ = 'michal'


class MarathonPMCommand(object):

    def __call__(self, *args, **kwargs):
        print self.__class__.__name__