class Map:
    def __init__(self) -> None:
        
        Matriz = []
        for i in range(100):
            Matriz = Matriz + [[0]*100]
        # Matriz contendo o mapa
        self.map = Matriz
        
    def atualiza_player(self, corpo, n=1):
        # Coloca o player no mapa da matriz
        if n == 0:
            for parte in corpo:
                self.map[parte[1]//10][parte[0]//10] = 0
        else:
            self.map[corpo[0][1]//10][corpo[0][0]//10] = n
            self.map[corpo[-1][1]//10][corpo[-1][0]//10] = 0

    def atualiza_fruta(self, x, y):
        # Coloca a fruta no mapa da matriz
        self.map[y][x] = 2

    def verificaCoord(self, corpo):
        if self.map[corpo[1]//10][corpo[0]//10] == 1: # morreu
            return 0
        if self.map[corpo[1]//10][corpo[0]//10] == 2: # comeu a fruta
            return 2
        else:
            return 1
        
