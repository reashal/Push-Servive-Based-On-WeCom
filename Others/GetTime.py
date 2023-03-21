import time


class GetTime(object):
    def __init__(self):
        ti = time.time()
        ti = time.localtime(ti)
        self.tm_year = str(ti.tm_year)
        self.tm_mon = str(ti.tm_mon)
        self.tm_day = str(ti.tm_mday)
        self.tm_hour = str(ti.tm_hour)
        self.tm_min = str(ti.tm_min)
        self.tm_sec = str(ti.tm_sec)

    def get_time(self):
        ti = "%s年%s月" % (
            self.tm_year, self.tm_mon)
        # print(ti)
        return ti

    def get_day(self):
        return str(self.tm_day)

    def get_hour(self):
        return str(self.tm_hour)

    def get_minute(self):
        return str(self.tm_min)

    def get_second(self):
        return str(self.tm_sec)


if __name__ == '__main__':
    x = GetTime()
