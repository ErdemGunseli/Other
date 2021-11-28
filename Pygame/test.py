class Gateway(): # The parent class of snakes and ladders.

    def __init__(self, enterPos, exitPos): # Paramenters are the enter and exit positions, taken from a list.
        self.enterPos = enterPos
        self.exitPos = exitPos


class Snake(Gateway): # Child of gateways - doesn't need any specialised attributes and only exists for flexibility.

    def __init__(self, enterPos, exitPos):
        super().__init__(enterPos, exitPos)
       


class Ladder(Gateway): # Child of gateways - doesn't need any specialised attributes and only exists for flexibility.

    def __init__(self, enterPos, exitPos):
        super.__init__(enterPos, exitPos)
      
mysnake = Snake(100, 1)

