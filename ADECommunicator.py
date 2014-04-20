__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from XMLAnalyser import *
from google.appengine.api import memcache


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

        if groups is None:
            logging.error("CACHE MISS ADECommunicator get_students_groups()")
            groups = self.parser.get_members()
            memcache.set("group_list", groups, time=self.default_cache_long_prune)

        return groups

    def get_teacher_class(self, teacher, time, date):
        all_lessons = memcache.get("lessons_list")
        if all_lessons is None:
            logging.error("CACHE MISS ADECommunicator get_teacher_class()")
            all_lessons = self.parser.get_lessons()

            memcache.set("lessons_list", all_lessons, time=self.default_cache_short_prune)

        teacher_classes = list()

        # Subject looks like 'TP TNI 2A G11'
        for subject in all_lessons:

            # lesson is a list of:
            # [ ...,
            # {'classroom': u'AIPL 3',
            # 'date': u'10/12/2013',
            # 'endHour': u'18:00',
            # 'instructor': u'SCHEID JEAN-FRANCOIS',
            # 'startHour': u'14:00',
            # 'trainee': [u'2A G11']},
            # ...,
            # ]
            for lesson in all_lessons[subject]:

                if 'instructor' in lesson.keys():
                    if lesson['instructor'] == teacher:
                        teacher_classes.append(lesson)

        #logging.error("Result")
        #logging.error(teacher_classes)

        first_step = list()

        # Filter by date
        for lesson in teacher_classes:
            if lesson['date'] == date:
                first_step.append(lesson)

        final_step = None
        # Filter by time
        my_time = time.split(':')
        my_time[0] = int(my_time[0])
        my_time[1] = int(my_time[1])

        for lesson in first_step:
            lesson_start_time = lesson['startHour'].split(':')
            lesson_start_time[0] = int(lesson_start_time[0])
            lesson_start_time[1] = int(lesson_start_time[1])
            lesson_end_time = lesson['endHour'].split(':')
            lesson_end_time[0] = int(lesson_end_time[0])
            lesson_end_time[1] = int(lesson_end_time[1])

            # if we are the same hours, compare minutes
            if lesson_start_time[0] == my_time[0]:
                if lesson_start_time[1] <= my_time[1]:
                    final_step = lesson
            elif lesson_end_time[0] == my_time[0]:
                if my_time[1] <= lesson_end_time[1]:
                    final_step = lesson
            # else if hours are not the same, compare hours
            elif lesson_start_time[0] < my_time[0] and my_time[0] < lesson_end_time[0]:
                final_step = lesson

        #return {"class_name": "TP PGWEB 2A IL", "groups": ["2A IL", "2A TRS"], "start_time": "10h00", "end_time": "12h00",
        #        "teacher_name": "CHAROY FRANCOIS", "room": "S2.42"}

        if final_step is None:
            return None
        else:
            return {"class_name": final_step["subject"],
                    "groups": final_step["trainee"],
                    "start_time": final_step["startHour"],
                    "end_time": final_step["endHour"],
                    "teacher_name": final_step["instructor"],
                    "room": final_step["classroom"]}