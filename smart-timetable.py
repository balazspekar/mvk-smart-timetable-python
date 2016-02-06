# -*- coding: utf-8 -*-

import urllib.parse, urllib.request, time, os
from datetime import datetime, date


class StationScreen():

    def __init__(self, station_id):
        self.station_id = station_id
        self.raw_data = self._fetch_raw_data()
        self.clean_data = self._clean()
        self.seconds_to_go = 0

    def _fetch_raw_data(self):
        url = 'http://owa.mvkzrt.hu:8080/android/handler.php'
        values = {'SMART' : self.station_id}
        data = urllib.parse.urlencode(values)
        binary_data = data.encode('utf_8')
        req = urllib.request.Request(url, binary_data)
        response = urllib.request.urlopen(req)
        raw_result = str(response.read())
        result = raw_result.split("\\n")
        return result

    def _clean(self):
        result = []
        lines = []
        for i in range(len(self.raw_data)):
            lines.append(self.raw_data[i].split("|"))
        for i in range(len(lines) - 1):
            fixed_vehicle_id = lines[i][0]
            fixed_vehicle_id = fixed_vehicle_id[-2:]
            result.append(fixed_vehicle_id)
            result.append(lines[i][2])
        return result

    def refresh(self):
        self.raw_data = self._fetch_raw_data()
        self.clean_data = self._clean()

    def display(self):
        for i in range(len(self.clean_data)):
            if i % 2 == 0:
                arrival_time = datetime.strptime(self.clean_data[i + 1], '%H:%M:%S').time()
                seconds_until_arrival = datetime.combine(date.today(), arrival_time) - datetime.combine(date.today(), datetime.now().time())
                seconds_until_arrival_int = seconds_until_arrival.seconds
                self.seconds_to_go = seconds_until_arrival_int
                # minutes_until_arrival_int = round(seconds_until_arrival_int / 60, 1)
                minutes_until_arrival_int = (seconds_until_arrival_int // 60) + 1

                if seconds_until_arrival_int <= 30:
                    minutes_until_arrival_int = "Arriving"
                elif seconds_until_arrival_int > 86000:
                    minutes_until_arrival_int = "Arrived"
                elif seconds_until_arrival_int <= 60:
                    minutes_until_arrival_int = str(minutes_until_arrival_int) + " minute until arrival"
                else:
                    minutes_until_arrival_int = str(minutes_until_arrival_int) + " minutes until arrival"

                print(self.clean_data[i] + " > " + str(arrival_time)[:-3] + " > " + str(minutes_until_arrival_int) + "  (~" + str(seconds_until_arrival_int) + "sec)")

# Instantiating StationScreen objects
laev_to_downtown = StationScreen("514")
laev_to_diosgyor = StationScreen("513")

print(laev_to_diosgyor.display())
print(laev_to_downtown.display())

