from Diffstat import Diffstat

class Loglet(object):
    def __init__(self):
        self.sha = ''
        self.date = ''
        self.time = ''
        self.datetime = ''
        self.gmt_offset = ''
        self.diffstats = None

    def add_header(self, header):
        sha, remainder = header.strip().split(",", 1)
        time, date, gmt_offset = remainder.split()
        self.sha = sha
        self.date = date
        self.time = time
        self.datetime = "%s %s" % (date, time)
        self.gmt_offset = gmt_offset

    def add_content(self, content):
        lines_added, lines_deleted, filename = content.split()
        d = Diffstat()
        d.lines_added = lines_added
        d.lines_deleted = lines_deleted
        d.filename = filename
        if self.diffstats is None:
            self.diffstats = [d]
        else:
            self.diffstats = self.diffstats.append(d)