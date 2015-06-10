import ue9
import os
from time import time, sleep
import numpy as np, pylab as plt
"""
Radio telescope tools
"""
def get_jd(t): return t/86400. + 2440587.5

Spectrometer = False

d = ue9.UE9()
#f = open('TestData', 'w')
#f.write('Volts MicroWatts\n')

def V2freq(V): return 79.25*V + 880.55

def set_dac0(Volt,d):
	fb = d.feedback(DAC0Enabled=True,DAC0=d.voltageToDACBits(Volt),DAC0Update=True)
	return fb

def set_dac1(Volt,d):
	fb = d.feedback(DAC1Enabled=True,DAC1=d.voltageToDACBits(Volt),DAC1Update=True)
	return fb

count = 0
period = 200
width=4.8/period
#"count" takes "period" steps of "width" volts, and then resets to zero
# so for (count,period,width) of (0,24,0.2), we get a range of 0 V to 4.8 V

# Time interval in seconds between steps
dt = 0.1

# Default is the middle of the range
fb = d.feedback(DAC0Enabled=True,DAC0=d.voltageToDACBits(2.4),DAC0Update=True)
sleep(2)

"""
Streaming plot "Plotly" setup
"""

import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

py.sign_in('saulkohn','rwawordhbz') #<-- from my login page.

#setup stream credentials (make sure everything lands in the right place)
tls.set_credentials_file(stream_ids=["wsxq4jq3dz","nreqw9fxaz","75so5954pp","voduofa1vs"])
stream_ids = tls.get_credentials_file()['stream_ids']
stream_id = stream_ids[0]

#declare the stream and format it
stream = Stream(token=stream_id,maxpoints=100)
trace1 = Scatter(x=[], y=[], mode='lines+markers', stream=stream)
data = Data([trace1])
layout = Layout(title='miniPCRT: Voltage vs. Time')
fig = Figure(data=data, layout=layout)

#this should launch the Chrome window with the relevant axes
unique_url = py.plot(fig, filename='miniPCRTstream')

#get the stream ready to get data
s = py.Stream(stream_id)
s.open()

"""
Connect to telescope
"""

os.system('rm RadioTelescope.txt')
f=open("RadioTelescope.txt","w")

print 'JD  COUNT INPUT_VOLTS V2FREQ_MHz VRCVR DBM MICROW'
f.write('JD  COUNT INPUT_VOLTS V2FREQ_MHz VRCVR DBM MICROW\n')
while True:
	t = time() # this algorithm does give the correct time in utc
	if Spectrometer:
		# Do the frequency ramp
		if count > period: count = 0

		if (count >= 0 and count <= period):
			fb = d.feedback(DAC0Enabled=True,DAC0=d.voltageToDACBits(width*count),DAC0Update=True)
		count += 1

	jd = get_jd(t)
	V_rcvr = d.readRegister(0)
	V_therm1 = d.readRegister(2)
	V_rcvr_empty = d.readRegister(4)
	V_therm2 = d.readRegister(6)
	dBm = -5./0.12*(V_rcvr-0.639)
	mW = 10.**(dBm/10.)
	microW = mW *1000.
# Temperature calibration 
#	A = 0.00000238
#	B = 0.002836
#	T =  (mW-B)/A

	sleep(dt)
	
	"""
	WRITE JD AND ONE OTHER DATA PRODUCT TO THE STREAM
	"""
	try: s.write(dict(x=jd, y=V_rcvr))
	except KeyboardInterrupt: break
	"""
	"""
	
	print jd,count,width*count,V2freq(width*count),round(V_rcvr,2),dBm,microW
	f.write("%.7f %.3i %.3f %.3f %.3f %.3f %.3f"%(jd,count,width*count,V2freq(width*count),round(V_rcvr,2),dBm,microW))
	f.write("\n")
	f.flush()

s.close() #<--- shut off stream
f.close()