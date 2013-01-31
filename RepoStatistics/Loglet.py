class Loglet(object):
    def __init__(self):
        self.sha = ''
        self.date = ''
        self.time = ''
        self.datetime = ''
        self.gmt_offset = ''
        self.diffstats = []

    def add_header(self, header):
        sha, remainder = header.strip().split(",", 1)
        time, date, gmt_offset = remainder.split()
        self.sha = sha
        self.date = date
        self.time = time
        self.datetime = "%s %s" % (date, time)
        self.gmt_offset = gmt_offset

    def add_content(self, content):
        pass