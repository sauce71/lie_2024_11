import machine
import network
import time
import socket
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


# Globale variabler for data fra sensorer
tvoc = 0
humidity = 0
pressure = 0
temperature_aht20 = 0
temperature_bmp280 = 0

def read_sensors():
    # Dette er en egen funksjon for å gjøre koden noe mer oversiktlig
    global tvoc
    global humidity
    global pressure
    global temperature_aht20
    global temperature_bmp280

    tvoc = ags10_sensor.total_volatile_organic_compounds_ppb
    if aht20_sensor.is_ready:
        temperature_aht20 = aht20_sensor.temperature
        humidity = aht20_sensor.humidity
    bmp280_data = bmp280_sensor.read_compensated_data() # Returnerer en tuple med de forskjellige verdiene
    temperature_bmp280 = bmp280_data[0]
    pressure = bmp280_data[1]

def webpage():
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Raspberry Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
        <style>
        td:nth-child(2) {{
            float:right;
        }}
        </style>
            <h1>Raspberry Pi Pico Web Server</h1>
        <table>
        <tr><td>TVOC</td><td>{tvoc}</td><td>ppb</td></tr>
        <tr><td>Humidity</td><td>{humidity:.2f}</td><td>%</td></tr>
        <tr><td>Pressure</td><td>{pressure:.2f}</td><td>hPA</td></tr>
        <tr><td>Temperature (AHT20)</td><td>{temperature_aht20:.2f}</td><td>C</td></tr>
        <tr><td>Temperature (BMP280)</td><td>{temperature_bmp280:.2f}</td><td>C</td></tr>
        </table>            
        </body>
        </html>
        """
    return str(html)

# Set up socket and start listening
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
print(addr)
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        request = conn.recv(1024)

        read_sensors()

        print('TVOC', tvoc, 'ppb')
        print('Humidity', humidity, '%')
        print('Pressure', pressure, 'hPA')
        print('Temperature (AHT20)', temperature_aht20, 'C')
        print('Temperature (BMP280)', temperature_bmp280, 'C')

        response = webpage()

        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')


           










    







