__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Accounts import *
from handler.ClassAbsenteesHandler import *
from handler.ClassWeekHandler import *
from model.Absentees import *
from util import *

class HomeHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        super(HomeHandler, self).__init__()
        self.initialize(request, response)
        self.ade_communicator = ADECommunicator()
        self.classweekhandler = ClassWeekHandler()
        self.page_name = "home"

    def get_current_lesson(self):
        if 'user_id' in self.request.cookies:
            current_user = get_connected_user(self.request.cookies['user_id'])
            current_lesson=None
            if current_user is not None:
                current_date = self.date_details.strftime("%d/%m/%Y")
                current_hour = self.date_details.strftime("%H:%M")

                #example (IL):
                #current_date = "14/04/2014"
                #current_hour = "09:30"

                student_name = get_account_from_id(self.request.cookies.get('user_id').split('|')[0]).name
                teacher = get_is_teacher_from_id(self.request.cookies.get('user_id').split('|')[0])

                (start, end, lessons_of_week, previous_week, next_week) = \
                    self.classweekhandler.get_lessons_of_week(student_name, current_date, teacher)

                for lesson in lessons_of_week:
                    if current_date == lesson['date']:
                        if current_hour >= lesson['startHour'] and lesson['endHour']>=current_hour:
                            current_lesson=lesson
                            return current_lesson
        return current_lesson


    def get(self):
        if 'user_id' in self.request.cookies:
            current_user = get_connected_user(self.request.cookies['user_id'])
            if current_user is not None:
                absentees_j=dict()
                absentees_u=dict()
                absentees = get_absentees_from_student_name(current_user.name)
               #Example :
               #absentee = Absentees(student_name=current_user.name, student_email="mail",
               #                            student_group="2A",
               #                           class_title="CM ...",
               #                           teacher_name="prof ..",
               #                            start_hour="8:00",
               #                             end_hour="10:00",
               #                            class_date="15/04/2014", justification_bool=True, justification_text="was sleeping ...")
               # absentee.put()
                for a in absentees:
                    if a.justification_bool:
                        absentees_j[len(absentees_j)]=a
                    else:
                        absentees_u[len(absentees_u)]=a
                teacher_bool = get_is_teacher_from_id(self.request.cookies.get('user_id').split('|')[0])
                current_lesson=self.get_current_lesson()

                self.render('home_co.html',absenteesJ=absentees_j,absenteesU=absentees_u, lesson = current_lesson,name=current_user.name,isteacher=teacher_bool)

            else:
                # User is not logged in
                self.render('home.html')
        else:
            # User is not logged in
            self.render('home.html')

    def post(self):
        if 'user_id' in self.request.cookies:
            current_user = get_connected_user(self.request.cookies['user_id'])
            if current_user is not None:
                if self.request.get('show_abs'):
                    absentees = get_absentees_from_student_name(current_user.name)
                    self.render("absentees_monitor_results.html", absentees=absentees,search_object="All")
