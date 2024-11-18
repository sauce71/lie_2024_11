import network
import requests



# Eksempel på Nowcast API fra met.no
# https://api.met.no/weatherapi/nowcast/2.0/documentation

# Dette er samme data som YR bruker
# https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/1-30795/Norge/Telemark/Skien/Skien

# Tilleget JSON Fromatter for Google Chrome gjør JSON mer leselig
# https://chromewebstore.google.com/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa


# Kobler til wifi
sta_if = network.WLAN(network.STA_IF) # Static interface
sta_if.active(True) # Aktiverer netwerk

sta_if.connect('kurs', 'kurs2024') # Kobler til wifi

while not sta_if.isconnected(): # Venter på at tilkoblingen er klar
    time.sleep(1)
print('\nNettverks konfigurasjon', sta_if.ifconfig()) # Printer nettverkskonfigurasjon



# Koordinater for ønsket lokasjon (En kan finne koordinater ved å høyreklikke i Google Maps)
latitude = 59.2102183365655
longitude = 9.603447767110834

headers = {'User-Agent': 'Bydelshuset kurs tom.oyvnd.hogstad@gmail.com'} # met.no krever at en identifiserer seg
# Bruker en "f-string" eller "format string". Det er en enkel måte å få variabler til å bli en del av en tekst
url = f'https://api.met.no/weatherapi/nowcast/2.0/complete?lat={latitude}&lon={longitude}'
print('Lenken vi ender opp med å hente data fra')
print(url)
# requests modulen brukes til å hente og sende data på internett med HTTP protokollen (Akkurat som en nettleser gjør det)
r = requests.get(url, headers=headers)

data = r.json() # Data motatt som JSON (Javascript Object Notation) gjøres om til en Python "Dict" (Dictionary/Ordbok)
#print(data)

# Plukker fra hverandre mottate data i flere steg for å gjøre det noe mer lesbart
latest_timeseries = data['properties']['timeseries'][0] #[0] er første element i listen timeseries
#print(latest_timeseries)
instant_details = latest_timeseries['data']['instant']['details'] # Det er her de data vi ønsker er gjemt
#print(instant_details)

print('\nAlle nå verdier') #\n i en streng lager et linjeskift

# Printer nøkkel , data
for k in instant_details:
    print(k, instant_details[k])

# Printer bare en av verdiene fra instant_details
print('\nTemperaturen ute:', instant_details['air_temperature'])


