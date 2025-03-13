import machine
import time

button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    print(button.value())
    time.sleep(0.5)
    