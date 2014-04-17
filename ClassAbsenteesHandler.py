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
        #First, get the class the teacher should have right now
        class_to_display = self.ade_communicator.get_teacher_class(self.temp_prof_name,
                                                                   time.strftime("%H:%M:%S"),
                                                                   time.strftime("%d/%m/%Y"))

        #Then, we get the students for this class
        students_list = []
        groups = self.ade_communicator.get_students_groups()
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


    def post(self):
        pass
        """tag_clicked = self.request.get('tag')

        if tag_clicked:
            tags_exemple = {'IL':'2A IL','LE':'2A LE','TRS':'2A TRS'}
            group_example = tags_exemple[tag_clicked]
            ClassAbsenteesHandler.render_temp(self,group_example,tags_exemple)
        else:
            self.redirect('/class_absentees')"""

    def render_temp(self,group_to_display="",group_tags=""):
        groups = self.ade_communicator.get_students_groups()

        toDisplay = dict()
        cpt=0;
        for gkey in groups:
            if group_to_display in gkey:
                toDisplay[gkey] = groups[gkey]

        for gkey in groups:
            for v in group_tags.values():
                if v in gkey:
                    for skey in groups[gkey]:
                        cpt+=1

        class_parameters = {'class_name': 'RSA', 'time': ' 10:10 - 12:00', 'teacher': 'Ms Moufida', 'type': 'CM',
                          'room': 'Amphi Nord', 'nb_students': cpt,'groups':toDisplay,'tags':group_tags,'main_tag':group_to_display}

        self.render('class_absentees.html', **class_parameters)