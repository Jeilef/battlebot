import random
import numpy as np

class kaempfer:
    def __init__(self, koerper, leben, flinkheit, ausweichen, initiative, waffe1, waffe2):
        self.koerper = koerper
        self.leben = leben
        self.flinkheit = flinkheit
        self.ausweichen = ausweichen
        self.intitiative = initiative
        self.hand1 = waffe1
        self.hand2 = waffe2
        self.waffen = None

    def ausruesten(self):
        self.waffen = np.genfromtxt("data/waffen.csv", delimiter=";", dtype=str, encoding="utf-8")
        print(len(self.waffen))
        for row in range(len(self.waffen)):
            if self.hand1 == self.waffen[row][0]:
                self.hand1 = self.waffen[row]
                break
            elif row == len(self.waffen)-1:
                self.hand1 = self.waffen[0]
                break
            elif self.hand1 != self.waffen[row][0]:
                self.hand1 = self.hand1
        for row in range(len(self.waffen)):
            if self.hand2 == self.waffen[row][0]:
                self.hand2 = self.waffen[row]
                break
            elif row == len(self.waffen) - 1:
                self.hand2 = self.waffen[0]
                break
            elif self.hand2 != self.waffen[row][0]:
                self.hand2 = self.hand2
        print(self.hand1, self.hand2)
        return(self.hand1,self.hand2)

    def angriff(self):
        w20 = random.randint(1, 20)
        w6h1 = 1 #random.randint(1, 6)
        w6h2 = random.randint(1, 6)
        angriffswert = self.koerper + int(self.hand1[7]) + int(self.hand2[7])
        if angriffswert >= w20:
            schaden = 0
            while w6h1 == 1:
                if w6h1 == 1:
                    w6h1 = random.randint(1, 6)
                    schaden = schaden + int(self.hand1[1])
                    print('+', self.hand1[1])
            schaden = schaden + int(self.hand1[w6h1])
            while w6h2 == 1:
                if w6h2 == 1:
                    w6h2 = random.randint(1, 6)
                    schaden = schaden + int(self.hand1[1])
                    print('+', self.hand1[1])
            schaden = schaden + int(self.hand1[w6h2])
            print(schaden, self.hand1[w6h1], self.hand2[w6h2])
        else:
            schaden = 0
            print(schaden)



k1 = kaempfer(10, 2, 2, 2, 2, 'Langschwert', 'Faust')
k1.ausruesten()
k1.angriff()