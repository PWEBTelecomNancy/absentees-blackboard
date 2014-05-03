from time import strftime, strptime
from datetime import date, timedelta, datetime

from handler.BaseHandler import *
from model.Accounts import *
from util import *


class ClassWeekHandler(BaseHandler):
    ade_communicator = None

    def __init__(self, request=None, response=None):
        super(ClassWeekHandler, self).__init__()
        self.initialize(request, response)
        self.page_name = "class_week"
        self.ade_communicator = ADECommunicator()

    def search_lessons(self, start_week_tuple, end_week_tuple, users_lessons):
        # 2) Parse each lesson and see if it's in the range
        filtered_lessons = list()

        for lesson in users_lessons:
            for one_lesson in users_lessons[lesson]:
                date_lesson = one_lesson['date'].split('/')
                date_lesson = (int(date_lesson[2]), int(date_lesson[1]), int(date_lesson[0]))
                if start_week_tuple <= date_lesson <= end_week_tuple:
                    filtered_lessons.append(one_lesson)
                    # Right date
                else:
                    # Wrong date
                    pass

        return filtered_lessons

    def get_lessons_of_week(self, username, str_date_to_look_for, teacher=False):
        all_lessons = self.ade_communicator.get_lessons()

        if teacher is True:
            users_lessons = get_lessons_of_a_teacher(username, all_lessons)
        else:
            users_groups = get_extended_groups_of_a_user(
                get_groups_of_a_user(username, self.ade_communicator.get_students_groups()))
            users_lessons = get_lessons_of_groups(users_groups, all_lessons)

        date_to_look_for = self.date_details.strptime(str_date_to_look_for, "%d/%m/%Y")

        # Let's filter the lessons that are this week
        # 1) Get the date of the beginning/end of the week

        start_week = date_to_look_for - timedelta(days=date_to_look_for.weekday())
        end_week = date_to_look_for + timedelta(days=(6 - date_to_look_for.weekday()))

        start_week_str = start_week.strftime("%d/%m/%Y")
        end_week_str = end_week.strftime("%d/%m/%Y")
        start_week_tuple = start_week_str.split('/')
        end_week_tuple = end_week_str.split('/')

        start_week_tuple = (int(start_week_tuple[2]), int(start_week_tuple[1]), int(start_week_tuple[0]))
        end_week_tuple = (int(end_week_tuple[2]), int(end_week_tuple[1]), int(end_week_tuple[0]))

        return start_week, end_week, \
               self.search_lessons(start_week_tuple, end_week_tuple, users_lessons), \
               start_week - timedelta(weeks=1), \
               start_week + timedelta(weeks=1)

    def sort_lessons(self, lessons):
        sorted_list = dict()
        for x in range(0, 6):
            sorted_list[x] = list()

        for lesson in lessons:
            lesson_date = self.date_details.strptime(lesson['date'], "%d/%m/%Y")
            sorted_list[lesson_date.weekday()].append(lesson)

        for weekday in sorted_list:
            sorted_list[weekday].sort(key=lambda x: int(x['startHour'].split(':')[0]))

        return sorted_list

    def get(self):
        if 'user_id' in self.request.cookies:
            current_user = get_connected_user(self.request.cookies['user_id'])

            if current_user is not None:
                arg_date = self.request.get('date', self.date_details.strftime("%d/%m/%Y"))

                teacher = get_is_teacher_from_id(self.request.cookies.get('user_id').split('|')[0])
                (start, end, my_lessons, previous_week, next_week) = \
                    self.get_lessons_of_week(current_user.name, arg_date, teacher)

                sorted_lessons = self.sort_lessons(my_lessons)

                self.render('class_week.html', days=sorted_lessons,
                            first_day=start, last_day=end,
                            previous_week=previous_week,
                            next_week=next_week)

            else:
                # User is not logged in
                self.write("Please login!")
        else:
            # User is not logged in
            self.write("Please login!")

