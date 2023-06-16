import socket

class Network:
    def __init__(self, porta):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Server que utiliza UDP por ser mais rápido, apropriado para um jogo multiplayer
        self.server = '192.168.0.101' #Colocar o IP
        self.port = porta
        self.addr = (self.server, self.port)
        self.n = self.send("n") # retorna a identidade do usuário no server
        # Exemplo, player numero 1 => player1.n = 1
        
    def rcv(self):
        # Função para receber do servidor
        try:
            pos, end = self.client.recvfrom(200)
            if pos and end:
                pos = pos.decode()
                return pos
            else:
                return False
        except socket.error as e:
        # Se não der certo 
            return False    

    def send(self, pos):
        # Função para mandar para o servidor
        try:
            self.client.sendto(str.encode(pos), self.addr)
            return self.rcv()
        except socket.error as e:
            return e