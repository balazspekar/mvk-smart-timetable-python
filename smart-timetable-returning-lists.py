# -*- coding: utf-8 -*-

import re
import urllib.parse
import urllib.request
from datetime import date, datetime


class Schedule:
    def __init__(self, station_id):
        self.station_id = station_id
        self.raw_data = self.fetch_raw_data()
        self.departure_times = self.extractDepartureTimes(self.raw_data)
        self.remaining_seconds = []

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

    def update_remaining_seconds(self):
        remaining_seconds = []
        now = datetime.now()
        time_format = '%H:%M:%S'

        for time in self.departure_times:
            arrival_time = datetime.strptime(time, time_format).time()
            arrival_time = datetime.combine(date.today(), arrival_time)
            diff = arrival_time - now
            diff_seconds = round(diff.total_seconds())

            if diff_seconds < 0:
                remaining_seconds.append(0)
            else:
                remaining_seconds.append(diff_seconds)

        self.remaining_seconds = remaining_seconds


if __name__ == '__main__':
    schedule = Schedule("514")
    schedule.update_remaining_seconds()
    print(schedule.remaining_seconds)
