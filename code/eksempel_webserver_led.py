import machine
import network
import time
import socket

# Kobler til wifi
sta_if = network.WLAN(network.STA_IF) # Static interface
sta_if.active(True) # Aktiverer netwerk

sta_if.connect('kurs', 'kurs2024') # Kobler til wifi

while not sta_if.isconnected(): # Venter på at tilkoblingen er klar
    time.sleep(1)
print('\nNettverks konfigurasjon', sta_if.ifconfig()) # Printer nettverkskonfigurasjon

led = machine.Pin('LED')
led.on()

def webpage(led_value):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Raspberry Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Raspberry Pi Pico Web Server</h1>
            <h2>LED status: {led_value}</h2>
          <form action="./lighton">
                <input type="submit" value="Light on" />
            </form>
            <br>
            <form action="./lightoff">
                <input type="submit" value="Light off" />
            </form>    
        </body>
        </html>
        """
    return str(html)

# Set up socket and start listening
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        request = conn.recv(1024)
        #print(request)
        request_lines = request.split()
        print(request_lines)
        
        if len(request_lines) > 1 and 'lighton' in request_lines[1]:
            led.on()
        if len(request_lines) > 1 and 'lightoff' in request_lines[1]:
            led.off()
        
        response = webpage(led.value())

        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')


           










    







