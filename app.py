from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import csv
import plotly.plotly as py
import plotly.graph_objs as go

# dati contenti nome_citta, data, umidita, latitudine, longitudine
dati = []
# servizio per avere le coordinate
geolocator = Nominatim()

max_dati = 200
n_dati = 0
# leggiamo il file csv
with open('dati_umidita.csv', 'rb') as csvfile:
    umiditareader = csv.reader(csvfile, delimiter=';', quotechar='|')

    # citta e coordinate che di volta in volta analizziamo
    citta_precedente = ''
    coordinate_precedenti = [0, 0]

    # per ogni riga del file
    for row in umiditareader:
        n_dati += 1
        if n_dati > max_dati:
            break

        # prendiamo le coordinate solo se la citta non l'abbiamo ancora analizzata
        if row[0] != citta_precedente:
            # la citta e' il primo campo
            citta_precedente = row[0]
            # coordinate della citta
            location = geolocator.geocode(citta_precedente)
            coordinate_precedenti = [location.latitude, location.longitude]
            # le mostriamo a schermo
            print citta_precedente
            print coordinate_precedenti
        # aggiungiamo i dati
        dati.extend([[row[0], row[1], float(row[2].replace(",", ".")), location.latitude, location.longitude]])

# prendiamo in input le coordinate
latitudine = longitudine = 1000

# latitudine tra -90 e 90
while latitudine < -90 or latitudine > 90:
    latitudine = float(raw_input("Inserisci la latitudine: "))

# longitudine tra -90 e 90
while longitudine < -90 or longitudine > 90:
    longitudine = float(raw_input("Inserisci la longitudine: "))

# massima distanza
min_distanza = 999999999
citta_min_distanza = ''

# per ogni dato
for dato in dati:
    # citta che di volta in volta analizziamo
    citta_precedente = ''
    if dato[0] != citta_precedente:
        citta_precedente = dato[0]
        # calcoliamo la distanza
        distanza = vincenty((latitudine, longitudine), (dato[3], dato[4])).meters / 1000
        if distanza < min_distanza:
            min_distanza = distanza
            citta_min_distanza = citta_precedente


# mostriamo a schermo i dati della citta piu vicina
print 'Dati per la citta di ' + citta_min_distanza

date = []
umidita = []
for dato in dati:
    if dato[0] == citta_min_distanza:
        print 'In data ' + dato[1] + ' umidita pari a ' + str(dato[2]) + ' %'
        date.append(dato[1])
        umidita.append(dato[2])


data = [go.Scatter(
    x = date,
    y = umidita,
    mode = 'lines',
    name = 'lines'
)]
py.plot(data, filename = 'basic-line')