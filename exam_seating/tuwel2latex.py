source = open('upload2tuwel.csv','r')
text = source.read()
source.close()

text_lines = text.split('\n')
del text_lines[0]
del text_lines[-1]

name_sort = []
#aufräumen
for i in range(len(text_lines)):
    if text_lines[i] == ['']:
            del text_lines[i]

i =1

file = open('plaetze.csv', 'w')
print(len(text_lines), "lines")
clean_lines = []
for teilnehmer in text_lines:

    line = teilnehmer.split(',')

    print(i, line[1])
    gesamt = line[1]
    gesamt_clean = gesamt.strip('\"')
    name = gesamt_clean.split(' ')
    nachname = name[0]
    del name[0]
    vorname  = ' '.join(name)
    matrikel = line[2]
    hs = line[8]

    clean_lines +=[[(nachname,vorname), str(nachname+';'+vorname+';'+matrikel+';'+hs) ]]
    i += 1
print(clean_lines[0],'\n',clean_lines[1])
sorted_lines = sorted(clean_lines, key = lambda x:x[0])
print(sorted_lines[0][1],'\n',sorted_lines[1][1])


i = 1
for line in sorted_lines:
    file.write(line[1])
    print(line[1])
    if i%2 == 1:
        file.write(';')
        print('ungerade', i)
    else:
        file.write('\n')
        print('gerade', i)

    i += 1

file.close()
