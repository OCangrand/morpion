#!/usr/bin/python3

from grid import *
import  random
import socket
import select

def main():
    grids = [grid(), grid(), grid()]
    current_player = J1
    


    l = []

    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 7777))
    s.listen(1)

    while True:
        listSLecture, lNUL1, lNUL2 = select.select(l + [s], [], [])
        for x in listSLecture:
            if x == s:
                (newS, adr) = s.accept()
                l.append(newS)
                if len(l)==2:
                    joueur1 = l[0]
                    joueur2 = l[1]
                    joueur1.send(b"Bonjour, vous etes le joueur 1\n")
                    joueur2.send(b"Bonjour, vous etes le joueur 2\n")
                    print("Les deux joueurs sont arrivés, démarrage du jeu.")
                    grids[0].display()
                    joueur1.send(bytearray(grids[J1].displayInOneString(), 'utf8'))
            
                    while grids[0].gameOver() == -1:
                        if current_player == J1:
                            shot = 10
                            while shot < 0 or shot >= NB_CELLS:
                                joueur1.send(b"Joueur 1, quelle case allez-vous jouer ?")
                                shot = int(joueur1.recv(10))
                            print("Le joueur 1 a joué la case", int(shot))
                        elif current_player == J2:
                            shot = 10
                            while shot < 0 or shot >= NB_CELLS:
                                joueur2.send(b"Joueur 2, quelle case allez-vous jouer ?")
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
                        else:
                            joueur2.send(bytearray(grids[J2].displayInOneString(), 'utf8'))
                        grids[0].display()
                    print("game over")
                    joueur1.send(bytearray(grids[0].displayInOneString(), 'utf8'))
                    joueur2.send(bytearray(grids[0].displayInOneString(), 'utf8'))
                    if grids[0].gameOver() == J1:
                        joueur1.send(b"You WIN !")
                        joueur2.send(b"You LOOSE !")
                    else:
                        joueur1.send(b"You LOOSE !")
                        joueur2.send(b"You WIN !")


main()
