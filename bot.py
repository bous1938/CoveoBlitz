from game_message import Tick, Action, Spawn, Sail, Dock, Anchor, directions, Position
import math
class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.CloserPort = None       
    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        self.tick = tick
        self.DirectionChoisi = 'N'
        self.actionChoisi = None
        self.HauteurActu = tick.tideSchedule[0]    
        #On Spawn au premier tour
        self.startPortIndex = 0 
        if tick.currentLocation is None:
            self.printDebugInfo(Spawn(tick.map.ports[self.startPortIndex]))
            return Spawn(tick.map.ports[self.startPortIndex])

        #On Trouve le port le plus proche
        self.findCloserPort()

        #Si le port le plus proche est à une distance de 0, on ancre.
        if self.calculDistance(self.CloserPort) == 0:
            self.CloserPort = None
            self.printDebugInfo(Dock)
            return Dock()

        #Sinon on choisi la prochaine direction
        self.chooseBestDirection()  
        self.printDebugInfo(Sail(self.DirectionChoisi))  

        Ymax  = self.CloserPort.row
        Ymin = self.tick.currentLocation.row
        if Ymax > Ymin:
            tmp = Ymax
            Ymax = Ymin
            Ymin = tmp

        Xmin = self.CloserPort.column
        Xmax = self.CloserPort.column
        if Xmax > Xmin:
            tmp = Xmax
            Xmax = Xmin
            Xmin = tmp

        if (Xmax - Xmin) < 5: 
            Xmax = Xmax + 5
            Xmin = Xmin - 5
       
        if (Ymax - Ymin) < 5: 
            Ymax = Ymax + 5
            Ymin = Ymin - 5
       

        tmpArrayTopo = []
 
        for y in range(Ymin,Ymax):
            row = []
            for x in range(Xmin, Xmax):
                row.append(self.tick.map.topology[y][x])
            tmpArrayTopo.append(row)


        print(tmpArrayTopo)




        


        return Sail(self.DirectionChoisi)
    def findBestPath(self, matrice, depart, cible):
        s = None


    def findCloserPort(self):
        if self.CloserPort is None : 
            closerDist = 0

            #On passe sur tous les ports de la map
            for i in range(len(self.tick.map.ports)):
                if i in self.tick.visitedPortIndices: continue # Si un port est visité on l'ignore

                # Si on a pas encore trouvé le port le plus proche, on prend le port actuel par défaut
                if self.CloserPort is None:
                    self.CloserPort = self.tick.map.ports[i]
                    closerDist =  self.calculDistance(self.tick.map.ports[i])
                    continue
                
                tmp = self.calculDistance(self.tick.map.ports[i])
                # Si on trouve un port plus proche, on le cible
                if closerDist > tmp: 
                    self.CloserPort = self.tick.map.ports[i]
                    closerDist = tmp
            
            #Si on a passé sur tous les ports, on retourne au port d'origine
            if self.CloserPort is None:
                self.CloserPort = self.tick.map.ports[self.startPortIndex]




    def calculDistance(self, port: Position):
        return math.sqrt((self.tick.currentLocation.column - port.column)**2 + (self.tick.currentLocation.row - port.row)**2)



    def printDebugInfo(self,ActionChoisi:Action):
        print("Action choisi : " + str(ActionChoisi))
        print("Direction choisi : "  + str(self.DirectionChoisi))
        
        xActu = -1
        yActu = -1
        if not self.tick.currentLocation is None:
            xActu = self.tick.currentLocation.column
            yActu = self.tick.currentLocation.row
        print("Position Actuelle : X: " + str(xActu) + "  Y:" + str(yActu))

        xPortCible = -1
        yPortCible = -1
        if not self.CloserPort is None:
            xPortCible = self.CloserPort.column
            yPortCible = self.CloserPort.row
        print("Position ciblé : X: " + str(xPortCible) + "  Y:" + str(yPortCible))
        print("Port Visité : " + str(self.tick.visitedPortIndices))
        print("Niveau d'eau actuel : " + str(self.HauteurActu))

    def CalculNextPost(self):
        nextPos = self.tick.currentLocation
        if self.DirectionChoisi == "N":
            nextPos.row -= 1
        elif self.DirectionChoisi == "S":
            nextPos.row += 1
        elif self.DirectionChoisi == "E":
            nextPos.column += 1
        elif self.DirectionChoisi == "W":
            nextPos.column -= 1
        elif self.DirectionChoisi == "NE":
            nextPos.row -= 1 
            nextPos.column += 1
        elif self.DirectionChoisi == "NW":
            nextPos.row -= 1 
            nextPos.column -= 1
        elif self.DirectionChoisi == "SE":
            nextPos.row += 1 
            nextPos.column += 1
        elif self.DirectionChoisi == "SW":
            nextPos.row += 1 
            nextPos.column -= 1
        return nextPos




    def chooseBestDirection(self):
                # Choix du la direction selon le port Choisi.
        DeltaY = self.tick.currentLocation.row - self.CloserPort.row
        DeltaX = self.CloserPort.column - self.tick.currentLocation.column
        Pente = 3
        if DeltaX > 0 or DeltaX <0: Pente= DeltaY/DeltaX
        PenteAbs = Pente

        Direction = 'N'
        if PenteAbs < 0: PenteAbs = -PenteAbs


        if PenteAbs > 2.41:
            if DeltaY > 0 :
                Direction = 'N'
            else:
                Direction = 'S'
        elif PenteAbs < 0.41: 
            if DeltaX > 0 :
                Direction = 'E'
            else:
                Direction = 'W'   
        else:
            if DeltaY > 0 :
                if Pente > 0:
                    Direction = 'NE'
                else:
                    Direction = 'NW'
            else:
                if Pente > 0:
                    Direction = 'SW'
                else:
                    Direction = 'SE'
        self.DirectionChoisi = Direction
        return Direction