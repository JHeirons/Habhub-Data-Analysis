import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import datetime
import urllib
from StringIO import StringIO

flight_id = '3f2e3ebf76f973da7d395e753752fec8'
payload_id = '3f2e3ebf76f973da7d395e75374d9f06'
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

def getData(f_id, p_id):
    key = '%22' + f_id + '%22,%22' + p_id + '%22'
    fp=urllib.urlopen('http://habitat.habhub.org/habitat/_design/ept/_list/csv/payload_telemetry/flight_payload_time?include_docs=true&startkey=['+key+']&endkey=['+key+',[]]&fields=sentence_id,time,latitude,longitude,altitude,satellites,speed,heading,temperature_external,battery,bmp,temperature_external2,humidity,pressure,pitch,roll,yaw,x,y,z')
    data = np.genfromtxt(StringIO(fp.read()), dtype=None, delimiter=',', names=True)
    return data

data = getData(flight_id, payload_id)


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
y = data['satellites']
y2 = data['altitude']

x = [datetime.datetime.strptime(elem, '%H:%M:%S') for elem in x]
fig, ax1 = plt.subplots()
ax1.plot(x, y, 'b-')
ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))
plt.setp(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')

ax2 = ax1.twinx()
ax2.plot(x, y2, 'r-')


plt.show()
