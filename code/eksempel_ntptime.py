import time
import network # nettverksfunksjoner
import ntptime # https://mpython.readthedocs.io/en/v2.2.1/library/micropython/ntptime.html


sta_if = network.WLAN(network.STA_IF) # Static interface
sta_if.active(True) # Aktiverer netwerk


# Søker opp tilgjengelige nettverk og skriver dem ut. Kan være kjet for å problemløse.
# Det er bare 2G wifi på RPI Pico kortet
networks = sta_if.scan() # Søker opp tilgjengelige netverk
#print(networks)
for n in networks:
    # Skriver ut nettverk som er tilgjengelig
    print('SSID:', str(n[0]), 'Kanal:', n[2], 'RSSI:', n[3])


sta_if.connect('kurs', 'kurs2024') # Kobler til wifi

while not sta_if.isconnected(): # Venter på at tilkoblingen er klar
    time.sleep(1)
print('\nNettverks konfigurasjon', sta_if.ifconfig()) # Printer nettverkskonfigurasjon

ntptime.settime() # Henter dato tid fra en ntp server

# Tid kommer ut i en tuple
lt = time.localtime()
print(lt)

# Setter sammen delene fra lt til en lesbar dato og tid
print(f"Dato / tid: {lt[2]}.{lt[1]:02}.{lt[0]} {lt[3]}:{lt[4]:02}:{lt[5]:02}")





