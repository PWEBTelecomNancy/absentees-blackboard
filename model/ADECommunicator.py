__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.api import memcache

from model.XMLAnalyser import *


class ADECommunicator():
    """
    This class's task is to use/maintain/check/refresh the cache.
    Create new methods to manage ADE data in the cache.
    """
    parser = None
    default_cache_long_prune = 604800000
    default_cache_short_prune = default_cache_long_prune / 2

    def __init__(self):
        self.parser = XMLAnalyser()

    def get_students_groups(self):
        groups = memcache.get("group_list")
        #raise Exception("I know python!")

        if groups is None:
            self.reload_groups()

        else:
            logging.error("CACHE HIT ADECommunicator get_students_groups()")

        return groups

    def get_lessons(self):
        all_lessons = memcache.get("lessons_list")
        if all_lessons is None:
            self.reload_lessons()

        else:
            logging.error("CACHE HIT ADECommunicator get_lessons()")

        return all_lessons

    def preload(self):
        self.get_students_groups()
        self.get_lessons()
