import urllib.parse, urllib.request, time, os
from datetime import datetime, date
from pprint import pprint

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

    def generateLCD(self):
        count = 0
        result = ""
        formatted_arrival_times = []
        formatted_until_arrivals = []

        for i in range(len(self.clean_data)):
            # based on clean_data put every even line into this list
            if i % 2 != 0:
                formatted_arrival_times.append(self.clean_data[i])

        for i in range(len(formatted_arrival_times)):
            # parsing arrival times now available in formatted_arrival_times into time objects
            arrival_time = datetime.strptime(formatted_arrival_times[i], '%H:%M:%S').time()
            # calculating time delta
            seconds_until_arrival = datetime.combine(date.today(), arrival_time) - datetime.combine(date.today(), datetime.now().time())
            # appending that calculated delta represented in minutes
            formatted_until_arrivals.append(seconds_until_arrival.seconds // 60)
            #formatted_until_arrivals.append(seconds_until_arrival.seconds)

        print(formatted_arrival_times)
        print(formatted_until_arrivals)

        # determining how many times we have
        data_length = len(formatted_until_arrivals)
        # data_length = 2

        # i want to display 5 arrival times on the lcd
        if data_length == 0:
            result = "--\n--\n--\n--\n--\n"
        elif data_length == 1:
            if formatted_until_arrivals[0] < 10:
                result += "0" + str(formatted_until_arrivals[0]) + "\n"
            elif formatted_until_arrivals[0] > 99:
                result += "00\n" #!!
            else:
                result += str(formatted_until_arrivals[0]) + "\n"
            result += "--\n--\n--\n--\n"
        elif data_length == 2:
            for i in range(2):
                if formatted_until_arrivals[i] < 10:
                    result += "0" + str(formatted_until_arrivals[i]) + "\n"
                elif formatted_until_arrivals[i] > 99:
                    result += "00\n" #!!
                else:
                    result += str(formatted_until_arrivals[i]) + "\n"
            result += "--\n--\n--\n"
        elif data_length == 3:
            for i in range(3):
                if formatted_until_arrivals[i] < 10:
                    result += "0" + str(formatted_until_arrivals[i]) + "\n"
                elif formatted_until_arrivals[i] > 99:
                    result += "00\n" #!!
                else:
                    result += str(formatted_until_arrivals[i]) + "\n"
            result += "--\n--\n"
        elif data_length == 4:
            for i in range(4):
                if formatted_until_arrivals[i] < 10:
                    result += "0" + str(formatted_until_arrivals[i]) + "\n"
                elif formatted_until_arrivals[i] > 99:
                    result += "00\n" #!!
                else:
                    result += str(formatted_until_arrivals[i]) + "\n"
            result += "--"
        else:
            for i in range(5):
                if formatted_until_arrivals[i] < 10:
                    result += "0" + str(formatted_until_arrivals[i]) + "\n"
                elif formatted_until_arrivals[i] > 99:
                    result += "00\n" # replace with exclamation marks in all 5 occurences, its here to deal with the 86000 secs issue
                else:
                    result += str(formatted_until_arrivals[i]) + "\n"

        return result


# Instantiating StationScreen objects
laev_to_downtown = StationScreen("514")
laev_to_diosgyor = StationScreen("513")
brightness = "max"
now = datetime.now()

if int(now.strftime("%H")) > 6 and int(now.strftime("%H")) < 22:
    brightness = "max"
else:
    brightness = "min"


with open("result.txt", "w") as result_file:
    result_file.write("Content-Type: text/html\r\n\r" + laev_to_downtown.generateLCD() + "\n" +  laev_to_diosgyor.generateLCD() + "\n" + now.strftime("%H:%M") + "\n" + now.strftime("%Y-%m-%d") + "\n" + brightness)