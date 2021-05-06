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
        for row in range(len(self.waffen)):                 # Ausrüstung der Waffe
            if self.hand1 == self.waffen[row][0]:
                self.hand1 = self.waffen[row]
                break
            elif row == len(self.waffen)-1:
                self.hand1 = self.waffen[1]
                break
            elif self.hand1 != self.waffen[row][0]:
                self.hand1 = self.hand1
        for row in range(len(self.waffen)):
            if self.hand2 == self.waffen[row][0]:
                self.hand2 = self.waffen[row]
                break
            elif row == len(self.waffen) - 1:
                self.hand2 = self.waffen[1]
                break
            elif self.hand2 != self.waffen[row][0]:
                self.hand2 = self.hand2
        hand = int(self.hand1[10]) + int(self.hand2[10])    # gucken ob man genug hände hat
        if hand > 2:
            self.hand1 = self.waffen[0]
            self.hand2 = self.waffen[0]
            print('Waffen auswahl nicht möglich')
        print(self.hand1, self.hand2)
        return(self.hand1,self.hand2)

    def angriff(self):
        w20 = random.randint(1, 20)
        w6h1 = 1 #random.randint(1, 6)
        w6h2 = 1 #random.randint(1, 6)
        angriffswert = self.koerper + int(self.hand1[7]) + int(self.hand2[7])
        if angriffswert >= w20:                                     # Ob der Angriff trifft
            schaden = 0
            while w6h1 == 1:                                        # krit Ermittlung Waffe1
                if w6h1 == 1:
                    w6h1 = random.randint(1, 6)
                    schaden = schaden + int(self.hand1[1])
                    print('+', self.hand1[1])
            schaden = schaden + int(self.hand1[w6h1])
            schaden1 = schaden
            while w6h2 == 1:                                        # krit Ermittlung Waffe2
                if w6h2 == 1:
                    w6h2 = random.randint(1, 6)
                    schaden = schaden + int(self.hand2[1])
                    print('+', self.hand2[1])
            schaden = schaden + int(self.hand2[w6h2])
            schaden2= schaden - schaden1
            print(schaden, schaden1, schaden2)
        else:
            schaden = 0
            print(schaden)

    def blocken(self):
        anzahl = int(self.hand1[8]) + int(self.hand2[8])
        blockwurf = []
        reduzierung = 0
        for wurf in range(0, anzahl):
            blockwurf.append(random.randint(1, 6))
            if blockwurf[wurf] <= 5:
                reduzierung = reduzierung + 1
                print(blockwurf,reduzierung)


    def ausweichen(self):
        for wurf in range(0, 6):
            ausweichwurf = random.randint(1, 6)
            if ausweichwurf == 6:
                gegnerschaden = 0
                print(gegnerschaden)
                break



k1 = kaempfer(20, 2, 2, 2, 2, 'Langschwert', '-')
k1.ausruesten()
k1.angriff()
k1.blocken()
k1.ausweichen()