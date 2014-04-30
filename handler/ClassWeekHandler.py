from time import strftime, strptime
from datetime import date, timedelta, datetime

from handler.BaseHandler import *
from model.Accounts import *
from util import *


class ClassWeekHandler(BaseHandler):
    ade_communicator = None

    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "class_week"
        self.ade_communicator = ADECommunicator()

    def filter_lessons_of_week(self):
        all_lessons = self.ade_communicator.get_lessons()

        if 'user_id' in self.request.cookies:
            current_user = get_connected_user(self.request.cookies['user_id'])

            if current_user is not None:
                users_groups = get_extended_groups_of_a_user(current_user.name)
                users_lessons = get_lessons_of_groups(users_groups, all_lessons)

                # Let's filter the lessons that are this week
                # 1) Get the date of the beginning of the week

                # <<<<<< USE THIS TO SEE THE PREVIOUS WEEK'S LESSONS >>>>>> #
                #start_week = date.today() - timedelta(days=date.today().weekday() + 7)
                #end_week = date.today() + timedelta(days=(6 - date.today().weekday()) - 7)
                # This is the correct version down there
                start_week = date.today() - timedelta(days=date.today().weekday())
                end_week = date.today() + timedelta(days=(6 - date.today().weekday()))

                start_week = start_week.strftime("%d/%m/%Y")
                end_week = end_week.strftime("%d/%m/%Y")
                start_week_tuple = start_week.split('/')
                end_week_tuple = end_week.split('/')

                start_week_tuple = (int(start_week_tuple[2]), int(start_week_tuple[1]), int(start_week_tuple[0]))
                end_week_tuple = (int(end_week_tuple[2]), int(end_week_tuple[1]), int(end_week_tuple[0]))

                # 2) Parse each lesson and see if it's in the range
                filtered_lessons = list()

                for lesson in users_lessons:
                    for one_lesson in users_lessons[lesson]:
                        date_lesson = one_lesson['date'].split('/')
                        date_lesson = (int(date_lesson[2]), int(date_lesson[1]), int(date_lesson[0]))
                        if start_week_tuple <= date_lesson <= end_week_tuple:
                            filtered_lessons.append(one_lesson)
                            #print "<Bonne date"
                        else:
                            #print "Mauvaise date"
                            pass

                return filtered_lessons
            else:
                return None
        else:
            return None
    def sort_lessons(self, lessons):
        sorted = dict()
        for x in range(0, 6):
            sorted[x] = list()

        for lesson in lessons:
            lesson_date = datetime.strptime(lesson['date'], "%d/%m/%Y")
            sorted[lesson_date.weekday()].append(lesson)

        for weekday in sorted:
            sorted[weekday].sort(key=lambda x: int(x['startHour'].split(':')[0]))

        return sorted


    def get(self):
        my_lessons = self.filter_lessons_of_week()

        sorted_lessons = self.sort_lessons(my_lessons)

        if my_lessons is None:
            # User is not logged in
            self.write("Please login!")
        else:
            ClassWeekHandler.renderTemp(self, sorted_lessons)

    def post(self):
        my_lessons = self.filter_lessons_of_week()
        sorted_lessons = self.sort_lessons(my_lessons)

        el = self.request.get('day_button')
        if el:
            ClassWeekHandler.renderTemp(self, sorted_lessons, el)
        else:
            ClassWeekHandler.renderTemp(self, sorted_lessons, el)

    def renderTemp(self, lessons):

        #############
        # change "days_classes" by "lessons" and comment all between the two "########"
        # to connect to real datas (no datas to display right now on holiday).
        # here just for example.


        days_classes = dict()

        monday_ex = dict()
        tuesday_ex = dict()
        wednesday_ex = dict()

        monday_ex[0] = {"subject": "CM PGWEB 2A IL", "group": ["2A IL", "2A TRS"], "startHour": "8:00",
                        "endHour": "10:00",
                        "teacher_name": "CHAROY FRANCOIS"}
        monday_ex[1] = {"subject": "TP PGWEB 2A IL", "group": ["2A IL", "2A TRS"], "startHour": "10:00",
                        "endHour": "12:00",
                        "teacher_name": "CHAROY FRANCOIS"}
        monday_ex[2] = {"subject": "TD MOCI 2A G1", "group": ["2A G1"], "startHour": "14:00", "endHour": "16:00",
                        "teacher_name": "CHAROY FRANCOIS"}

        tuesday_ex[0] = {"subject": "Exam PWEB", "group": ["2A IL"], "startHour": "16:00", "endHour": "17:00",
                         "teacher_name": ""}
        tuesday_ex[1] = {"subject": "Something ...", "group": ["2A"], "startHour": "17:00", "endHour": "18:00",
                         "teacher_name": "CHAROY FRANCOIS"}

        wednesday_ex[0] = {"subject": "TP PGWEB 2A IL", "group": ["2A IL", "2A TRS"], "startHour": "10:00",
                           "endHour": "12:00",
                           "teacher_name": "CHAROY FRANCOIS"}
        wednesday_ex[1] = {"subject": "projet 2A pidr", "group": ["2A"], "startHour": "14:00", "endHour": "17:00",
                           "teacher_name": "Prof you want ..."}


        days_classes[0] = monday_ex
        days_classes[1] = tuesday_ex
        days_classes[2] = wednesday_ex
        days_classes[3] = monday_ex
        days_classes[4] = monday_ex
        days_classes[5] = tuesday_ex

        #############

        week_nb = strftime("%W")
        year = strftime("%Y")
        buff = strptime('%s %s 1' % (year, week_nb), '%Y %W %w')
        buff2 = strptime('%s %s 0' % (year, week_nb), '%Y %W %w')

        first_day = strftime("%A %d %B", buff)
        last_day = strftime("%A %d %B", buff2)

        class_parameters = {'days': days_classes, 'first_day': first_day, 'last_day': last_day}

        self.render('class_week.html', **class_parameters)
