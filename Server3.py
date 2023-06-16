import socket
import pygame
import random
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nome_servidor = socket.gethostname()
server = '192.168.0.101'
porta = 2022
clock = pygame.time.Clock()
try:
    s.bind((server, porta))
except socket.error as e:
    print(e)
print("Server iniciado")
lista_jogadores = {}
pos_cada = {}
n = 0
iniciado = False
x = random.randrange(0, 100)
y = random.randrange(0, 100)
while True:
    clock.tick(60)
    try:
        pos, end = s.recvfrom(200)
        resp = ''
        # se existe mensagem
        if end and pos:
            # se a msg é do server principal
            if end == ('192.168.0.101', 2019):
                pass
            else:
                if end not in lista_jogadores.keys() and not iniciado:
                    n += 1
                    lista_jogadores[end] = n
                    s.sendto(str(n).encode(), end)
                elif end in lista_jogadores.keys():
                    if pos.decode() == 'n':
                        s.sendto(str(lista_jogadores[end]).encode(), end)
                    elif pos.decode() == 'qtd_jogadores?':
                        s.sendto(str(n).encode(), end)
                    elif pos.decode() == 'Fruta':
                        resp = str(x)+' '+str(y)
                        s.sendto(resp.encode(), end)
                    elif pos.decode() == "Comeu":
                        x = random.randrange(0, 100)
                        y = random.randrange(0, 100)
                        s.sendto('Ok'.encode(), end)
                    elif pos.decode() == '1':
                        if iniciado:
                            s.sendto(pos, end)
                        else:
                            if lista_jogadores[end] == 1:
                                s.sendto(pos, end)
                                iniciado = True
                            else:
                                s.sendto('0'.encode(), end)
                    else:
                        if iniciado:
                            for ende in lista_jogadores.keys():
                                if end == ende:
                                    if pos.decode() == "Morri":
                                        pos_cada[lista_jogadores[end]] = '0'
                                    else:
                                        pos_cada[lista_jogadores[end]] = pos.decode()
                                else:
                                    try:    
                                        resp += pos_cada[lista_jogadores[ende]]+'-'+str(lista_jogadores[ende])+';'
                                    except:
                                        pass
                            print(lista_jogadores)
                            print(pos_cada)
                            print(resp)
                            s.sendto(resp.encode(), end)
                else:
                    s.sendto('Partida indisponível'.encode(), end)

                s.sendto(str(n).encode(), ('192.168.0.101', 2019))
    except socket.error as e:
        print(e)
        break