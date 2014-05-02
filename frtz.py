__author__ = 'videl'
import datetime


class frtz(datetime.tzinfo):
    CONSTANT = datetime.timedelta(hours=+1)

    def utcoffset(self, dt):
        return self.CONSTANT + self.dst(dt)

    def tzname(self, dt):
        return "Europe/France"

    def dst(self, dt):
        return datetime.timedelta(hours=+1)