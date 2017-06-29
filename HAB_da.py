import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import urllib
from StringIO import StringIO

flight_id = '3f2e3ebf76f973da7d395e753752fec8'
payload_id = '3f2e3ebf76f973da7d395e75374d9f06'

key = '%22' + flight_id + '%22,%22' + payload_id + '%22'
z = 0

time = '10:45:'
def launch(time):
    s1 = ['0','1','2','3','4','5']
    s2 = ['0','1','2','3','4','5','6','7','8','9']
    seconds = []
    launch = []
    for s1_1 in s1:
        for s2_1 in s2:
            s = s1_1 + s2_1
            seconds.append(s)
    for s in seconds:
        ntime = time + s
        launch.append(ntime)
        
    return launch  

launch = launch(time)
fp=urllib.urlopen('http://habitat.habhub.org/habitat/_design/ept/_list/csv/payload_telemetry/flight_payload_time?include_docs=true&startkey=['+key+']&endkey=['+key+',[]]&fields=sentence_id,time,latitude,longitude,altitude,satellites,speed,heading,temperature_external,battery,bmp,temperature_external2,humidity,pressure,pitch,roll,yaw,x,y,z')

data = np.genfromtxt(StringIO(fp.read()), dtype=None, delimiter=',', names=True)


for x in np.nditer(data):
    z += 1
    for l in launch:
        if l == x['time']:
            start = z
            break 


data = data[start:]
print data


#x = np.arange(0, len(data['altitude']))
x = data['time']
y = data['altitude']

x = [datetime.datetime.strptime(elem, '%H:%M:%S') for elem in x]
fig, ax = plt.subplots()
plt.plot(x, y)

ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))

plt.title('Altitude vs Time')
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()
