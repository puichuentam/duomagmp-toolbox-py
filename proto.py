from duomag import DUOMAG
import time

coilA = DUOMAG("COM4")
coilB = DUOMAG("COM3")

coilA.set_intensity(50)
coilB.set_intensity(50)

time.sleep(3)

coilA.duopulse()
time.sleep(100/1000)
coilB.duopulse()

time.sleep(5)

coilB.duopulse()
time.sleep(100/1000)
coilA.duopulse()

coilA.set_intensity()
coilB.set_intensity()

coilA.close()
coilB.close()
