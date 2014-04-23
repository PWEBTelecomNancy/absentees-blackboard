from BaseHandler import *
from ADECommunicator import *
import time
import re


class ClassAbsenteesHandler(BaseHandler):
    temp_prof_name = "CHAROY FRANCOIS"
    ade_communicator = None

    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "class_absentees"
        self.ade_communicator = ADECommunicator()

    def get(self):
        #Test user connexion and privileges
        if self.is_connected() and get_is_teacher_from_id(self.request.cookies.get('user_id').split('|')[0]):
            #First, get the class the teacher should have right now
            class_to_display = self.ade_communicator.get_teacher_class(self.temp_prof_name,
                                                                       time.strftime("%H:%M"),
                                                                       time.strftime("%d/%m/%Y"))
            #Then, we get the students for this class
            students_list = []
            groups = self.ade_communicator.get_students_groups()
            if class_to_display is not None:
                for group_name in groups:
                    for group_to_find in class_to_display['groups']:
                        if re.match(group_to_find, group_name) is not None:
                            temp = []
                            for student in groups[group_name]:
                                temp.append({"name": student, "group": group_name})

                            students_list.extend(temp)

                students_list.sort(key=lambda x: x['name'])

                #Render the page
                self.render("class_absentees.html", students=students_list, **class_to_display)
            else:
                self.render("message.html", title="No lessons found!", subtitle="Looks like you don't have to work!")
        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not a teacher nor a connected user")

    def post(self):
        pass