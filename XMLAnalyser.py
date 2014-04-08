
from xml.dom import minidom
import logging


class XMLAnalyser():
    url = "https://adeweb.univ-lorraine.fr/jsp/webapi?"
    request = ""
    session_id = ""
    projectId = ""


    def get_session_id(self):
        temp = self.craft_url({"function": "connect", "login": "ade_projet_etu", "password": ";projet_2014"})
        xml_data = self.get_xml(temp)
        # 
        session_id = xml_data.childNodes[0].getAttribute("id")

        return session_id

    def get_project_id(self):
        pass

    def craft_url(self, parameters):
        request = self.url

        for i in parameters:
            request = request + "&" + i + "=" + parameters[i]

        return request

    def query(self, ):
        if self.session_id is "":
            self.session_id = XMLAnalyser.get_session_id()

        if self.projectId is "":
            self.projectId = XMLAnalyser.get_project_id()