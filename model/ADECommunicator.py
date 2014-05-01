__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.api import memcache

from model.XMLAnalyser import *


class ADECommunicator():
    """
    This class's task is to use/maintain/check/refresh the cache.
    Create new methods to manage ADE data in the cache.
    """
    parser = None
    default_cache_long_prune = 604800
    default_cache_short_prune = default_cache_long_prune / 2

    def __init__(self):
        self.parser = XMLAnalyser()

    def get_students_groups(self):
        groups = memcache.get("group_list")
        #raise Exception("I know python!")

        if groups is None:
            logging.error("CACHE MISS ADECommunicator get_students_groups()")
            groups = self.parser.get_members()
            memcache.set("group_list", groups, time=self.default_cache_long_prune)
        else:
            logging.error("CACHE HIT ADECommunicator get_students_groups()")

        return groups

    def get_lessons(self):
        all_lessons = memcache.get("lessons_list")
        if all_lessons is None:
            logging.error("CACHE MISS ADECommunicator get_lessons()")
            all_lessons = self.parser.get_lessons()

            memcache.set("lessons_list", all_lessons, time=self.default_cache_short_prune)
        else:
            logging.error("CACHE HIT ADECommunicator get_lessons()")

        return all_lessons