from time import strftime,strptime
from datetime import date, timedelta

from handler.BaseHandler import *
from model.ADECommunicator import *
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
                users_groups = get_groups_of_a_user(current_user.name)
                users_lessons = get_lessons_of_groups(users_groups, all_lessons)

                # Let's filter the lessons that are this week
                # 1) Get the date of the beginning of the week
                start_week = date.today() - timedelta(days = date.today().weekday())
                end_week   = date.today() + timedelta(days = (6 - date.today().weekday()))

                start_week = start_week.strftime("%d/%m/%Y")
                end_week   = end_week.strftime("%d/%m/%Y")
                start_week_tuple = start_week.split('/')
                end_week_tuple = end_week.split('/')

                start_week_tuple = (start_week_tuple[2], start_week_tuple[1], start_week_tuple[0])
                end_week_tuple = (end_week_tuple[2], end_week_tuple[1], end_week_tuple[0])

                # 2) Parse each lesson and see if it's in the range
                filtered_lessons = list()

                for lesson in users_lessons:
                    for one_lesson in users_lessons[lesson]:
                        date_lesson = one_lesson['date'].split('/')
                        date_lesson = (date_lesson[2], date_lesson[1], date_lesson[0])
                        if start_week_tuple <= date_lesson <= end_week_tuple:
                            filtered_lessons.append(one_lesson)
                            print "<Bonne date"
                        else:
                            logging.error(start_week_tuple)
                            logging.error(date_lesson)
                            logging.error(end_week_tuple)

                return filtered_lessons
            else:
                return None
        else:
            return None

    def get(self):
        my_lessons = self.filter_lessons_of_week()
        logging.error(">>>>>>>>>>>>>>>>>>>>>END OF THE FILTER<<<<<<<<<<<<<<<<<<<<<")
        logging.error("Result:")
        logging.error(my_lessons)

        if my_lessons is None:
            # User is not logged in
            self.write("Please login!")
        else:
            ClassWeekHandler.renderTemp(self)

    def post(self):
        el=self.request.get('day_button')
        if el:
            ClassWeekHandler.renderTemp(self, el)
        else:
            ClassWeekHandler.renderTemp(self, el)

    def renderTemp(self, selected_day='0'):


        #Here days is a dict with 7 entry : one per day from monday tu sunday
		days_classes = dict()

		monday_ex = dict()
		tuesday_ex = dict()
		wednesday_ex = dict()
        # based on ADECommunicator example
        # The height of each class_box is computed with start_time and end_time
        
		monday_ex[0] = {"class_name": "CM PGWEB 2A IL", "group": ["2A IL", "2A TRS"], "start_time": "8h00", "end_time": "10h00",
                "teacher_name": "CHAROY FRANCOIS"}
		monday_ex[1] =  {"class_name": "TP PGWEB 2A IL", "group": ["2A IL", "2A TRS"], "start_time": "10h00", "end_time": "12h00",
                "teacher_name": "CHAROY FRANCOIS"}
		monday_ex[2] =  {"class_name": "TD MOCI 2A G1", "group": ["2A G1"], "start_time": "14h00", "end_time": "16h00",
                "teacher_name": "CHAROY FRANCOIS"}
                
		tuesday_ex[0] = {"class_name": "Exam PWEB", "group": ["2A IL"], "start_time": "16h00", "end_time": "17h00",
                "teacher_name": ""}
		tuesday_ex[1] =  {"class_name": "Something ...", "group": ["2A"], "start_time": "17h00", "end_time": "18h00",
                "teacher_name": "CHAROY FRANCOIS"}
                
		wednesday_ex[0] = {"class_name": "TP PGWEB 2A IL", "group": ["2A IL", "2A TRS"], "start_time": "10h00", "end_time": "12h00",
                "teacher_name": "CHAROY FRANCOIS"}
		wednesday_ex[1] = {"class_name": "projet 2A pidr", "group": ["2A"], "start_time": "14h00", "end_time": "17h00",
                "teacher_name": "Prof you want ..."}

        #for the exemple I'll add the same classes, we'll be adapted with loops later ....
        # lessons must be add in chronological order
		days_classes[0]=monday_ex
		days_classes[1]=tuesday_ex
		days_classes[2]=wednesday_ex
		days_classes[3]=monday_ex
		days_classes[4]=monday_ex
        
        # I have an empty week, should try with someone who have something to do this week
        # list of all lessons = do we have to sort it day by day ??
		# days_classes = self.filter_lessons_of_week()
		
		week_nb = strftime("%W")
		year = strftime("%Y")
		buff = strptime('%s %s 1' %(year,week_nb), '%Y %W %w')
		buff2 = strptime('%s %s 0' %(year,week_nb), '%Y %W %w')

		first_day=strftime("%A %d %B",buff)
		last_day=strftime("%A %d %B",buff2)

		class_parameters = {'days':days_classes,'first_day':first_day,'last_day':last_day,'selected_day':selected_day}

		self.render('class_week.html', **class_parameters)
