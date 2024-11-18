import machine
import time
from bme280_float import BME280

# Setter opp i2c med en frekvens på 10khz
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

sensor = BME280(i2c=i2c, address=0x77) # Instans av sensoren - kortet bruker adresse 0x77/119 - det er ikke standard

while True:
    values = sensor.values # Henter alle verdiene BMP280 har ikke luftfuktighet, derfor er denne verdien 0
    altitude = sensor.altitude
    print(altitude, values)
    time.sleep(2)
