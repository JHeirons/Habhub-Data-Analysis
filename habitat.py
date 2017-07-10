import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import datetime
import urllib
from StringIO import StringIO
import sys


reload(sys)
sys.setdefaultencoding('utf8')

import couchdbkit

db = couchdbkit.Server("http://habitat.habhub.org")["habitat"]
flights = db.view("flight/end_start_including_payloads", include_docs=True)

#name = raw_input("Flight Name: ")
name = 'Panda Launch PITS'
t = '10:45:'

def addSeconds(t):
    s1 = ['0','1','2','3','4','5']
    s2 = ['0','1','2','3','4','5','6','7','8','9']
    seconds = []
    launch = []
    for s1_1 in s1:
        for s2_1 in s2:
            s = s1_1 + s2_1
            seconds.append(s)
    for s in seconds:
        ntime = t + s
        launch.append(ntime)
        
    return launch  

launch = addSeconds(t)



def getFlight(flight_data, flight_name):
    p_id = ""
    f_id = ""
    field = ""

    for flight in flight_data:
        if flight["doc"]["name"] == flight_name:
            f_id = flight["doc"]["_id"]
            p_id = flight["doc"]["payloads"][0]

        elif flight["doc"]["_id"] == p_id:
            sentence = flight["doc"]["sentences"][0]["fields"]
            for i in sentence:
                field = field + i["name"] +','
        
        else:
            print 'Not a valid flight name'
        
    flight_info = [f_id, p_id, field]
    return flight_info

flight = getFlight(flights, name)
print flight[2]


def getData(f_info):
    
    key = '%22' + f_info[0] + '%22,%22' + f_info[1] + '%22'

    fp=urllib.urlopen('http://habitat.habhub.org/habitat/_design/ept/_list/csv/payload_telemetry/flight_payload_time?include_docs=true&startkey=['+key+']&endkey=['+key+',[]]&fields=' + f_info[2])
    data = np.genfromtxt(StringIO(fp.read()), dtype=None, delimiter=',', names=True)
    return data

data = getData(flight)


def fromTime(data, launch):
    z = 0
    for x in np.nditer(data):
        z += 1
        for l in launch:
            if l == x['time']:
                start = z
                break  
    data = data[start:]
    return data

data = fromTime(data, launch)


x = data['time']
y = data['altitude']
#y2 = data['pressure']

x = [datetime.datetime.strptime(elem, '%H:%M:%S') for elem in x]
plt.style.use('ggplot')

fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True)
ax1.plot(x, y)
#ax2.plot(x, y2)

ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=20))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))

ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=20))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax2.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))

ax1.set_title('Altitude vs Time')
ax1.set_ylabel('Altitude (m)')
ax1.set_xlabel('Time')
plt.setp(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')

ax2.set_title('Pressure vs Time')
ax2.set_ylabel('Pressure (hector pascals)')
ax2.set_xlabel('Time')
plt.setp(ax2.get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()
