from BaseHandler import *
import logging
from XMLAnalyser import XMLAnalyser
from google.appengine.api import memcache

class ClassAbsenteesHandler(BaseHandler):
    temp_prof_name = "CHAROY FRANCOIS"

    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "class_absentees"

    def get(self):

        group_to_display_example ="2A IL"
        tags_exemple = {'IL':'2A IL','LE':'2A LE','TRS':'2A TRS'}
        ClassAbsenteesHandler.renderTemp(self,group_to_display_example,tags_exemple)

    def post(self):
        tag_clicked = self.request.get('tag')

        if tag_clicked:
            tags_exemple = {'IL':'2A IL','LE':'2A LE','TRS':'2A TRS'}
            group_example = tags_exemple[tag_clicked]
            ClassAbsenteesHandler.renderTemp(self,group_example,tags_exemple)
        else:
            self.redirect('/class_absentees')


    def renderTemp(self,group_to_display="",group_tags=""):

        groups = memcache.get("group_list")

        if groups is None:
            logging.error("CACHE MISS StudentsListHandler l. 24")
            parser = XMLAnalyser()
            groups = parser.get_members()
            memcache.set("group_list", groups)

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