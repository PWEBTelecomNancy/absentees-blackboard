__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'


class NoSuchParameterException(Exception):
    key = None

    def __init__(self, arg):
        super(NoSuchParameterException, self).__init__(arg)
        self.key = arg

    def get_key(self):
        return self.key