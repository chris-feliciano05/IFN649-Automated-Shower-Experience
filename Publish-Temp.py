import serial
import time
import string
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'INQjA3OyuCjPO04QT9q2'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'Water Temperature': 0}

next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

# reading and writing data from and to arduino serially.
# rfcomm0 -> this could be different
ser1 = serial.Serial("/dev/rfcomm0", 9600)
ser1.write(str.encode('Start\r\n'))
while True:
 if ser1.in_waiting > 0:
     rawserial = ser1.readline()
     cookedserial = rawserial.decode('utf-8').strip('\r\n')
     #print(cookedserial)
     #splitting
     split1 = cookedserial.split(" ")
     
     tempValue = split1[3].split(" ")[0]
     print(tempValue)
     
     publish.single("temp",tempValue, hostname="localhost")
     print("Done")
     ser1.write(b"temp\n")
     sensor_data['tempValue'] = tempValue
     # Sending humidity and temperature data to ThingsBoard
     client. publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

     count = 0
     next_reading += INTERVAL
     sleep_time = next_reading-time.time()
     if sleep_time > 0:
            time.sleep(sleep_time)
     
       
client.loop_stop()
client.disconnect()
