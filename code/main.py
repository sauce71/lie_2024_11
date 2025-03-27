import machine
import gc
import time
import network
import requests
from ags10 import AGS10
from aht import AHT2x
from bme280_float import BME280
from machine import WDT

led = machine.Pin('LED', machine.Pin.OUT)


HTTP_HEADERS = {'Content-Type': 'application/json'}
THINGSPEAK_WRITE_API_KEY = 'G89RA43MZGMEQFBA' # HER MÅ DERE BRUKE EGEN!!!
THINGSPEAK_WRITE_URL = f'http://api.thingspeak.com/update?api_key={THINGSPEAK_WRITE_API_KEY}'


# Kobler til nett
SSID = 'kurs'
PASSWORD = 'kurs2024'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(False) # Nettverket overlever en omstart
sta_if.active(True)
sta_if.connect(SSID, PASSWORD) # Kobler til wifi

wdt = WDT(timeout=8000)  # enable it with a timeout of 8s

ret = 0
print('Kobler til nett ', end='')
while not sta_if.isconnected():
    print('.', end='')
    time.sleep(1)
    ret += 1
    wdt.feed()
    led.toggle() # Blinker når den kobler til nett
    if ret > 30: # Prøver i 60 sekunder. 
        machine.reset() # Starter på nytt om ikke det er nett etter 30 sekunder
led.off()
print('\nNettverks konfigurasjon', sta_if.ifconfig()) # Printer nettverkskonfigurasjon

# Setter opp i2c med en frekvens på 10khz
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=10000)

ags10_sensor = AGS10(i2c) # Instans av sensoren

aht20_sensor = AHT2x(i2c, crc=False) # Instans av sensoren

bmp280_sensor = BME280(i2c=i2c, address=0x77) # Instans av sensoren - kortet bruker adresse 0x77/119 - det er ikke standard




while True:
    led.on()
    tvoc = ags10_sensor.total_volatile_organic_compounds_ppb

    if aht20_sensor.is_ready:
        temperature_aht20 = aht20_sensor.temperature
        humidity = aht20_sensor.humidity
        
    bmp280_data = bmp280_sensor.read_compensated_data() # Returnerer en tuple med de forskjellige verdiene
    temperature_bmp280 = bmp280_data[0]
    pressure = bmp280_data[1]

    print('TVOC:', tvoc, 'ppb')
    print('Humidity', humidity, '%')
    print('Pressure', pressure, 'hPA')
    print('Temperature (AHT20)', temperature_aht20, 'C')
    print('Temperature (BMP280)', temperature_bmp280, 'C')

    payload = {
            'field1' : tvoc,
            'field2' : humidity,
            'field3' : pressure,
            'field4' : temperature_aht20,
            'field5' : temperature_bmp280,
            }
    print(payload)
    try:
        r = requests.post(THINGSPEAK_WRITE_URL, json = payload, headers = HTTP_HEADERS)
    except Exception as e: # Here it catches any error.
        print(e)
        if isinstance(e, OSError) and r: # If the error is an OSError the socket has to be closed.
            r.close()
        machine.reset() # Starter på nytt om en får en Exception
            
    gc.collect()
    print('Status code:', r.status_code, 'Response:', r.text)
    led.off()
    for i in range(60):
        if not (i % 10):
            led.on() # Blinker hvert 10 sekund
            time.sleep(0.1)
            led.off()
        time.sleep(1)
        wdt.feed()
    r.close() # Lukker koblingen
