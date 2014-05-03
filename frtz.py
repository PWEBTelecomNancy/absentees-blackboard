__author__ = 'videl'
import datetime


class frtz(datetime.tzinfo):
    DST_OFFSET = datetime.timedelta(hours=+1)
    # In the US, DST starts at 2 am (standard time) on the last Sunday in March,
    # which is the first Sunday on or after March 25.
    DSTSTART = datetime.datetime(1, 3, 25, 2)
    # and ends at 3 am (DST time; 2am standard time) on the last Sunday of Oct.
    # which is the first Sunday on or after Oct 25.
    DSTEND = datetime.datetime(1, 10, 25, 1)

    def utcoffset(self, dt):
        return self.DST_OFFSET + self.dst(dt)

    def tzname(self, dt):
        return "Europe/France"

    def dst(self, dt):
        # Find last Sunday in March & the last in October.
        start = frtz.first_sunday_on_or_after(self.DSTSTART.replace(year=dt.year))
        end = frtz.first_sunday_on_or_after(self.DSTEND.replace(year=dt.year))

        if start <= dt.replace(tzinfo=None) < end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    @staticmethod
    def first_sunday_on_or_after(dt):
        days_to_go = 6 - dt.weekday()
        if days_to_go:
            dt += datetime.timedelta(days_to_go)
        return dt
