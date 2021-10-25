import RPi.GPIO as GPIO
import time, sys
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'K360g583CrNIKC1IGtp3'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'flow': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

f = open('FlowMeterOutput.txt','a')
GPIO.setmode(GPIO.BOARD)
inpt = 13
GPIO.setup(inpt,GPIO.IN)
min = 0
constant = 0.0031
newtime = 0.0
rpt_int = 10

global ratecount, totalcount
ratecount= 0
totalcount = 0

def PulseCount(inpt_pin):
    global ratecount,totalcount
    ratecount += 1
    totalcount += 1
   
GPIO.add_event_detect(inpt,GPIO.FALLING,callback=PulseCount,bouncetime=10)

#MAIN
print('WATER FLOW',
      str(time.asctime(time.localtime(time.time()))))
rpt_int = int(input('Input desired report interval in seconds: '))
print('reports every ', rpt_int, ' seconds')
print('Control C to EXIT!')
f.write('/nWater Flow - Approximate - Reports every ' +
        str(rpt_int)+ ' seconds '+
        str(time.asctime(time.localtime(time.time()))))

while True:
    newtime = time.time() + rpt_int
    ratecount = 0
    while time.time() <= newtime:
        try:
            None
            #print(GPIO.input(inpt), end='')
        except KeyboardInterrupt:
            print('Exiting Nicely!')
            GPIO.cleanup()
            f.close()
            print('END')
            sys.exit()
    min += 1
    LperM = round(((ratecount*constant)/(rpt_int/60)),2)
    TotLit = round(totalcount * constant, 1)
    print('\nLiters per Min', LperM, '(',rpt_int,'second sample)')
    print('\nTotal Liters', TotLit)
    print('Time (min & clock) ', min, '\t', time.asctime(time.localtime(time.time())),'\n')
    sensor_data['LperM'] = LperM
    sensor_data['TotLit'] = TotLit
    f.write('\nLiter per min ' + str(LperM))
    f.write('\nTotal Liters '+ str(TotLit))
    f.write('Time (min & clock) ' + str(min) + '\t' +
            str(time.asctime(time.localtime(time.time()))))
 # Sending humidity and temperature data to ThingsBoard
    client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    f.flush()
    next_reading += INTERVAL
    sleep_time = next_reading-time.time()
    if sleep_time > 0:
        time.sleep(sleep_time)
   
GPIO.cleanup()
f.close()
print('Done')

client.loop_stop()
client.disconnect()
   


