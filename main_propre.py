#!/usr/bin/python3

from grid import *
import  random
import socket
import select

def main():
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 7777))
    s.listen(1)
    
    l = []
    l.append(s)
    
    joueur1 = None
    joueur2 = None
    listSpec = []
    gameStart = False
    
    grids = [grid(), grid(), grid()]
    current_player = J1

    while grids[0].gameOver() == -1:
        listSLecture, lNUL1, lNUL2 = select.select(l + [s], [], [])
        print("test4")
        for x in listSLecture:
            print("test2")
            if x == s:
                print("test3")
                (newS, adr) = s.accept()
                l.append(newS)
                if joueur1 == None:
                    joueur1 = newS
                    joueur1.send(b"Bonjour, vous etes le joueur 1\n")
                elif joueur2 ==None:
                    joueur2 = newS
                    joueur2.send(b"Bonjour, vous etes le joueur 2\n")
                    gameStart = True
                    joueur1.send(bytearray(grids[J1].displayInOneString(), 'utf8'))
                    joueur1.send(b"Joueur 1, quelle case allez-vous jouer ?\n")
                else:
                    listSpec.append(newS)
                    newS.send(b"Bonjour, deux joueurs jouent deja, vous etes spectateur\n")
                    
            if joueur1 != None and joueur2 != None:
                print("Debut boucle")
                grids[0].display()
                if current_player == J1:
                    shot = 10
                    while shot < 0 or shot >= NB_CELLS:
                        #joueur1.send(b"Joueur 1, quelle case allez-vous jouer ?\n")
                        shot = int(joueur1.recv(10))
                    print("Le joueur 1 a joué la case", int(shot))
                elif current_player == J2:
                    shot = 10
                    while shot < 0 or shot >= NB_CELLS:
                        #joueur2.send(b"Joueur 2, quelle case allez-vous jouer ?\n")
                        shot = int(joueur2.recv(10))
                    print("Le joueur 2 a joué la case", int(shot))						
                if (grids[0].cells[shot] != EMPTY):
                    grids[current_player].cells[shot] = grids[0].cells[shot]
                else:
                    grids[current_player].cells[shot] = current_player
                    grids[0].play(current_player, shot)
                    current_player = current_player%2+1
                if current_player == J1:
                    joueur1.send(bytearray(grids[J1].displayInOneString(), 'utf8'))
                    joueur1.send(b"Joueur 1, quelle case allez-vous jouer ?\n")
                else:
                    joueur2.send(bytearray(grids[J2].displayInOneString(), 'utf8'))
                    joueur2.send(b"Joueur 2, quelle case allez-vous jouer ?\n")
                grids[0].display()
                for spec in listSpec:
                    spec.send(bytearray(grids[0].displayInOneString(), 'utf8'))
    print("game over")
    joueur1.send(bytearray(grids[0].displayInOneString(), 'utf8'))
    joueur2.send(bytearray(grids[0].displayInOneString(), 'utf8'))
    if grids[0].gameOver() == J1:
        joueur1.send(b"You WIN !\n")
        joueur2.send(b"You LOOSE !\n")
    else:
        joueur1.send(b"You LOOSE !\n")
        joueur2.send(b"You WIN !\n")


main()
