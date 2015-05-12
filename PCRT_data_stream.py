import ue9
from time import time, sleep
import numpy as np
import os

"""
Total intensity gets printed out to a file
Intensity is for a given frequency
"""


def get_jd(t): return t/86400. + 2440587.5

d = ue9.UE9()
os.system('rm TestData.txt')
f = open('TestData.txt', 'w')
#f.write('Time Volts MicroWatts Temperature\n')
f.write('Time Vrcvr Vtherm1 VrcvrEmpty Vtherm2\n')

def V2freq(V): return 79.25*V + 880.55
def freq2V(F): return (F-880.55)/79.25


def set_dac0(Volt,d):
	fb = d.feedback(DAC0Enabled=True,DAC0=d.voltageToDACBits(Volt),DAC0Update=True)
	return fb

def set_dac1(Volt,d):
	fb = d.feedback(DAC1Enabled=True,DAC1=d.voltageToDACBits(Volt),DAC1Update=True)
	return fb

c = 2
set_dac0(c,d) #<---- the "given frequency" in Volts: 2 V ~= 1 GHz
 
while True:
	"""
	set_dac0(c,d)
	if c>3: c = 0
	c+=1
	"""
	t = time()
	jd = get_jd(t)
	V_rcvr = d.readRegister(0)
	V_therm1 = d.readRegister(2)
	V_rcvr_empty = d.readRegister(4)
	V_therm2 = d.readRegister(6)
	dBm = -5./0.12*(V_rcvr-0.639)
	mW = 10.**(dBm/10.)
	microW = mW *1000.
	T =  (mW-0.002836)/0.00000238
	#f.write("%.7f %.5f %.5f %.5f"%(jd,V_rcvr,microW,T))
	f.write("%.7f %.5f %.5f %.5f %.5f"%(jd,V_rcvr,V_therm1,V_rcvr_empty,V_therm2))
	f.write('\n')
	f.flush()
	