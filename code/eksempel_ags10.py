import machine
import time
from ags10 import AGS10

# Setter opp i2c med en frekvens på 10khz
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=10000)


sensor = AGS10(i2c) # Instans av sensoren


while True:
    tvoc = sensor.total_volatile_organic_compounds_ppb # Leser tvoc
    #resistance = sensor.resistance_kohm # Leser motstand
    print('TVOC:', tvoc) # Skriver ut den avleste verdien
    time.sleep(10) # Venter i x sekunder
    