from os import listdir
from pathlib import Path    
import glob
import pandas as pd
import locale

###### Sortieren von Strings mit Umlauten
locale.setlocale(locale.LC_COLLATE, "de_AT.UTF-8")

#Liste der Anmeldungen
#Bewertungstabelle
#Latex-Datei
#HS-Liste


def _import_csv(file, delimiter=','):
    df = pd.read_csv(file, sep=delimiter)
    return df

def _sort_per_name(df, german_locale=True):
    if german_locale:
        df = df.sort_values(by='Vollständiger Name', inplace=True, key=lambda s: s.map(locale.strxfrm))
    else:    
        df = df.sort_values(by='Vollständiger Name')
    return df

'''
print('start')
# csv-trennzeichen
trennzeichen = ','
# Einlesen der Anmeldungen
arr = [f for f in glob.glob("*.csv")]
for file in arr:
    print(file)
file = ''


source = open('anmeldungen.csv','r')
text = source.read()
source.close()

# Extrahieren von Name und Matr.Nr.
text_lines = text.split('\n')
platz = []
matrikel = []
for line in text_lines:
    platz += [line.split(',')]
    if len(line.split(',')) > 1:
        matrikel += [line.split(',')[2]]
print(len(text_lines)-1, 'Anmeldungen ',end='')


# Einlesen der Bewertungstabelle zur Abfrage
source = open('original_tabelle.csv','r')
text = source.read()
source.close()

text_line= text.split('\n')

abfrage = []

for line in text_line:
    
    for nr in matrikel:
        if nr in line.split(trennzeichen) or '0'+nr in line.split(trennzeichen):
            abfrage += [line.split(trennzeichen)]
abfrage.sort(key=lambda x: x[1])
# print(len(abfrage))
if (len(abfrage)== len(text_lines)-1):
    print(u'✓\n')

hsliste = ['hs8_33percent.csv', 'hs17_33percent.csv', 'ae-u1.csv']

hs_liste = listdir('hs')

file = open('upload2tuwel.csv', 'w')
n=0

#Kopfzeile schreiben
file.write(text_line[0]+'\n')
for hoersaal in hsliste:
    hs = open('hs/'+hoersaal, 'r')
    hs = hs.read()
    nr = hs.split('\n')
    kap = len(nr)-1



    # print(nr)
    print(len(abfrage), 'noch nicht vergeben:', nr[0], 'Kapazität', kap)
    print('Wieviele davon verwenden? (blank=alle)')
    kap_change = input()
    if kap_change != '':
        kap_change = int(kap_change)
        assert kap_change >= 0 and kap_change <= kap
        kap = kap_change



    for j in range(min(kap, len(abfrage))):
        
        for i in range(8):
            file.write(abfrage[j][i]+',')
        #file.write(str(n)+'\n')
        file.write('"'+nr[0]+' - Sitzplatz '+nr[j+1]+'"'+'\n')
        #print('Vergebe Sitzplatz '+nr[j+1]+' im ' + nr[0])
        n += 1

    for j in range(kap):
        if len(abfrage)>0:
            del abfrage[0]
         
file.close()
print(n,' Sitzplätze vergeben')
'''

if __name__ == '__main__':
    file = input('Name of csv file [test_table.csv]: ')
    if file:
        df = _import_csv(Path(__file__).parent / file)
    else:
        df = _import_csv(Path(__file__).parent.parent / 'tests' / 'test_table.csv')
    _sort_per_name(df)
    print(df.head())