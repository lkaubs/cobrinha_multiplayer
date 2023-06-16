import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nome_servidor = socket.gethostname()
server = '192.168.0.101'
porta = 2019

try:
    s.bind((server, porta))
except socket.error as e:
    print(e)
print("Server iniciado")

lista_servers = {
    ('192.168.0.101', 2020): 0,
    ('192.168.0.101', 2021): 0,
    ('192.168.0.101', 2022): 0
}
while True:
    try:
        pos, end = s.recvfrom(2000)
        resp = ''
        if end and pos:
            for ende in lista_servers.keys():
                # sabe-se que é uma mensagem de um jogador
                if end != ende:
                    resp += str(ende)+' '+str(lista_servers[ende])+';'
                # mensagem de um servidor
                else:
                    lista_servers[end] = int(pos.decode())
                    resp = None
                    break
            if resp:
                s.sendto(resp.encode(), end)
        else:
            for ende in lista_servers.keys():
                s.sendto('n'.encode, ende)
    except socket.error as e:
        print(e)