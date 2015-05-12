# setup as of 2014/07/14
import ue9
from time import time, sleep
import numpy as np
import pylab as plt

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



#fig = plt.figure()
f=open("RadioTelescope.txt","w")

#info = np.zeros((24,24,24,24,24,24,24,24,24)) #this array holds one loop of the table
#print 'THEORY | OUTPUT'
#print 'JD','COUNT','INPUT_VOLTS','V2FREQ_MHz','|','VRCVR','MICROW','VTHERM1','VEMPTY','VTHERM2'
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
	
	print jd,count,width*count,V2freq(width*count),round(V_rcvr,2),dBm,microW
	f.write("%.7f %.3i %.3f %.3f %.3f %.3f %.3f"%(jd,count,width*count,V2freq(width*count),round(V_rcvr,2),dBm,microW))
	f.write("\n")
	f.flush()


