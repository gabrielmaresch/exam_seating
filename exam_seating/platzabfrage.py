from os import listdir
from pathlib import Path    
import glob
import pandas as pd
import locale
import networkx as nx
import json

###### Sortieren von Strings mit Umlauten Ä=ae, Ö=oe, Ü=ue, ß=ss
locale.setlocale(locale.LC_COLLATE, "de_AT.UTF-8")

#Liste der Anmeldungen
#Bewertungstabelle
#Latex-Datei
#HS-Liste


def _import_csv(file, delimiter=','):
    df = pd.read_csv(file, sep=delimiter)
    return df

def _sort_per_name(df, german_locale=True):
    #TODO: check for diacritics in column names and sort accordingly
    if german_locale:
        df.sort_values(by='Vollständiger Name', inplace=True, key=lambda s: s.map(locale.strxfrm))
    else:    
        df.sort_values(by='Vollständiger Name', inplace=True)
    return df


class LectureHall: 
    class Segment:
            def __init__(self, name=None, rows=None, unuseable_seats=None, line_of_sight_graph=None):
                #TODO: define LectureHall as Metagraph of LectureHallSegments
                if name is None:
                    name = ""
                self.name = name
                if rows is None:
                    rows = {}
                if unuseable_seats is None:
                    unuseable_seats = []
                
                self.rows = rows
                self.unusable_seats = unuseable_seats
                self.line_of_sight_graph = line_of_sight_graph

            def _get_last_row_number(self):
                if self.rows:
                    return max(self.rows.keys())
                else:
                    return 0
                
            def _get_last_seat_label(self):
                if self.rows:
                    number_of_last_row = self._get_last_row_number()
                    return self.rows[number_of_last_row]["seats"][-1]
                else:
                    return str(0)

            def _add_row_after(self, row_number=None, num_seats=None, offset=0, direction ='right', row_label =None,  seat_labels = None, row_is_elevated = False):
                if seat_labels is None:
                    last_seat_lable = self._get_last_seat_label()
                    if not last_seat_lable.isdigit():
                        start = 1
                    else:
                        start = int(last_seat_lable) + 1
                    seat_labels = [str(start+i) for i in range(num_seats)]
                
                if row_number is None or row_number >= self._get_last_row_number():   #append at end
                    row_number = self._get_last_row_number() + 1
                else:
                    for i in range(self._get_last_row_number(), row_number-1, -1):
                        self.rows[i+1] = self.rows.pop(i) 
                self.rows[row_number] = {}                      
                
                if row_label is None:
                    row_label = str(row_number)
                self.rows[row_number]["row_label"] = row_label
                    

                self.rows[row_number]["seats"] = seat_labels #seats from left to right
                
                self.rows[row_number]["offset"] = offset
                self.rows[row_number]["elevated"] = row_is_elevated


                #TODO: - if num_seats is None, add same number of seats as in the previous row
                #      - allow only half integer offset and check for plausibility (e.g. no overlap with previous row)
                #      - if row_index is None, add row at the end
                #      - if direction is 'left', add seats to the left of the last seat of the previous row, otherwise to the right
                #      - direction is probably not needed if we allow negative offset, but it might be more intuitive to specify direction and offset separately     
                #      - assume elevated rows, so that line of sight to seat in front is not blocked by the person sitting in front
                #      - add support for same-level rows (e.g. for lecture halls with flat seating)


    def __init__(self, name, segments, segment_graph=None, capacity=None):
        self.name = name
        self.capacity = capacity
        for segment in segments:
            assert isinstance(segment, LectureHall.Segment), "not of data type LectureHallSegment"
        self.segments = segments
        self.segment_graph = segment_graph

    def compute_capacity(self):
        self.capacity = 0
        for segment in self.segments:
            for i in segment.rows.keys():
                self.capacity += len(segment.rows[i]["seats"])

    def save_hall_as_json(self):
        hall_data = {"name": self.name, "segments": []}
        
        for segment in self.segments:
            seg_dict = {"name": segment.name, "rows": segment.rows, "unuseable_seats": segment.unusable_seats}
            hall_data["segments"].append(seg_dict)
        
        filepath = Path(__file__).parent.parent / 'data' / f"{self.name.replace(" ", "_")}.json"

        with open(filepath, "w") as file:
            json.dump(hall_data, file, indent=2)
            
        

 
        
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