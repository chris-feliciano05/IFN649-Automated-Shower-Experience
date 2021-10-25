import paho.mqtt.client as mqtt
import serial
import time
import string
ser = serial.Serial("/dev/rfcomm2", 9600)
ser.write(str.encode('Start\r\n'))

def on_connect(client, userdata, flags, rc): # func for making connection
 print("Connected to MQTT")
 print("Connection returned result: " + str(rc) )
 client.subscribe("temp") 
def on_message(client, userdata, msg): # Func for Sending msg
 print(msg.topic+" "+str(msg.payload))
 if (float(msg.payload) > 41):
         print("High")
         ser.write(b"High\n")
 if (float(msg.payload) > 37) and (float(msg.payload) < 41):
         print("Medium")
         ser.write(b"Medium\n")
 if (float(msg.payload) < 37): 
         print("Low")
         ser.write(b"Low\n")
 if (float(msg.payload) == 0 ): 
         print("No Value")
         ser.write(b"No Value\n")
         

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()


