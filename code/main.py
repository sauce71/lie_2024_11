import machine
import time
from ags10 import AGS10


led = machine.Pin('LED', machine.Pin.OUT) # Setter pinne LED som en output pi

# Setter opp i2c med en frekvens på 10khz
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=10000)


sensor = AGS10(i2c) # Instans av sensoren


while True:
    led.toggle() # Slår led av og på
    tvoc = sensor.total_volatile_organic_compounds_ppb # Leser tvoc
    print('TVOC:', tvoc) # Skriver ut de avleste verdiene
    time.sleep(10) # Venter i x sekunder
    
    
