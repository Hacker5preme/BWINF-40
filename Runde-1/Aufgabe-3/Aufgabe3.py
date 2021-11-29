# BWINF: Nr. 40
# Runde: 1
# Aufgabe: 3
# Autor: Ron Jost
# Team: Opensourcehacker (00155)

import random
import sys
import string
import time


# Dateneinlese
worte_datei = open(str(sys.argv[1]), 'r')
lines = worte_datei.readlines()
worte_datei.close()
lines_bearbeitet = []
for line in lines:
    lines_bearbeitet.append(line.replace('\n', ''))

ZeilenNr = int(lines_bearbeitet[0][:lines_bearbeitet[0].find(' ')])
SpaltenNr = int(lines_bearbeitet[0][lines_bearbeitet[0].find(' ') + 1:])
WörterNr = lines_bearbeitet[1]
Wörter_Liste = []
for i in range(1, int(WörterNr) + 1):
    Wörter_Liste.append(lines_bearbeitet[1 + i])

# 1. Einfach: Nur Horizontal und Vertikal
def Einfach(ZeilenNr, SpaltenNr, Wörter_Liste):
    Wörter_Liste = sorted(Wörter_Liste, key=len)
    Wörter_Liste = Wörter_Liste[::-1]
    # Konstruktion des grids, dem leeren Wortsucherätsel
    grid = [['0' for _ in range(int(SpaltenNr))] for _ in range(int(ZeilenNr))]
    Richtungen = ['horizontal', 'vertikal']
    Error = False
    # Sollte es unmöglich sein, ein Wort unterzubringen, wird wieder von vorne gestartet, mit allen Worten
    while Error == False:
        try:
            for Wort in Wörter_Liste:
                Wortlänge = len(Wort)
                platziert = False
                t_end = time.time() + 5
                while not platziert:
                    if time.time() < t_end:
                        failed = False
                        #Zufällige Entscheidung, welche Richtung genommen wird.
                        Richtung = random.choice(Richtungen)

                        if Richtung == 'vertikal':
                            step_Zeile = 1
                            step_Spalte = 0
                            maximum_Zeile = ZeilenNr - Wortlänge
                            Zeilen_position = random.randrange(0, maximum_Zeile + 1)
                            Spalten_position = random.randrange(0, SpaltenNr +1)

                        if Richtung == 'horizontal':
                            step_Zeile = 0
                            step_Spalte = 1
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(ZeilenNr +1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        for i in range(Wortlänge):
                            # Das Wort wird Buchstabe für Buchstabe mit den Werten in der Tabelle verglichen
                            Buchstabe = Wort[i]
                            neu_Zeile = Zeilen_position + i * step_Zeile
                            neu_Spalte = Spalten_position + i * step_Spalte
                            Buchstabe_neue_Position = grid[neu_Zeile][neu_Spalte]
                            if Buchstabe_neue_Position != '0':
                                if Buchstabe_neue_Position == Buchstabe:
                                    continue
                                # Wenn der Buchstabe an der neuen Position x keine 0 sondern ein anderer Buchstabe,
                                # als der einzusetztende ist, muss abgebrochen werden und das Wort muss neu platziert werden
                                else:
                                    failed = True
                                    break
                        if failed:
                            continue
                        else:
                            # Das Wort je nach gewählter Richtung Buchstabe für Buchstabe eingetragen
                            for i in range(Wortlänge):
                                Buchstabe = Wort[i]
                                neu_Zeile = Zeilen_position + i * step_Zeile
                                neu_Spalte = Spalten_position + i * step_Spalte
                                grid[neu_Zeile][neu_Spalte] = Buchstabe
                            platziert = True
                            break

            # Die restlichen Leerstellen werden mit zufälligen Großbuchstaben aufgefüllt
            for x in range(ZeilenNr):
                for y in range(SpaltenNr):
                    if grid[x][y] == '0':
                        grid[x][y] = random.choice(string.ascii_uppercase)

            # Ausgabe des Wortsucherätsels
            for x in range(ZeilenNr):
                print('\t' * 2 + ''.join(grid[x]))
            Error = True
        except IndexError:
            grid = [['0' for _ in range(int(SpaltenNr))] for _ in range(int(ZeilenNr))]

# 2. Mittel: Horizontal, Vertikal und diagonal von links nach rechts von unten nach oben und von oben nach unten:
def Mittel(ZeilenNr, SpaltenNr, Wörter_Liste):
    Wörter_Liste = sorted(Wörter_Liste, key=len)
    Wörter_Liste = Wörter_Liste[::-1]
    # Konstruktion des grids, dem leeren Wortsucherätsel
    grid = [['0' for _ in range(int(SpaltenNr))] for _ in range(int(ZeilenNr))]
    Richtungen = ['vertikal', 'horizontal', 'diagonal-lr-down', 'diagonal-lr-up']
    Error = False
    while Error == False:
        try:
            for Wort in Wörter_Liste:
                Wortlänge = len(Wort)
                platziert = False
                t_end = time.time() + 5
                while not platziert:
                    if time.time() < t_end:
                        failed = False
                        # Zufälliges Aussuchen der Richtung
                        Richtung = random.choice(Richtungen)

                        if Richtung == 'vertikal':
                            step_Zeile = 1
                            step_Spalte = 0
                            maximum_Zeile = ZeilenNr - Wortlänge
                            Zeilen_position = random.randrange(0, maximum_Zeile + 1)
                            Spalten_position = random.randrange(0, SpaltenNr + 1)

                        if Richtung == 'horizontal':
                            step_Zeile = 0
                            step_Spalte = 1
                            maximum_Spalte = SpaltenNr - Wortlänge

                            Zeilen_position = random.randrange(ZeilenNr + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        if Richtung == 'diagonal-lr-down':
                            step_Zeile = 1
                            step_Spalte = 1
                            maximum_Zeile = ZeilenNr - Wortlänge
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(maximum_Zeile + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        if Richtung == 'diagonal-lr-up':
                            step_Zeile = -1
                            step_Spalte = 1
                            minimum_Zeile = Wortlänge
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(minimum_Zeile, ZeilenNr +1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        for i in range(Wortlänge):
                            # Das Wort wird Buchstabe für Buchstabe mit den Werten in der Tabelle verglichen
                            Buchstabe = Wort[i]
                            neu_Zeile = Zeilen_position + i * step_Zeile
                            neu_Spalte = Spalten_position + i * step_Spalte
                            Buchstabe_neue_Position = grid[neu_Zeile][neu_Spalte]
                            if Buchstabe_neue_Position != '0':
                                if Buchstabe_neue_Position == Buchstabe:
                                    continue
                                else:
                                    failed = True
                                    break
                        if failed:
                            continue
                        else:
                            for i in range(Wortlänge):
                                # Das Wort je nach gewählter Richtung Buchstabe für Buchstabe eingetragen
                                Buchstabe = Wort[i]
                                neu_Zeile = Zeilen_position + i * step_Zeile
                                neu_Spalte = Spalten_position + i * step_Spalte
                                grid[neu_Zeile][neu_Spalte] = Buchstabe
                            platziert = True
                            break

            for x in range(ZeilenNr):
                for y in range(SpaltenNr):
                    # Die übrig gebliebenen Leerstellen werden aufgefüllt
                    if grid[x][y] == '0':
                        grid[x][y] = random.choice(string.ascii_uppercase)

            for x in range(ZeilenNr):
                # Ausgabe des Wortsucherätsels
                print('\t' * 2 + ''.join(grid[x]))
            Error = True
        except IndexError:
            grid = [['0' for _ in range(int(SpaltenNr))] for _ in range(int(ZeilenNr))]

# 3. Schwer: Horizontal, Vertikal, Diagonal l-r, Diagonal r-l und alle Wörter können rückwärts vorkommen
def Schwer(ZeilenNr, SpaltenNr, Wörter_Liste):
    Wörter_Liste = sorted(Wörter_Liste, key=len)
    Wörter_Liste = Wörter_Liste[::-1]
    grid = [['0' for _ in range(int(SpaltenNr))] for _ in range(int(ZeilenNr))]
    Richtungen = ['vertikal', 'horizontal', 'diagonal-lr-down', 'diagonal-lr-up', 'diagonal-rl-down', 'diagonal-rl-up']
    Richtungen.append('vertikal-rev')
    Richtungen.append('horizontal-rev')
    Error = False
    # Sollte es unmöglich sein, ein Wort unterzubringen, wird wieder von vorne gestartet, mit allen Worten
    while Error == False:
        try:
            for Wort in Wörter_Liste:
                Wortlänge = len(Wort)
                platziert = False
                t_end = time.time() + 5
                while not platziert:
                    if time.time() < t_end:
                        failed = False
                        Richtung = random.choice(Richtungen)
                        if Richtung == 'vertikal':
                            step_Zeile = 1
                            step_Spalte = 0
                            maximum_Zeile = ZeilenNr - Wortlänge
                            Zeilen_position = random.randrange(0, maximum_Zeile + 1)
                            Spalten_position = random.randrange(0, SpaltenNr + 1)

                        if Richtung == 'horizontal':
                            step_Zeile = 0
                            step_Spalte = 1
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(ZeilenNr + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        if Richtung == 'diagonal-lr-down':
                            step_Zeile = 1
                            step_Spalte = 1
                            maximum_Zeile = ZeilenNr - Wortlänge
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(maximum_Zeile + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        if Richtung == 'diagonal-lr-up':
                            step_Zeile = -1
                            step_Spalte = 1
                            minimum_Zeile = Wortlänge
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(minimum_Zeile, ZeilenNr +1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        if Richtung == 'diagonal-rl-down':
                            step_Zeile = 1
                            step_Spalte =  -1
                            maximum_Zeile = ZeilenNr - Wortlänge
                            minimum_Spalte = Wortlänge
                            Zeilen_position = random.randrange(maximum_Zeile +1)
                            Spalten_position = random.randrange(minimum_Spalte, SpaltenNr +1)

                        if Richtung == 'diagonal-rl-up':
                            step_Zeile = -1
                            step_Spalte = -1
                            minimum_Zeile = Wortlänge
                            minimum_Spalte = Wortlänge
                            Zeilen_position = random.randrange(minimum_Zeile, ZeilenNr +1)
                            Spalten_position = random.randrange(minimum_Spalte, SpaltenNr +1)

                        if Richtung == 'vertikal-rev':
                            Wort = Wort[::-1]
                            step_Zeile = 1
                            step_Spalte = 0
                            maximum_Zeile = ZeilenNr - Wortlänge
                            Zeilen_position = random.randrange(0, maximum_Zeile + 1)
                            Spalten_position = random.randrange(0, SpaltenNr + 1)

                        if Richtung == 'horizontal-rev':
                            Wort = Wort[::-1]
                            step_Zeile = 0
                            step_Spalte = 1
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(ZeilenNr + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        for i in range(Wortlänge):
                            Buchstabe = Wort[i]
                            neu_Zeile = Zeilen_position + i * step_Zeile
                            neu_Spalte = Spalten_position + i * step_Spalte
                            Buchstabe_neue_Position = grid[neu_Zeile][neu_Spalte]
                            if Buchstabe_neue_Position != '0':
                                if Buchstabe_neue_Position == Buchstabe:
                                    continue
                                else:
                                    failed = True
                                    break
                        if failed:
                            continue
                        else:
                            for i in range(Wortlänge):
                                Buchstabe = Wort[i]
                                neu_Zeile = Zeilen_position + i * step_Zeile
                                neu_Spalte = Spalten_position + i * step_Spalte
                                grid[neu_Zeile][neu_Spalte] = Buchstabe
                            platziert = True
                            break

            for x in range(ZeilenNr):
                for y in range(SpaltenNr):
                    if grid[x][y] == '0':
                        grid[x][y] = random.choice(string.ascii_uppercase)

            for x in range(ZeilenNr):
                print('\t' * 2 + ''.join(grid[x]))
            Error = True
        except IndexError:
            grid = [['0' for _ in range(int(SpaltenNr))] for _ in range(int(ZeilenNr))]

# 4. Extrem: Horizontal, Vertikal, Diagonal l-r, Diagonal r-l und alle Wörter können rückwärts vorkommen
#            Das Wortsucherätsel wird mit Buchstaben, der unterzubringenden Wörter aufgefüllt
def Extrem(ZeilenNr, SpaltenNr, Wörter_Liste):
    Wörter_Liste = sorted(Wörter_Liste, key=len)
    Wörter_Liste = Wörter_Liste[::-1]
    grid = [['0' for _ in range(int(SpaltenNr))] for _ in range(int(ZeilenNr))]
    Richtungen = ['vertikal', 'horizontal', 'diagonal-lr-down', 'diagonal-lr-up', 'diagonal-rl-down', 'diagonal-rl-up']
    Richtungen.append('vertikal-rev')
    Richtungen.append('horitontal-rev')
    Buchstaben = []
    for Wort in Wörter_Liste:
        for char in Wort:
            Buchstaben.append(char)
    Buchstaben = list(dict.fromkeys(Buchstaben))
    Error = False
    while Error == False:
        try:
            for Wort in Wörter_Liste:
                Wortlänge = len(Wort)
                platziert = False
                t_end = time.time() + 5
                while not platziert:
                    if time.time() < t_end:
                        failed = False
                        Richtung = random.choice(Richtungen)
                        if Richtung == 'vertikal':
                            step_Zeile = 1
                            step_Spalte = 0
                            maximum_Zeile = ZeilenNr - Wortlänge
                            Zeilen_position = random.randrange(0, maximum_Zeile + 1)
                            Spalten_position = random.randrange(0, SpaltenNr + 1)

                        if Richtung == 'horizontal':
                            step_Zeile = 0
                            step_Spalte = 1
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(ZeilenNr + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        if Richtung == 'diagonal-lr-down':
                            step_Zeile = 1
                            step_Spalte = 1
                            maximum_Zeile = ZeilenNr - Wortlänge
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(maximum_Zeile + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        if Richtung == 'diagonal-lr-up':
                            step_Zeile = -1
                            step_Spalte = 1
                            minimum_Zeile = Wortlänge
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(minimum_Zeile, ZeilenNr + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        if Richtung == 'diagonal-rl-down':
                            step_Zeile = 1
                            step_Spalte = -1
                            maximum_Zeile = ZeilenNr - Wortlänge
                            minimum_Spalte = Wortlänge
                            Zeilen_position = random.randrange(maximum_Zeile + 1)
                            Spalten_position = random.randrange(minimum_Spalte, SpaltenNr + 1)

                        if Richtung == 'diagonal-rl-up':
                            step_Zeile = -1
                            step_Spalte = -1
                            minimum_Zeile = Wortlänge
                            minimum_Spalte = Wortlänge
                            Zeilen_position = random.randrange(minimum_Zeile, ZeilenNr + 1)
                            Spalten_position = random.randrange(minimum_Spalte, SpaltenNr + 1)

                        if Richtung == 'vertikal-rev':
                            Wort = Wort[::-1]
                            step_Zeile = 1
                            step_Spalte = 0
                            maximum_Zeile = ZeilenNr - Wortlänge
                            Zeilen_position = random.randrange(0, maximum_Zeile + 1)
                            Spalten_position = random.randrange(0, SpaltenNr + 1)

                        if Richtung == 'horizontal-rev':
                            Wort = Wort[::-1]
                            step_Zeile = 0
                            step_Spalte = 1
                            maximum_Spalte = SpaltenNr - Wortlänge
                            Zeilen_position = random.randrange(ZeilenNr + 1)
                            Spalten_position = random.randrange(maximum_Spalte + 1)

                        for i in range(Wortlänge):
                            Buchstabe = Wort[i]
                            neu_Zeile = Zeilen_position + i * step_Zeile
                            neu_Spalte = Spalten_position + i * step_Spalte
                            Buchstabe_neue_Position = grid[neu_Zeile][neu_Spalte]
                            if Buchstabe_neue_Position != '0':
                                if Buchstabe_neue_Position == Buchstabe:
                                    continue
                                else:
                                    failed = True
                                    break
                        if failed:
                            continue
                        else:
                            for i in range(Wortlänge):
                                Buchstabe = Wort[i]
                                neu_Zeile = Zeilen_position + i * step_Zeile
                                neu_Spalte = Spalten_position + i * step_Spalte
                                grid[neu_Zeile][neu_Spalte] = Buchstabe
                            platziert = True
                            break

            for x in range(ZeilenNr):
                # Hier wird anstatt string.ascii.uppercase Buchstaben als Basis verwendet
                for y in range(SpaltenNr):
                    if grid[x][y] == '0':
                        grid[x][y] = random.choice(Buchstaben)

            for x in range(ZeilenNr):
                print('\t' * 2 + ''.join(grid[x]))
            Error = True
        except IndexError:
            grid = [['0' for _ in range(int(SpaltenNr))] for _ in range(int(ZeilenNr))]

# Ausführug der Funktionen:
Schwierigkeit = sys.argv[2]
if Schwierigkeit == 'Einfach':
    Einfach(ZeilenNr,SpaltenNr,Wörter_Liste)
if Schwierigkeit == 'Mittel':
    Mittel(ZeilenNr, SpaltenNr, Wörter_Liste)
if Schwierigkeit == 'Schwer':
    Schwer(ZeilenNr, SpaltenNr, Wörter_Liste)
if Schwierigkeit == 'Extrem':
    Extrem(ZeilenNr, SpaltenNr, Wörter_Liste)
print('')
print('Wörter versteckt:')
print(', '.join(Wörter_Liste))
