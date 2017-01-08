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
    playAgain = True
    turnCount = 0
    scorej1 = 0
    scorej2 = 0
    
    grids = [grid(), grid(), grid()]
    current_player = J1
    
    while playAgain == True:
        playAgain = False
        while grids[0].gameOver() == -1:
            listSLecture, lNUL1, lNUL2 = select.select(l + [s], [], [])
            for x in listSLecture:
                if x == s:
                    (newS, adr) = s.accept()
                    l.append(newS)
                    if joueur1 == None:
                        joueur1 = newS
                        joueur1.send(str.encode("Bonjour, vous etes le joueur 1\n"))
                    elif joueur2 ==None:
                        joueur2 = newS
                        joueur2.send(str.encode("Bonjour, vous etes le joueur 2\n"))
                        gameStart = True
                    else:
                        listSpec.append(newS)
                        newS.send(str.encode("Bonjour, deux joueurs jouent deja, vous etes spectateur\n"))
                        
            if joueur1 != None and joueur2 != None:
                if turnCount == 0:
                    grids[0].display()
                    joueur1.send(str.encode(grids[J1].displayInOneString()))
                    joueur1.send(str.encode("Joueur 1, quelle case allez-vous jouer ?\n"))
                if current_player == J1:
                    shot = 10
                    while shot < 0 or shot >= NB_CELLS:
                        shot = int(joueur1.recv(64))
                    print("Le joueur 1 a joué la case", int(shot))
                elif current_player == J2:
                    shot = 10
                    while shot < 0 or shot >= NB_CELLS:
                        shot = int(joueur2.recv(64))
                    print("Le joueur 2 a joué la case", int(shot))						
                if (grids[0].cells[shot] != EMPTY):
                    grids[current_player].cells[shot] = grids[0].cells[shot]
                else:
                    grids[current_player].cells[shot] = current_player
                    grids[0].play(current_player, shot)
                    current_player = current_player%2+1
                if current_player == J1:
                    joueur1.send(str.encode(grids[J1].displayInOneString()))
                    joueur1.send(str.encode("Joueur 1, quelle case allez-vous jouer ?\n"))
                else:
                    joueur2.send(str.encode(grids[J2].displayInOneString()))
                    joueur2.send(str.encode("Joueur 2, quelle case allez-vous jouer ?\n"))
                grids[0].display()
                for spec in listSpec:
                    spec.send(str.encode(grids[0].displayInOneString()))
                turnCount = turnCount +1
        print("Partie Terminee")
        joueur1.send(str.encode(grids[0].displayInOneString()))
        joueur2.send(str.encode(grids[0].displayInOneString()))
        if grids[0].gameOver() == J1:
            joueur1.send(str.encode("You WIN !\n"))
            joueur2.send(str.encode("You LOOSE !\n"))
            scorej1 = scorej1 + 1
        else:
            joueur1.send(str.encode("You LOOSE !\n"))
            joueur2.send(str.encode("You WIN !\n"))
            scorej2 = scorej2 + 1

        joueur1.send(str.encode("Voulez-vous rejouez?(y/n)\n"))
        answer = joueur1.recv(1)
        if answer == b'y':
            playAgain = True
            grids[0].resetGrids()
            grids[0].display()
            grids[J1].resetGrids()
            grids[J2].resetGrids()
            turnCount = 0
            current_player = J1

main()
