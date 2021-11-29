# BWINF: Nr. 40
# Runde: 1
# Aufgabe: 4
# Autor: Ron Jost
# Team: Opensourcehacker (00155)

import sys
import itertools
import random

würfel_datei = sys.argv[1]
würfel_daten = open(würfel_datei, 'r').readlines()
würfel_daten_bearbeitet = []
for line in würfel_daten:
    würfel_daten_bearbeitet.append(line.replace('\n', ''))
Anzahl_Würfel = würfel_daten_bearbeitet[0]
Würfel = {}
for i in range(int(Anzahl_Würfel)):
    würfel_info = würfel_daten_bearbeitet[i+1]
    würfel_seiten = würfel_info[:würfel_info.find(' ')]
    würfel_info = würfel_info[würfel_info.find(' ')+1:].split()
    würfel_info = [int(x) for x in würfel_info]
    Würfel[i] = (int(würfel_seiten), würfel_info)


# Berechne mögliche Partien:
Partien = []
for key in Würfel:
    Partien.append(key)
Partien = list(itertools.combinations(Partien,2))

for Partie in Partien:
    player1_würfel = Würfel[Partie[0]][1]
    player2_würfel = Würfel[Partie[1]][1]


#(Würfel)

def Spielfeld():
    # Haus der Figuren, die auf ins Spiel bringen warten:
    player1_Box = [1,1,1,1]
    player2_Box = [2,2,2,2]

    # Spielfeld Startpunkt der Indizes ist das Gelbe A Feld und dann in Uhrzeigerrichtung:
    Feld = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Start_indizes = {'Gelb': 0,
                     'Grün': 10,
                     'Rot': 20,
                     'Schwarz': 30
                     }
    Ziele = {'Grün': (9, [0,0,0,0]),
             'Rot': (19, [0,0,0,0]),
             'Schwarz': (29, [0,0,0,0]),
             'Gelb': (39,[0,0,0,0])
            }
    return player1_Box, player2_Box, Feld, Ziele, Start_indizes

def move(Spieler, Feld, Würfel, player1_box, player2_box, Ziel):
    '''
    Regeln:
    Der vorderste Stein wird gezogen
    Man kann wenn kein Stein bewegbar ist, auf dem Feld im Zielfeld nach vorne
    Solange noch andere Figuren in der Box warten muss das Start Feld sofort freigemacht werden
    Besonderheit 6:
    Man muss einen Stein aus der Box ins Feld bringen, wenn das Feld frei ist + in der box etwas ist
    -> Man kann nach dem Zug direkt nochmal ziehen
    Es muss immer geschlagen werden --> Back to box
    '''
    if Spieler == 1:
        # Wird mit Gelb gespielt; Würfel 1
        Augenzahl = random.choice(Würfel)
        # Wenn keine 6 und keine 0 ist
        if Augenzahl != 6 and Augenzahl != 0:
            # Erster check, ob Startfeld belegt ist und man sich wegbewegen kann
            if Feld[0] == 1 and Feld[Augenzahl] != 1:
                # Ohne Schlagen bewegen
                if Feld[Augenzahl] == 0:
                    Feld[Augenzahl] = 1
                    Feld[0] = 0

                # Mit Schlagen bewegen
                else:
                    Feld[Augenzahl] = 1
                    player2_box[player2_box.index(0)] = 2
                    Feld[0] = 0


            # Vordersten Stein bewegen
            else:
                failed_Ziel = False
                # Höchste Steine: Im Ziel:
                Ziel_indizes = [i for i, x in enumerate(Ziel[1]) if x == 1][::-1]
                if len(Ziel_indizes) != 0:
                    for element in Ziel_indizes:
                        if (element + Augenzahl) > len(Ziel[1])-1:
                            pass
                        else:
                            if Ziel[1][element + Augenzahl] == 0:
                                Ziel[1][element+Augenzahl] = 1
                                Ziel[1][element] = 0
                                break
                    failed_Ziel = True
                # Wenn man keinen Stein im Ziel bewegen kann
                if len(Ziel_indizes) == 0 or failed_Ziel == True:
                    indices = [i for i, x in enumerate(Feld) if x == 1][::-1]
                    for Stein in indices:
                        # Vor dem Ziel move ohne Schlagen
                        if Stein + Augenzahl <= Ziel[0]:
                            if Feld[Stein + Augenzahl] == 0:
                                Feld[Stein + Augenzahl] = 1
                                Feld[Stein] = 0
                                break

                            # Gegnerische Figur
                            if Feld[Stein+ Augenzahl] == 2:
                                # SCHLAGEN
                                Feld[Stein + Augenzahl] = 1
                                player2_box[player2_box.index(0)] = 2
                                Feld[Stein] = 0
                                break
                            # Falls keins von beiden, passiert nichts, nächster Stein

                        else:
                            Züge_nach_Zielfeld = Augenzahl - ( Ziel[0] - Stein)
                            # Falls man über das Ziel herrausschießen würde
                            if Züge_nach_Zielfeld > 4:
                                pass
                            # Falls es passen würde
                            else:
                                if Ziel[1][Züge_nach_Zielfeld-1] == 1:
                                    pass
                                else:
                                    Ziel[1][Züge_nach_Zielfeld-1] = 1
                                    Feld[Stein] = 0
                                    break
        else:
            if Augenzahl == 0:
                pass
            if Augenzahl == 6:
                # Erster Check: Ob sich noch Figuren in der Box befinden:
                Box_indizes = [i for i, x in enumerate(player1_box) if x == 1]
                # Falls sich Figuren in der Box befinden + das Startfeld nicht belegt ist
                if len(Box_indizes) != 0 and Feld[0] != 1:
                    # Falls es frei ist:
                    if Feld[0] == 0:
                        Feld[0] = 1
                        player1_box[player1_box.index(1)] = 0

                    # Falls geschlagen werden muss
                    else:
                        Feld[0] = 1
                        player2_box[player2_box.index(0)] = 2
                        player1_box[player1_box.index(1)] = 0

                # Falls sich keine Figuren mehr in der Box befinden oder das Feld belegt ist:
                else:
                    indices = [i for i, x in enumerate(Feld) if x == 1]
                    # Erster check, ob Startfeld belegt ist und man sich wegbewegen kann
                    if Feld[0] == 1 and Feld[Augenzahl] != 1:
                        # Ohne Schlagen bewegen
                        if Feld[Augenzahl] == 0:
                            Feld[Augenzahl] = 1
                            Feld[0] = 0

                        # Mit Schlagen bewegen
                        else:
                            Feld[Augenzahl] = 1
                            Feld[0] = 0
                            player2_box[player2_box.index(0)] = 2

                    # Vordersten Stein bewegen
                    else:
                        failed_Ziel = False
                        # Höchste Steine: Im Ziel:
                        Ziel_indizes = [i for i, x in enumerate(Ziel[1]) if x == 1][::-1]
                        if len(Ziel_indizes) != 0:
                            for element in Ziel_indizes:
                                if (element + Augenzahl) > len(Ziel[1]) - 1:
                                    pass
                                else:
                                    if Ziel[1][element + Augenzahl] == 0:
                                        Ziel[1][element + Augenzahl] = 1
                                        Ziel[1][element] = 0
                                        break
                            failed_Ziel = True
                        # Wenn man keinen Stein im Ziel bewegen kann
                        if len(Ziel_indizes) == 0 or failed_Ziel == True:
                            indices = [i for i, x in enumerate(Feld) if x == 1][::-1]
                            for Stein in indices:
                                # Vor dem Ziel move ohne Schlagen
                                if Stein + Augenzahl <= Ziel[0]:
                                    if Feld[Stein + Augenzahl] == 0:
                                        Feld[Stein + Augenzahl] = 1
                                        Feld[Stein] = 0
                                        break

                                    # Gegnerische Figur
                                    if Feld[Stein + Augenzahl] == 2:
                                        Feld[Stein + Augenzahl] = 1
                                        player2_box[player2_box.index(0)] = 2
                                        Feld[Stein] = 0
                                        break

                                    # Falls keins von beiden, passiert nichts, nächster Stein
                                else:
                                    Züge_nach_Zielfeld = Augenzahl - (Ziel[0] - Stein)
                                    # Falls man über das Ziel herrausschießen würde
                                    if Züge_nach_Zielfeld > 4:
                                        pass
                                    # Falls es passen würde
                                    else:
                                        if Ziel[1][Züge_nach_Zielfeld - 1] == 1:
                                            pass
                                        else:
                                            Ziel[1][Züge_nach_Zielfeld - 1] = 1
                                            Feld[Stein] = 0
                                            break
                # Da Spieler 1 eine 6 gewürfelt hat, darf er nochmal
                move(1, Feld, Würfel, player1_box,player2_box, Ziel)

    if Spieler == 2:
        # Umkonstruktion von Feld: ( WIrd am Ende des Zuges immer wieder umkonstruiert)
        Spieler_2_Feld = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Ziel = (39, Ziel[1])
        for element in range(20,40):
            Spieler_2_Feld[element-20] = Feld[element]
        for element in range(20):
            Spieler_2_Feld[element+20] = Feld[element]

        # Wird mit Rot gespielt
        Augenzahl = random.choice(Würfel)

        # Wenn keine 6 und keine 0 ist
        if Augenzahl != 6 and Augenzahl != 0:
            # Erster check, ob Startfeld belegt ist und man sich wegbewegen kann
            if Spieler_2_Feld[0] == 2 and Spieler_2_Feld[Augenzahl] != 2:
                # Ohne Schlagen bewegen
                if Spieler_2_Feld[Augenzahl] == 0:
                    Spieler_2_Feld[Augenzahl] = 2
                    Spieler_2_Feld[0] = 0
                    # Mit Schlagen bewegen
                else:
                    # SCHLAGEN
                    Spieler_2_Feld[Augenzahl] = 2
                    Spieler_2_Feld[0] = 0
                    player1_box[player1_box.index(0)] = 1

            # Vordersten Stein bewegen
            else:
                failed_Ziel = False
                # Höchste Steine: Im Ziel:
                Ziel_indizes = [i for i, x in enumerate(Ziel[1]) if x == 2][::-1]
                if len(Ziel_indizes) != 0:
                    for element in Ziel_indizes:
                        if (element + Augenzahl) > len(Ziel[1]) - 1:
                            pass
                        else:
                            if Ziel[1][element + Augenzahl] == 0:
                                Ziel[1][element + Augenzahl] = 2
                                Ziel[1][element] = 0
                                break
                    failed_Ziel = True
                    # Wenn man keinen Stein im Ziel bewegen kann
                if len(Ziel_indizes) == 0 or failed_Ziel == True:
                    indices = [i for i, x in enumerate(Spieler_2_Feld) if x == 2][::-1]
                    for Stein in indices:
                        # Vor dem Ziel move ohne Schlagen
                        if Stein + Augenzahl <= Ziel[0]:
                            if Spieler_2_Feld[Stein + Augenzahl] == 0:
                                Spieler_2_Feld[Stein + Augenzahl] = 2
                                Spieler_2_Feld[Stein] = 0
                                break

                            # Gegnerische Figur
                            if Spieler_2_Feld[Stein + Augenzahl] == 1:
                                # SCHLAGEN
                                Spieler_2_Feld[Stein + Augenzahl] = 2
                                Spieler_2_Feld[Stein] = 0
                                player1_box[player1_box.index(0)] = 1
                                break
                            # Falls keins von beiden, passiert nichts, nächster Stein

                        else:
                            Züge_nach_Zielfeld = Augenzahl - (Ziel[0] - Stein)
                            # Falls man über das Ziel herrausschießen würde
                            if Züge_nach_Zielfeld > 4:
                                pass
                            # Falls es passen würde
                            else:
                                if Ziel[1][Züge_nach_Zielfeld - 1] == 2:
                                    pass
                                else:
                                    Ziel[1][Züge_nach_Zielfeld - 1] = 2
                                    Spieler_2_Feld[Stein] = 0
                                break
        else:
            if Augenzahl == 0:
                pass
            if Augenzahl == 6:
                # Erster Check: Ob sich noch Figuren in der Box befinden:
                Box_indizes = [i for i, x in enumerate(player2_box) if x == 2]
                # Falls sich Figuren in der Box befinden + das Startfeld nicht belegt ist
                if len(Box_indizes) != 0 and Spieler_2_Feld[0] != 2:
                    # Falls es frei ist:
                    if Spieler_2_Feld[0] == 0:
                        Spieler_2_Feld[0] = 2
                        player2_box[Box_indizes[0]] = 0

                    # Falls geschlagen werden muss
                    else:
                        Spieler_2_Feld[0] = 2
                        player2_box[player2_box.index(2)] = 0
                        player1_box[player1_box.index(0)] = 1



                # Falls sich keine Figuren mehr in der Box befinden oder das Feld belegt ist:
                else:
                    # Erster check, ob Startfeld belegt ist und man sich wegbewegen kann
                    if Spieler_2_Feld[0] == 2 and Spieler_2_Feld[Augenzahl] != 2:
                        # Ohne Schlagen bewegen
                        if Spieler_2_Feld[Augenzahl] == 0:
                            Spieler_2_Feld[Augenzahl] = 2
                            Spieler_2_Feld[0] = 0
                            # Mit Schlagen bewegen
                        else:
                            Spieler_2_Feld[Augenzahl] = 2
                            Spieler_2_Feld[0] = 0
                            player1_box[player1_box.index(0)] = 1

                    # Vordersten Stein bewegen
                    else:
                        failed_Ziel = False
                        # Höchste Steine: Im Ziel:
                        Ziel_indizes = [i for i, x in enumerate(Ziel[1]) if x == 2][::-1]
                        if len(Ziel_indizes) != 0:
                            for element in Ziel_indizes:
                                if (element + Augenzahl) > len(Ziel[1]) - 1:
                                    pass
                                else:
                                    if Ziel[1][element + Augenzahl] == 0:
                                        Ziel[1][element + Augenzahl] = 2
                                        Ziel[1][element] = 0
                                        break
                            failed_Ziel = True
                            # Wenn man keinen Stein im Ziel bewegen kann
                        if len(Ziel_indizes) == 0 or failed_Ziel == True:
                            indices = [i for i, x in enumerate(Spieler_2_Feld) if x == 2][::-1]
                            for Stein in indices:
                                # Vor dem Ziel move ohne Schlagen
                                if Stein + Augenzahl <= Ziel[0]:
                                    if Spieler_2_Feld[Stein + Augenzahl] == 0:
                                        Spieler_2_Feld[Stein + Augenzahl] = 2
                                        Spieler_2_Feld[Stein] = 0
                                        break

                                    # Gegnerische Figur
                                    if Spieler_2_Feld[Stein + Augenzahl] == 1:
                                        # SCHLAGEN
                                        Spieler_2_Feld[Stein + Augenzahl] = 2
                                        Spieler_2_Feld[Stein] = 0
                                        player1_box[player1_box.index(0)] = 1
                                        break
                                    # Falls keins von beiden, passiert nichts, nächster Stein

                                else:
                                    Züge_nach_Zielfeld = Augenzahl - (Ziel[0] - Stein)
                                    # Falls man über das Ziel herrausschießen würde
                                    if Züge_nach_Zielfeld > 4:
                                        pass
                                    # Falls es passen würde
                                    else:
                                        if Ziel[1][Züge_nach_Zielfeld - 1] == 2:
                                            pass
                                        else:
                                            Ziel[1][Züge_nach_Zielfeld - 1] = 2
                                            Spieler_2_Feld[Stein] = 0
                                        break
        # Umwandlung Feld_Spieler 2:
        Feld = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for element in range(20, 40):
            Feld[element -20] = Spieler_2_Feld[element]
        for element in range(20):
            Feld[element + 20] = Spieler_2_Feld[element]
    return Feld, player1_box, player2_box, Ziel


def Spiel(Start_Spieler, Feld, player1_würfel, player2_würfel, Anzahl_Züge_pro_Spiel_max):
    # Spieler 1 spielt mit Gelb, Spieler 2 mit Rot
    Feld_Spielstart = Feld[2]
    Start_indizes = Feld[4]
    player1_Box = Feld[0]
    player2_Box = Feld[1]
    Ziele = Feld[3]
    Feld_Spielstart[Start_indizes['Gelb']] = 1
    Feld_Spielstart[Start_indizes['Rot']] = 2
    player1_Box[0] = 0
    player2_Box[0] = 0
    if Start_Spieler == 1:
        Sieg_1 = False
        Sieg_2 = False
        move_er_1 = move(1, Feld_Spielstart, player1_würfel, player1_Box, player2_Box, Ziele['Gelb'])
        Feld = move_er_1[0]
        player1_Box = move_er_1[1]
        player2_Box = move_er_1[2]
        Ziel_gelb = move_er_1[3]
        move_er_2 = move(2, Feld, player2_würfel, player1_Box, player2_Box, Ziele['Rot'])
        Feld = move_er_2[0]
        player1_Box = move_er_2[1]
        player2_Box = move_er_2[2]
        Ziel_rot = move_er_2[3]
        # Maximal 1000 Züge pro Spiel
        züge_score = 0
        while Sieg_1 == False and Sieg_2 == False and züge_score <= Anzahl_Züge_pro_Spiel_max:
            move_er_1 = move(1, Feld, player1_würfel, player1_Box, player2_Box, Ziel_gelb)
            Feld = move_er_1[0]
            player1_Box = move_er_1[1]
            player2_Box = move_er_1[2]
            Ziel_gelb = move_er_1[3]
            if Ziel_gelb[1].count(1) == 4:
                Sieg_1 = True
                break
            move_er_2 = move(2, Feld, player2_würfel, player1_Box, player2_Box, Ziel_rot)
            Feld = move_er_2[0]
            player1_Box = move_er_2[1]
            player2_Box = move_er_2[2]
            Ziel_rot = move_er_2[3]
            if Ziel_rot[1].count(2):
                Sieg_2 = True
                break
            züge_score = züge_score + 1

            
    if Start_Spieler == 2:
        Sieg_1 = False
        Sieg_2 = False
        move_er_2 = move(2, Feld_Spielstart, player2_würfel, player1_Box, player2_Box, Ziele['Rot'])
        Feld = move_er_2[0]
        player1_Box = move_er_2[1]
        player2_Box = move_er_2[2]
        Ziel_rot = move_er_2[3]
        move_er_1 = move(1, Feld, player1_würfel, player1_Box, player2_Box, Ziele['Gelb'])
        Feld = move_er_1[0]
        player1_Box = move_er_1[1]
        player2_Box = move_er_1[2]
        Ziel_gelb = move_er_1[3]
        züge_score = 0
        while Sieg_1 == False and Sieg_2 == False and züge_score <= Anzahl_Züge_pro_Spiel_max:
            move_er_2 = move(2, Feld, player2_würfel, player1_Box, player2_Box, Ziel_rot)
            Feld = move_er_2[0]
            player1_Box = move_er_2[1]
            player2_Box = move_er_2[2]
            Ziel_rot = move_er_2[3]
            if Ziel_rot[1].count(2) == 4:
                Sieg_2 = True
                break
            move_er_1 = move(1, Feld, player1_würfel, player1_Box, player2_Box, Ziel_gelb)
            Feld = move_er_1[0]
            player1_Box = move_er_1[1]
            player2_Box = move_er_1[2]
            Ziel_gelb = move_er_1[3]
            if Ziel_gelb[1].count(1) == 4:
                Sieg_1 = True
                break
            züge_score = züge_score + 1
    return Sieg_1, Sieg_2


def Spiel_simulation(player1_würfel, player2_würfel, Start_Spieler, Anzahl_max_Zug):
    Feld = Spielfeld()
    Sieg = Spiel(Start_Spieler, Feld, player1_würfel, player2_würfel, Anzahl_max_Zug)
    if Sieg[0]:
        return 1
    if Sieg[1]:
        return 2


Anzahl_wiederholungen_Partie = int(sys.argv[2])
Anzahl_Züge_pro_Spiel_max = int(sys.argv[3])
for Partie in Partien:
    Siege = []
    player1_würfel = Würfel[Partie[0]][1]
    player2_würfel = Würfel[Partie[1]][1]
    for i in range(int(Anzahl_wiederholungen_Partie/2)):
        Sieg = Spiel_simulation(player1_würfel, player2_würfel, 1, Anzahl_Züge_pro_Spiel_max)
        Siege.append(Sieg)
    for i in range(int(Anzahl_wiederholungen_Partie/2)):
        Sieg = Spiel_simulation(player1_würfel, player2_würfel, 2, Anzahl_Züge_pro_Spiel_max)
        Siege.append(Sieg)
    print('Würfel 1 : ' + str(player1_würfel) + str(round(((Siege.count(1)/len(Siege)) * 100), 3)) + '% W Quote vs ' + 'Würfel 2: ' + str(player2_würfel) + str(round(Siege.count(2)/len(Siege) * 100, 3))+ '% W Quote')

