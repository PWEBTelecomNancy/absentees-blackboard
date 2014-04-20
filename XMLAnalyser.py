from xml.dom import minidom
import urllib2
import logging
import codecs


class XMLAnalyser():
    url = "https://adeweb.univ-lorraine.fr/jsp/webapi?"
    request = ""
    session_id = ""
    projectId = "9"
    projectSet = False

    def get_session_id(self):
        temp = self.craft_url({"function": "connect", "login": "ade_projet_etu", "password": ";projet_2014"})
        xml_data = self.get_xml(temp)

        session_id = xml_data.childNodes[0].getAttribute("id")

        return session_id

    def get_project_id(self):
        queryUrl = self.craft_url({"function": "getProjects", "sessionId": self.session_id, "detail": 2})
        xmlString = self.get_xml(queryUrl)
        pass

    def set_project_id(self):
        queryUrl = self.craft_url({"function": "setProject", "sessionId": self.session_id, "projectId": self.projectId})
        self.get_xml(queryUrl)
        self.projectSet = True

    def craft_url(self, parameters):
        request = self.url

        for i in parameters:
            request = request + "&" + i + "=" + parameters[i]

        return request

    def get_xml(self, url):
        page = urllib2.urlopen(url)
        logging.error(url)
        content = page.read()

        return minidom.parseString(content)

    def query(self, parameters):
        if self.session_id is "":
            self.session_id = self.get_session_id()

        if self.projectId is "":
            self.projectId = self.get_project_id()

        if not self.projectSet:
            self.set_project_id()

        parameters["sessionId"] = self.session_id

        query = self.craft_url(parameters)
        logging.error(query)
        xml = self.get_xml(query)

        return xml

    def get_members(self):
        clubs_list = dict()

        x = self.query({"function": "getResources", "detail": "13", "tree": "false"})
        resources = x.getElementsByTagName("resource")

        for x in range(0, resources.length):
            item = resources[x]
            if item.getAttribute("category") == "category5": # category5 <- most students
                groups = item.getElementsByTagName("memberships")
                groups = groups[0].childNodes


                # print groups.toprettyxml()
                for y in range(0, groups.length):
                    group = groups[y]

                    if group.nodeName == "membership":
                        if group.getAttribute("name") not in clubs_list :
                            clubs_list[group.getAttribute("name")] = list()

                        clubs_list[group.getAttribute("name")].append(item.getAttribute("name"))

        return clubs_list

    def get_lessons(self):
        """
        You can see an example of the output here:
        https://github.com/PWEBTelecomNancy/abstentees-blackboard/wiki/XMLAnalyser.py#get_lessons
        """
        x = self.query({"function": "getActivities", "detail": "17", "tree": "true"})

        folders = x.getElementsByTagName("folder")

        #print "folders a une taille de %d." % folders.length

        fetchedLessons = dict()

        for folder in folders:
            # In one folder, there are things such as
            # Examen Anglais 1A
            # Colorations 3A
            # Gestion de masses de donnees 2A IAMD-SIE
            for activity in folder.getElementsByTagName("activity"):
                name = activity.getAttribute("name")
                # Possible names are: (without the group details)
                # TD TEC 1A apprentissage
                # TD TEC 2A
                #print name

                events = activity.getElementsByTagName("event")

                # Careful: some lessons have zero events.. For now I disregard
                # 		   them, but would be nice to know more about those.
                if len(events) > 0:
                    lesson_name = events[0].getAttribute("name")
                    # print "---> %s" % lesson_name


                    fetchedLessons[lesson_name] = list();

                    for x in range(0, events.length):

                        data = dict()
                        data["startHour"] = events[x].getAttribute("startHour")
                        data["endHour"] = events[x].getAttribute("endHour")
                        data["date"] = events[x].getAttribute("date")
                        data['subject'] = lesson_name
                        data['trainee'] = list()


                        # Parse event details, such as teacher, students, room
                        event_details = events[x].getElementsByTagName("eventParticipant")
                        for event_detail in event_details:
                            ev_category = event_detail.getAttribute("category")
                            ev_name = event_detail.getAttribute("name")
                            #print "ev_cat: %s; ev_name: %s" % (ev_category, ev_name)

                            if "trainee" in ev_category:
                                #print "type equals trainee"
                                data['trainee'].append(ev_name)
                            elif "classroom" in ev_category:
                                #print "type equals classroom"
                                data['classroom'] = ev_name
                            elif "instructor" in ev_category:
                                #print "type equals instructor"
                                data['instructor'] = ev_name

                        #fetchedLessons['lesson_name'] = data;
                        #print lesson_name
                        #print data

                        # Save data into a list into a dict that has a key like
                        # "lesson_name". Though, be careful not to overwrite!
                        fetchedLessons[lesson_name].append(data)

        # You may see an example of what it looks like here:
        # https://github.com/PWEBTelecomNancy/abstentees-blackboard/wiki/XMLAnalyser.py#get_lessons
        return fetchedLessons