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
        if tick.currentLocation is None:
            return Spawn(tick.map.ports[0])
        
        # Choix du prochain port (On prend le plus proche)
        if not self.CloserPort is None: 
            if self.calculDistance(self.CloserPort) == 0:
                self.CloserPort = None
                self.printDebugInfo()  
                return Dock()

        if self.CloserPort is None : 
            self.CloserPort = None
            closerDist = 0
            for i in range(len(tick.map.ports)):
                if i in tick.visitedPortIndices: continue 
                if self.CloserPort is None:
                    self.CloserPort = tick.map.ports[i]
                    closerDist =  self.calculDistance(tick.map.ports[i])

                tmp = self.calculDistance(tick.map.ports[i])
                if tmp == 0 : 
                    self.CloserPort = None
                    self.printDebugInfo()     
                    return Dock()

                if closerDist > tmp: 
                    self.CloserPort = tick.map.ports[i]
                    closerDist = tmp


        self.chooseBestDirection()  


        self.printDebugInfo()      
        return Sail(self.DirectionChoisi)


    def calculDistance(self, port: Position):
        return math.sqrt((self.tick.currentLocation.column - port.column)**2 + (self.tick.currentLocation.row - port.row)**2)



    def printDebugInfo(self):
        print("Direction choisi : "  + str(self.DirectionChoisi))
        print("Position Actuelle : X: " + str(self.tick.currentLocation.column) + "  Y:" + str(self.tick.currentLocation.row))
        xPortCible = -1
        yPortCible = -1
        if not self.CloserPort is None:
            xPortCible = self.CloserPort.column
            yPortCible = self.CloserPort.row
        print("Position ciblé : X: " + str(xPortCible) + "  Y:" + str(yPortCible))
        print("Port Visité : " + str(self.tick.visitedPortIndices))


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