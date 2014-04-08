
from xml.dom import minidom
import urllib2
import logging


class XMLAnalyser():
    url = "https://adeweb.univ-lorraine.fr/jsp/webapi?"
    request = ""
    session_id = ""
    projectId = "9"
    projectSet = False

    def get_session_id(self):
        temp = self.craft_url({"function": "connect", "login": "ade_projet_etu", "password": ";projet_2014"})
        logging.error(temp)

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
        return minidom.parseString(page.read())

    def query(self, ):
        if self.session_id is "":
            self.session_id = XMLAnalyser.get_session_id()

        if self.projectId is "":
            self.projectId = XMLAnalyser.get_project_id()

        if not self.projectSet:
            self.set_project_id()