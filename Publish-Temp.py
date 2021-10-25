import serial
import time
import string
import paho.mqtt.publish as publish
# reading and writing data from and to arduino serially.
# rfcomm0 -> this could be different
ser = serial.Serial("/dev/rfcomm0", 9600)
ser.write(str.encode('Start\r\n'))
while True:
 if ser.in_waiting > 0:
     rawserial = ser.readline()
     cookedserial = rawserial.decode('utf-8').strip('\r\n')
     #print(cookedserial)
     #splitting
     split1 = cookedserial.split(" ")
     
     tempValue = split1[3].split(" ")[0]
     print(tempValue)
     
     publish.single("temp",tempValue, hostname="localhost")
     print("Done")
     ser.write(b"temp\n")
