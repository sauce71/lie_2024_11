import machine
import network
import time
import json
import requests
from ags10 import AGS10
from aht import AHT2x
from bme280_float import BME280

# Kobler til wifi
sta_if = network.WLAN(network.STA_IF) # Static interface
sta_if.active(True) # Aktiverer netwerk

sta_if.connect('kurs', 'kurs2024') # Kobler til wifi

while not sta_if.isconnected(): # Venter på at tilkoblingen er klar
    time.sleep(1)
print('\nNettverks konfigurasjon', sta_if.ifconfig()) # Printer nettverkskonfigurasjon


# Setter opp i2c med en frekvens på 10khz
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=10000)


ags10_sensor = AGS10(i2c) # Instans av sensoren

aht20_sensor = AHT2x(i2c, crc=False) # Instans av sensoren

bmp280_sensor = BME280(i2c=i2c, address=0x77) # Instans av sensoren - kortet bruker adresse 0x77/119 - det er ikke standard

tvoc = ags10_sensor.total_volatile_organic_compounds_ppb

if aht20_sensor.is_ready:
    temperature_aht20 = aht20_sensor.temperature
    humidity = aht20_sensor.humidity
    
bmp280_data = bmp280_sensor.read_compensated_data() # Returnerer en tuple med de forskjellige verdiene
temperature_bmp280 = bmp280_data[0]
pressure = bmp280_data[1]

print('TVOC', tvoc, 'ppb')
print('Humidity', humidity, '%')
print('Pressure', pressure, 'hPA')
print('Temperature (AHT20)', temperature_aht20, 'C')
print('Temperature (BMP280)', temperature_bmp280, 'C')

IFTTT_KEY = 'mvte1BsLxR5g0AvW_QxumINgBvboGo_-CpF6C_gIdq1'
IFTTT_EVENT = 'data_to_email'
IFTTT_URL = f'https://maker.ifttt.com/trigger/{IFTTT_EVENT}/with/key/{IFTTT_KEY}'

row = []
row.append(f'TVOC: {tvoc}')
row.append(f'Humidity: {humidity}')
row.append(f'Pressure: {pressure}')
row.append(f'Temperature (AHT20): {temperature_aht20}')
row.append(f'Temperature (BMP280): {temperature_bmp280}')

value2 = '<br>' + '<br>'.join(row) # Slår sammen elementene i listen med HTML linjeskift

ifttt_data = dict(value1='tom.oyvind.hogstad@vtfk.no', value2=value2, value3=0)

json_data = json.dumps(ifttt_data)

r = requests.post(IFTTT_URL, data=json_data, headers={'Content-Type': 'application/json'})

print(json_data)
print(r.status_code)
print(r.text)
