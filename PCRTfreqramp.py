# setup as of 2014/07/14
import ue9
from time import time, sleep
import numpy as np

def get_jd(t): return t/86400. + 2440587.5

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
period = 24
width=0.2
#"count" takes "period" steps of "width" volts, and then resets to zero
# so for (count,period,width) of (0,24,0.2), we get a range of 0 V to 4.8 V

#fb = d.feedback(DAC0Enabled=True,DAC0=d.voltageToDACBits(0.0),DAC0Update=True)
set_dac0(0.0,d)

#info = np.zeros((24,24,24,24,24,24,24,24,24)) #this array holds one loop of the table
print 'THEORY | OUTPUT'
print 'JD','COUNT','INPUT_VOLTS','V2FREQ_MHz','|','VRCVR','MICROW','VTHERM1','VEMPTY','VTHERM2'
while True:
	t = time() # this algorithm does give the correct time in utc
	if count > period: count = 0

	if (count >= 0 and count <= period):
           fb = set_dac0(width*count)
	#if (count >= period and count <= 2*period):
           #fb = d.feedback(DAC0Enabled=True,DAC0=d.voltageToDACBits(0.0),DAC0Update=True)
	
	jd = get_jd(t)
	V_rcvr = d.readRegister(0)
	V_therm1 = d.readRegister(2)
	V_rcvr_empty = d.readRegister(4)
	V_therm2 = d.readRegister(6)
	dBm = -5./0.12*(V_rcvr-0.639)
	mW = 10.**(dBm/10.)
	microW = mW *1000.
#	A = 0.00000238
#	B = 0.002836
#	T =  (mW-B)/A
#	print jd, V_rcvr, microW, V_therm1, V_rcvr_empty, V_therm2
#	f.write("%.7f %.5f %.5f %.5f %.5f %.5f"%(jd,V_rcvr,microW,V_therm1,V_rcvr_empty,V_therm2))
#'%s %s %s %s %s'%(str(jd),str(V_rcvr),str(V_therm1),str(V_rcvr_empty),str(V_therm2)))
#	f.write('\n')
#	f.flush()
	sleep(10)
	
	#print "%.7f %i %.1f %.1f %.5 %.5 %.5 %.5 %.5"%(jd,count,width*count,V2freq(width*count),V_rcvr,microW,V_therm1,V_rcvr_empty,V_therm2)
	print jd,count,width*count,V2freq(width*count),round(V_rcvr,2),round(microW,2),round(V_therm1,2),round(V_therm1,2),round(V_rcvr_empty,2),round(V_therm2,2)
	#info[count,count,count,count,count,count,count,count,count] = count,width*count,V2freq(width*count),V_rcvr,microW,V_therm1,V_rcvr_empty,V_therm2
	count += 1
