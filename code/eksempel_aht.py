import machine
import time
from aht import AHT2x

# Setter opp i2c med en frekvens på 10khz
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=10000)

sensor = AHT2x(i2c, crc=False) # Instans av sensoren

while True:
    if sensor.is_ready:
        temperature = sensor.temperature
        humidity = sensor.humidity

    print('Temperatur:', temperature, 'Luftfuktighet:', humidity)
    time.sleep(2)

