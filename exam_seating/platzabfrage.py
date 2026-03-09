from os import listdir
from pathlib import Path    
import glob
import pandas as pd
import locale
import networkx as nx

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

    def __init__(self, name, capacity, segment_graph=None):
        self.name = name
        self.capacity = capacity
        self.segment_graph = segment_graph
class LectureHallSegment:

    def __init__(self, part_of, seating_graph):
        #TODO: define LectureHall as Metagraph of LectureHallSegments
        assert isinstance(part_of, LectureHall)
        assert isinstance(seating_graph, nx.Graph)
        self.part_of = part_of 
        self.seating_graph = seating_graph

    def get_last_row_index(self):
        pass
    
    def get_leftmost_seat_id(self, row_index):
        pass
    
    def get_rightmost_seat_id(self, row_index):
        pass
    
    # edge = (id, row, label)
    # as general rule in same row, seat_id is increasing from left to right

    def _get_rightneighbor_seat_id(self, row_index, n=1):
        pass

    def _get_leftneighbor_seat_id(self, row_index, n=1):
        pass

    def _add_row_after(self, row_index=None, num_seats=None, offset=0, direction ='right'):
        #TODO: - if num_seats is None, add same number of seats as in the previous row
        #      - allow only half integer offset and check for plausibility (e.g. no overlap with previous row)
        #      - if row_index is None, add row at the end
        #      - if direction is 'left', add seats to the left of the last seat of the previous row, otherwise to the right
        #      - direction is probably not needed if we allow negative offset, but it might be more intuitive to specify direction and offset separately     
        #      - assume elevated rows, so that line of sight to seat in front is not blocked by the person sitting in front
        #      - add support for same-level rows (e.g. for lecture halls with flat seating)

        if direction == 'right':
            last_seat_id = self.get_rightmost_seat_id(row_index)
            last_seat_label = self.seating_graph.nodes[last_seat_id]['seat']
        
        #add seats as nodes
        for seat in range(num_seats):
            self.seating_graph.add_node(last_seat_id+seat+1, row=row_index+1, seat=last_seat_label+seat+1)

        #add edges between seats in the same row
        for seat_id in range(last_seat_id+1, last_seat_id+num_seats):
            self.seating_graph.add_edge(seat_id, seat_id+1, same_row=True)
        
        #assume for now only elevated configuration
        #add edges to seats in the previous row 
        #integer offset means that the new row starts at the same position as the last seat of the previous row
        if offset == int(offset): 
            leftmost_seat_in_front_id = self._get_leftneighbor_seat_id(row_index)
            if offset < 0:
                for i in range(abs(offset), num_seats):
                    self.seating_graph.add_edge(leftmost_seat_in_front_id+i, last_seat_id+1+i, same_row=False)
            else:
                for i in range(num_seats-offset):
                    self.seating_graph.add_edge(leftmost_seat_in_front_id+offset+i, last_seat_id+1+i, same_row=False)

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