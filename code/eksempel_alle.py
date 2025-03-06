import machine
import time
from ags10 import AGS10
from aht import AHT2x
from bme280_float import BME280

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

print('TVOC:', tvoc, 'ppb')
print('Humidity', humidity, '%')
print('Pressure', pressure, 'hPA')
print('Temperature (AHT20)', temperature_aht20, 'C')
print('Temperature (BMP280)', temperature_bmp280, 'C')










    






