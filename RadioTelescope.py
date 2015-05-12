import ue9
from time import time, sleep

def get_jd(t): return t/86400. + 2440587.5

#ipAddress = "192.168.1.105"

#print "Opening device at %s" % ipAddress
d = ue9.UE9()#ethernet=True,ipAddress=ipAddress)

#print "Device specs..."
print "%s" % d.commConfig()

f=open("RadioTelescope.txt","w")
f.write("Time    JD     rawV     muW \n")#K     degC \n")
t0 = time()
while(True):
#  print "%.4f %.3f "%(d.readRegister(0),d.readRegister(2))
  t = time()-t0
  jd = get_jd(t)
  tempSensV = d.readRegister(8)
  powerV = d.readRegister(0)
# Convert the temperature
  temperature = 500.*tempSensV-280.
# Convert the power to actual muW
# First, turn voltage into dBm
  dBm = -40.67*powerV + 39.71
  muW = 10.**(dBm/10.)*1000.
# Convert to brightness temperature
  K = muW*1e-3/1.38e-23/1e9/5.1e6
  f.write("%.7f %.7f %.5f %.3f "%(t,jd,powerV,muW))#,temperature))
  f.write("\n")	
  f.flush()
  sleep(0.1)



