import machine

i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

print('I2C enheter', i2c.scan())