# BWINF: Nr. 40
# Runde: 1
# Aufgabe: 1
# Autor: Ron Jost
# Team: Opensourcehacker (00155)


# Import von benötigten Bibliotheken
import sys
import copy

# Dateeineinlese:
dateiname = sys.argv[1]
datei = open(dateiname, 'r')
lines = datei.readlines()
lines_bearbeitet = []
for line in lines:
    lines_bearbeitet.append(line.replace('\n', ''))

# Verarbeitung
start_stop = lines_bearbeitet[0]
anz_quer = lines_bearbeitet[1]
quer_fahrezuge = lines_bearbeitet[2:]
Alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']

stop = Alphabet.index(start_stop[2]) + 1
normal_park_liste = list(range(stop))
normal_park_liste_buchstaben = []
for element in normal_park_liste:
    normal_park_liste_buchstaben.append(Alphabet[element])
querpark_liste = []
for i in normal_park_liste:
    querpark_liste.append(0)
quer_fahrezuge = lines_bearbeitet[2:]
for auto in quer_fahrezuge:
    pos = auto[2:]
    querpark_liste[int(pos)] = auto[0]
    querpark_liste[int(pos) + 1] = auto[0]



# Das blockierende Auto nach rechts wegbewegen
def testing_nach_rechts(array2, position):
    try:
        array_on = copy.deepcopy(array2)
        # Check, ob das querparkende Auto 2x mal nach rechts bewegt werden muss, um die position frei zu machen.
        if array_on[position + 1] == array_on[position]:
            need_2 = False
        else:
            need_2 = True

        # Falls zwei Bewegungen nach rechts gesucht werden.
        if need_2:
            new_pos = position + 1
            verschiebe_ar = []

            # Es werden zwei freie Parkplätze rechts von der Position gesucht
            while new_pos <= len(array_on):
                if array_on[new_pos] == 0:
                    if len(verschiebe_ar) == 1:
                        verschiebe_ar.append((array_on[new_pos - 1], new_pos))
                        break
                    else:
                        verschiebe_ar.append((array_on[new_pos - 1], new_pos))
                        new_pos = new_pos + 1
                else:
                    new_pos = new_pos + 1
            # Falls es keine 2 gibt, wird abgebrochen
            if len(verschiebe_ar) != 2:
                return (0, False)

            else:
                # Die nötigen Verschiebungen nach rechts werden berechnet
                verschiebung = []
                for element in verschiebe_ar:
                    new_position = position
                    backstart = element[1]
                    while new_position < backstart:
                        if array_on[new_position - 1] == 0:
                            new_position = new_position + 1
                        else:
                            array_on[new_position] = array_on[new_position - 1]
                            verschiebung.append((array_on[new_position], '1 rechts'))
                            new_position = new_position +    2

        # Falls nur ein freier Parkplatz nach rechts benötigt wird: Auto steht mit der hinteren Hälfte auf der Position
        if need_2 == False:
            new_pos = position + 2
            verschiebe_ar = []
            # Der freie Parkplatz wird gesucht.
            while new_pos <= len(array_on):
                if array_on[new_pos] == 0:
                    verschiebe_ar.append((array_on[new_pos - 1], new_pos))
                    break
                else:
                    new_pos = new_pos + 1
            back_start = verschiebe_ar[0][1]
            verschiebung = []
            new_position = position + 1
            # Die einzelnen Verschiebungen werden berechnet:
            while new_position < back_start:
                array_on[new_position] = array_on[new_position -1]
                verschiebung.append((array_on[new_position], '1 rechts'))
                new_position = new_position + 2
        return (len(verschiebung), verschiebung)
    except:
        return (0, False)

# Das blockierende Auto nach links wegbewegen
def testing_nach_links(array2, position):
    verschiebung = []
    array_on = copy.deepcopy(array2)
    # Check ob 2 Verschiebungen nach links nötig sind oder 1 reicht
    if position + 1 < len(array_on):
        if array_on[position + 1] == array_on[position]:
            need_2 = True
        else:
            need_2 = False
    else:
        need_2 = False

    # Falls 1 Verschiebung nach links langt
    if need_2 == False:
        new_pos = position - 2
        verschiebe_ar = []
        while new_pos >= 0:
            if array_on[new_pos] == 0:
                verschiebe_ar.append((array_on[new_pos + 1], new_pos))
                break
            else:
                new_pos = new_pos -1

        # Berechnung der Verschiebung nach Entdecken der freien Parklücke
        back_start = verschiebe_ar[0][1]
        verschiebung = []
        new_position = position - 1
        while new_position > back_start:
            array_on[new_position] = array_on[new_position +1]
            verschiebung.append((array_on[new_position], '1 links'))
            new_position = new_position -2

    # Falls zwei Parklücken benötigt werden
    if need_2:
        new_pos = position - 1
        verschiebe_ar = []
        # 2 freie Parklücken nach links werden gesucht
        while new_pos >= 0:
            if array_on[new_pos] == 0:
                if len(verschiebe_ar) == 1:
                    verschiebe_ar.append((array_on[new_pos + 1], new_pos))
                    break
                else:
                    verschiebe_ar.append((array_on[new_pos + 1], new_pos))
                    new_pos = new_pos - 1
            else:
                new_pos = new_pos - 1

        # Falls keine 2 freien Parkplätze gefunden wurden
        if len(verschiebe_ar) != 2:
            return (0, False)

        else:
            # Berechnung der benötigten Verschiebungen
            array_on = copy.deepcopy(array2)
            verschiebung = []
            for element in verschiebe_ar:
                new_position = position
                back_start = element[1]
                while new_position > back_start:
                    if array_on[new_position + 1] == 0:
                        new_position = new_position -1
                    else:
                        array_on[new_position] = array_on[new_position + 1]
                        verschiebung.append((array_on[new_position], '1 links'))
                        new_position = new_position -2
    return (len(verschiebung), verschiebung)

for x in range(0, len(querpark_liste)):
    score = False
    # Check ob man Querparkende Autos verschieben muss
    if querpark_liste[x] != 0:
        # Check ob man nach Rechts verschieben kann
        if x + 1 <= len(querpark_liste):
            # Check ob sich ein freier Parkplatz zum Verschieben nach rechts findet
            if 0 in querpark_liste[x:]:
                # Falls sich kein freier Parkplatz zum Verschieben nach links findet -> muss nach rechts
                if 0 not in querpark_liste[:x]:
                    rechts = testing_nach_rechts(querpark_liste, x)
                    rechts_string = str(normal_park_liste_buchstaben[x]) + ':'
                    rechts_dic = {}
                    for element in rechts[1]:
                        if element[0] in rechts_dic:
                            rechts_dic[element[0]] = rechts_dic[element[0]] + 1
                        else:
                            rechts_dic[element[0]] = 1
                    for element in rechts_dic:
                        rechts_string = rechts_string + ' ' + element + ' ' + str(rechts_dic[element]) + ' rechts'
                    print(rechts_string)
                # Falls man ebenso nach links verschieben kann
                if 0 in querpark_liste[:x]:
                    links = testing_nach_links(querpark_liste, x)
                    rechts = testing_nach_rechts(querpark_liste, x)
                    # Check ob nach links oder nach rechts mehr Verschiebungen benötigt:
                    # --> Das niedrigere wird ausgegeben
                    if type(rechts[1]) != bool:
                        if type(links[1]) != bool:
                            if rechts[0] <= links[0]:
                                rechts_string = str(normal_park_liste_buchstaben[x]) + ':'
                                rechts_dic = {}
                                for element in rechts[1]:
                                    if element[0] in rechts_dic:
                                        rechts_dic[element[0]] = rechts_dic[element[0]] + 1
                                    else:
                                        rechts_dic[element[0]] = 1
                                for element in rechts_dic:
                                    rechts_string = rechts_string + ' ' + element + ' ' + str(rechts_dic[element]) + ' rechts'
                                print(rechts_string)
                                score = True
                        else:
                            rechts_string = str(normal_park_liste_buchstaben[x]) + ':'
                            rechts_dic = {}
                            for element in rechts[1]:
                                if element[0] in rechts_dic:
                                    rechts_dic[element[0]] = rechts_dic[element[0]] + 1
                                else:
                                    rechts_dic[element[0]] = 1
                            for element in rechts_dic:
                                rechts_string = rechts_string + ' ' + element + ' ' + str(
                                    rechts_dic[element]) + ' rechts'
                            print(rechts_string)
                            score = True
                    if score != True:
                        links_string = str(normal_park_liste_buchstaben[x]) + ':'
                        links_dic = {}
                        for element in links[1]:
                            if element[0] in links_dic:
                                links_dic[element[0]] = links_dic[element[0]] + 1
                            else:
                                links_dic[element[0]] = 1
                        for element in links_dic:
                            links_string = links_string + ' ' + element + ' ' + str(links_dic[element]) + ' links'
                        print(links_string)
            # Falls ein Verschieben nach rechts nicht möglich ist, da man an der äußersten pPosition angelangt ist
            else:
                links = testing_nach_links(querpark_liste, x)
                links_string = str(normal_park_liste_buchstaben[x]) + ':'
                links_dic = {}
                for element in links[1]:
                    if element[0] in links_dic:
                        links_dic[element[0]] = links_dic[element[0]] + 1
                    else:
                        links_dic[element[0]] = 1
                for element in links_dic:
                    links_string = links_string + ' ' + element + ' ' + str(links_dic[element]) + ' links'
                print(links_string)
        if x + 1 > len(querpark_liste):
            links_string = str(normal_park_liste_buchstaben[x]) + ':'
            links_dic = {}
            for element in links[1]:
                if element[0] in links_dic:
                    links_dic[element[0]] = links_dic[element[0]] + 1
                else:
                    links_dic[element[0]] = 1
            for element in links_dic:
                links_string = links_string + ' ' + element + ' ' + str(links_dic[element]) + ' links'
            print(links_string)
    # Falls keine Verschiebung nötig ist
    else:
        print(normal_park_liste_buchstaben[x] + ': Keine Verschiebung nötig')
