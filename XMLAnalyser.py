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
