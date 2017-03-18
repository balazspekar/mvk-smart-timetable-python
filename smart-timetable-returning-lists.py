# -*- coding: utf-8 -*-

import pprint
import re
import urllib.parse
import urllib.request


class Schedule:
    def __init__(self, station_id):
        self.station_id = station_id
        self.raw_data = self.fetch_raw_data()
        self.clean_data = self.extractDepartureTimes(self.raw_data)

    def fetch_raw_data(self):
        url = 'http://owa.mvkzrt.hu:8080/android/handler.php'
        values = {'SMART': self.station_id}
        data = urllib.parse.urlencode(values)
        binary_data = data.encode('utf_8')
        req = urllib.request.Request(url, binary_data)
        response = urllib.request.urlopen(req)
        return str(response.read())

    @staticmethod
    def extractDepartureTimes(line):
        regex = r"[0-9]+:[0-9]+:[0-9]+"
        return re.findall(regex, line)  # returns a list of strings like ['12:14:34', '12:20:00'] etc


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(depth=6)
    schedule = Schedule("514")
    print(schedule.clean_data)
