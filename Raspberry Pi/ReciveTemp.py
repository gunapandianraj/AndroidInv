import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import requests
import json
from datetime import datetime

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 25)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()

uploadInterval = time.time()

while True:
    while not radio.available(0):
        time.sleep(1/100)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("ReceivedMessage:{}".format(receivedMessage))

    print("Translating")

    string = ""

    for n in receivedMessage:
        if(n >=32 and n <= 126):
            string += chr(n)

    dt = "{:%B %d, %Y}".format(datetime.now())


    Light = string.find("L")
    Sound = string.find("S")
    Temp = string.find("C")
    
    LightValue = slice(Light+1,Sound)
    SoundValue = slice(Sound+1,Temp)
    TempValue  = slice(Temp+1,Light+Sound+Temp+1)

    print("Light Sensor Reading from channel 0x76 is of  {}".format(string))
    print("Light Sensor Reading from channel 0x76 is of  {}".format(string[LightValue]))
    print("Sound Sensor Reading from channel 0x76 is of  {}".format(string[SoundValue]))
    print("Temperature Sensor Reading from channel 0x76 is of  {}".format(string[TempValue]))
    
    try:
      if time.time() - uploadInterval > 10:
          dt = "{:%B %d, %Y}".format(datetime.now())
        
          padata = {"DeviceId":"76", "Temperature":string[TempValue], "Light":string[LightValue], "Sound":string[SoundValue]} 

          r = requests.post('http://10.5.50.89:5000/api/Temperature', json=padata)
          uploadInterval = time.time()
          print("Sending Post Request")
    except:
        uploadInterval = time.time()
        print("Upload failed")
