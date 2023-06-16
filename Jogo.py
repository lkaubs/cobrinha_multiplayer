################################################################
# Main file do jogo, para funcionar corretamente, 
# inicie o server_principal, Server1, Server2 e Server3 
# antes de dar boot no jogo.
################################################################

import pygame
from network import Network
import random
from map import Map
import time

################################################################

largura = 1000 
altura = 1000
a = Map()
# setando o size da tela do jogo e o mapa das matrizes]
################################################################
# Iniciando o jogo

win = pygame.display.set_mode(size=(largura, altura))
pygame.display.set_caption("Cobrinha Multiplayer")
clock = pygame.time.Clock()
pygame.font.init()

################################################################

class Player():
    def __init__(self, x, y, width, height, color) -> None:
        self.corpo = [(x, y), (x-10, y), (x-20, y), (x-30, y), (x-40, y)]
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.tam = 4
        self.pont = 0
        self.vel = 10
        self.vivo = 1
        self.comeu = False

    def draw(self, win):
        # função para desenhar cada parte do corpo da cobrinha
        for c in range(len(self.corpo)-1):
            pygame.draw.rect(win, self.color, (self.corpo[c][0], self.corpo[c][1], self.width, self.height))

    def move(self, direcao_antes):
        # função para mexer o player
        if self.vivo:
            direcao = direcao_antes
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                direcao = 1

            elif keys[pygame.K_s]:
                direcao = 0

            elif keys[pygame.K_d]:
                direcao = 2

            elif keys[pygame.K_a]:
                direcao = 3
            
            if direcao_antes != 0 and direcao == 1: # teste para ver se está tentando voltar e para continuar indo na mesma direção
                if self.corpo[0][1] - self.vel >= 0: # verifica colizão
                    nova_pos = (self.corpo[0][0], self.corpo[0][1]-self.vel)
                    self.verificaPos(nova_pos)
                    if not self.comeu:
                        for c in range(0, len(self.corpo)):
                            if c != 0:
                                self.corpo[-c] = self.corpo[-c-1]
                        self.corpo[0] = nova_pos
                    else:
                        self.corpo.insert(0, nova_pos)
                    self.atualizaPos()
                return direcao
            
            if direcao_antes != 1 and direcao == 0:
                if self.corpo[0][1] + self.vel <= altura-self.height:
                    nova_pos = (self.corpo[0][0], self.corpo[0][1]+self.vel)
                    self.verificaPos(nova_pos)
                    if not self.comeu:
                        for c in range(0, len(self.corpo)):
                            if c != 0:
                                self.corpo[-c] = self.corpo[-c-1]
                        self.corpo[0] = nova_pos
                    else:
                        self.corpo.insert(0, nova_pos)
                    self.atualizaPos()
                return direcao
        
            if direcao_antes != 3 and direcao == 2:
                if self.corpo[0][0] + self.vel <= largura-self.width:
                    nova_pos = (self.corpo[0][0]+self.vel, self.corpo[0][1])
                    self.verificaPos(nova_pos)
                    if not self.comeu:
                        for c in range(0, len(self.corpo)):
                            if c != 0:
                                self.corpo[-c] = self.corpo[-c-1] # jeito de mexer que torna parecido com a cobrinha
                        self.corpo[0] = nova_pos
                    else:
                        self.corpo.insert(0, nova_pos)
                    self.atualizaPos()
                return direcao

            if direcao_antes != 2 and direcao == 3:
                if self.corpo[0][0] - self.vel >= 0:
                    nova_pos = (self.corpo[0][0]-self.vel, self.corpo[0][1])
                    self.verificaPos(nova_pos)
                    if not self.comeu and self.vivo:
                        for c in range(0, len(self.corpo)):
                            if c != 0:
                                self.corpo[-c] = self.corpo[-c-1]
                        self.corpo[0] = nova_pos
                    else:
                        self.corpo.insert(0, nova_pos)
                    self.atualizaPos()
                return direcao
            return direcao_antes
        else:
            pass
    
    def verificaPos(self, nova_pos):
        flag = a.verificaCoord(nova_pos)
        if flag == 0:
            self.vivo = 0

        elif flag == 2:
            self.tam += 1
            self.pont += 1
            self.comeu = True

        elif flag == 1:
            pass

    def atualizaPos(self, corpo=None):
        if corpo:
            novo_corpo = []
            if '0' == corpo[0]:
                a.atualiza_player(self.corpo, 0)
                self.vivo == 0
            try:
                for parte in corpo.split('/'):
                    novo_corpo.append((int(parte.split()[0]), int(parte.split()[1])))
            except:
                self.corpo = novo_corpo
                pass
        if self.vivo:
            a.atualiza_player(self.corpo)
        else:
            a.atualiza_player(self.corpo, 0)
            
    def pos(self):
        # Função para retornar a posição das partes do corpo do jogador para mandar para o server
        resp = ''
        for parte in self.corpo:
            resp += str(parte[0])+' '+str(parte[1])+'/'
        return resp

    
##############################################################################################

class Fruta():
    # Sistema de pontuação do jogo
    def __init__(self, net):
        self.coord = net.send("Fruta")
        self.x = int(self.coord.split()[0])
        self.y = int(self.coord.split()[1])
        self.altura_largura = 10
        self.rect = (self.x*10, self.y*10, self.altura_largura, self.altura_largura)
        a.atualiza_fruta(self.x, self.y)

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.rect)

#############################################################################################

class Botao:
    # Botão para escolher o server e afins.
    def __init__(self, texto, x, y, cor, server):
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.largura = 350
        self.altura = 150
        self.n = '0'
        self.server = server

    def draw(self, win):
        pygame.draw.rect(win, self.cor, (self.x, self.y, self.largura, self.altura))
        font = pygame.font.SysFont("comicsans", 45)
        texto = font.render(self.atualiza_botao(), 1, (255, 255, 255))
        win.blit(texto, (self.x + round(self.largura/2) - round(texto.get_width()/2), self.y + round(self.altura/2) - round(texto.get_height()/2)))
        pygame.display.update()
        
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.largura and self.y <= y1 <= self.y + self.altura:
            return True
        else:
            return False
        
    def atualiza_botao(self, n=None):
        if n:
            self.n = n
        return self.texto+(f'{self.n}/4')
    
#######################################################################################

def redrawWindow(win, lista_jogadores, fruta, net):
    # função para atualizar os players na tela
    win.fill((155, 155, 155))
    for player in lista_jogadores:
        # morreu
        if player.vivo:
            player.draw(win)
        if player.comeu:
            net.send('Comeu')
            player.comeu = False
    fruta = Fruta(net)
    fruta.draw(win)
    pygame.display.update()
    return fruta

def menu():
    botoes = [Botao("Sessão 1 = ", 50, 700, (0, 0, 0), 2020), Botao("Sessão 2 = ", 550, 700, (255, 0, 0), 2021), Botao("Sessão 3 = ", 350, 200, (0, 255, 0), 2022)]
    n = Network(2019)
    run = True
    win.fill((155, 155, 155))
    while run:
        # Verifica o estado dos servers toda hora para mudar o número de jogadores
        estado_servers = n.n
        estado_servers = estado_servers.split(';')
        for c in range(len(estado_servers)-1):
            servers = estado_servers[c].split()
            botoes[c].atualiza_botao(servers[-1])
        for botao in botoes:
            botao.draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for botao in botoes:
                    if botao.click(pos):
                        porta = botao.server
                        run = False
    # Leva o jogador para a sessão que ele escolheu 
    return sessao(porta)

def sessao(porta):
    run = True
    pygame.display.update()
    net2 = Network(porta)
    num = net2.n
    botao = None
    while run:
        # Verifica se o jogador é o player número 1
        if int(num) == 1:
            botao = Botao("Iniciar a partida ", 325, 425, (255, 100, 100), porta)
            botao.atualiza_botao(net2.send('qtd_jogadores?'))
            win.fill((155, 155, 155))
            botao.draw(win)
        else:
            q = Botao("Espere o Líder iniciar a partida ", 325, 425, (155, 155, 155), porta)
            q.atualiza_botao(net2.send('qtd_jogadores?'))
            win.fill((155, 155, 155))
            q.draw(win)
        # Espera pelo jogador 1 iniciar a partida
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if botao:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if botao.click(pos):
                        try: 
                            if int(net2.send('1')) == 1:
                                run = False
                        except:
                            pass
            else:
                try:
                    if int(net2.send('1')) == 1:
                        run = False
                except:
                    pass
    return main(net2)

def main(net):
    # Inicia o jogo de fato
    run = True
    win.fill((155, 155, 155))
    pygame.display.update()
    x_inicial = random.randrange(0, (largura//10))
    y_inicial = random.randrange(0, (altura//10))
    fruta = Fruta(net)
    p = Player(x_inicial*10, y_inicial*10, 10, 10, (0, 0, 0))
    p2 = Player(1010, 1010, 10, 10, (123, 222, 0))
    p3 = Player(1010, 1010, 10, 10, (231, 200, 33))
    p4 = Player(1010, 1010, 10, 10, (120, 0, 255))
    lista_jogadores = [p, p2, p3, p4]
    num = net.n
    direcao = 3
    while run:
        clock.tick(60)
        time.sleep(0.07)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        direcao = p.move(direcao)
        try:
            # Manda a posição do player para o server e recebe a resposta do server
            if p.vivo:
                resp = net.send(p.pos())
            else:
                resp = net.send('Morri')
            # Na resposta estão as posições dos players restantes que serão distribuidas da seguinte forma
            for pos in resp.split(';'):
                if int(num) < 3:
                    if int(pos.split('-')[1]) == 1:
                        p4.atualizaPos(pos.split('-')[0])
                    elif int(pos.split('-')[1]) == 2:
                        p4.atualizaPos(pos.split('-')[0])
                    elif int(pos.split('-')[1]) == 3:
                        p3.atualizaPos(pos.split('-')[0])
                    elif int(pos.split('-')[1]) == 4:
                        p2.atualizaPos(pos.split('-')[0])
                else:
                    if int(pos.split('-')[1]) == 1:
                        p4.atualizaPos(pos.split('-')[0])
                    elif int(pos.split('-')[1]) == 2:
                        p3.atualizaPos(pos.split('-')[0])
                    elif int(pos.split('-')[1]) == 3:
                        p2.atualizaPos(pos.split('-')[0])
                    elif int(pos.split('-')[1]) == 4:
                        p2.atualizaPos(pos.split('-')[0])
        except:
            pass
        # atualiza na tela essas posições
        fruta = redrawWindow(win, lista_jogadores,fruta, net)
# Inicia tudo
menu()
