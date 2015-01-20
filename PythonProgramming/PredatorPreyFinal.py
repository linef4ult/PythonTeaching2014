"""Predator-Prey Simulation
   four classes are defined: animal, predator, prey, and island
   where island is where the simulation is taking place,
   i.e. where the predator and prey interact (live).
   A list of predators and prey are instantiated, and
   then their breeding, eating, and dying are simulated.
"""
import random
import time
# import pylab


class Island(object):
    """Island
       n X n grid where zero value indicates not occupied."""

    def __init__(self, n, preyCnt=0, predatorCnt=0):
        '''Initialize grid to all 0's, then fill with animals
        '''
        # print n,preyCnt,predatorCnt
        self.gridSize = n
        self.grid = []
        for i in range(n):
            row = [0] * n  # row is a list of n zeros
            self.grid.append(row)
        self.initAnimals(preyCnt, predatorCnt)

    def initAnimals(self, preyCnt, predatorCnt):
        ''' Put some initial animals on the island
        '''
        cnt = 0
        # while loop continues until preyCnt unoccupied positions are found
        while cnt < preyCnt:
            x = random.randint(0, self.gridSize - 1)
            y = random.randint(0, self.gridSize - 1)
            if not self.animal(x, y):
                newPrey = Prey(island=self, x=x, y=y)
                cnt += 1
                self.register(newPrey)
        cnt = 0
        # same while loop but for predatorCnt
        while cnt < predatorCnt:
            x = random.randint(0, self.gridSize - 1)
            y = random.randint(0, self.gridSize - 1)
            if not self.animal(x, y):
                newPred = Predator(island=self, x=x, y=y)
                cnt += 1
                self.register(newPred)

    def clearAllMovedFlags(self):
        ''' Animals have a moved flag to indicated they moved this turn.
        Clear that so we can do the next turn
        '''
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                if self.grid[x][y]:
                    self.grid[x][y].clearMovedFlag()

    def size(self):
        '''Return size of the island: one dimension.
        '''
        return self.gridSize

    def register(self, animal):
        '''Register animal with island, i.e. put it at the
        animal's coordinates
        '''
        x = animal.x
        y = animal.y
        self.grid[x][y] = animal

    def remove(self, animal):
        '''Remove animal from island.'''
        x = animal.x
        y = animal.y
        self.grid[x][y] = 0

    def animal(self, x, y):
        '''Return animal at location (x,y)'''
        if 0 <= x < self.gridSize and 0 <= y < self.gridSize:
            return self.grid[x][y]
        else:
            return -1  # outside island boundary

    def __str__(self):
        '''String representation for printing.
           (0,0) will be in the lower left corner.
        '''
        s = ""
        for j in range(self.gridSize - 1, -1, -1):  # print row size-1 first
            for i in range(self.gridSize):  # each row starts at 0
                if not self.grid[i][j]:
                    # print a '.' for an empty space
                    s += "%-2s" % '.' + "  "
                else:
                    s += "%-2s" % (str(self.grid[i][j])) + "  "
            s += "\n"
        return s

    def preyCount(self):
        ''' count all the prey on the island'''
        cnt = 0
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                animal = self.animal(x, y)
                if animal:
                    if isinstance(animal, Prey):
                        cnt += 1
        return cnt

    def predatorCount(self):
        ''' count all the predators on the island'''
        cnt = 0
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                animal = self.animal(x, y)
                if animal:
                    if isinstance(animal, Predator):
                        cnt += 1
        return cnt


class Animal(object):
    def __init__(self, island, x=0, y=0, s="A"):
        '''Initialize the animal's and their positions
        '''
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def position(self):
        '''Return coordinates of current position.
        '''
        return self.x, self.y

    def __str__(self):
        return self.name

    def checkGrid(self, typeLookingFor=int):
        ''' Look in the 8 directions from the animal's location
        and return the first location that presently has an object
        of the specified type. Return 0 if no such location exists
        '''
        # neighbor offsets
        offset = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        result = 0
        for i in range(len(offset)):
            x = self.x + offset[i][0]  # neighboring coordinates
            y = self.y + offset[i][1]
            if not 0 <= x < self.island.size() or \
                    not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x, y)) == typeLookingFor:
                result = (x, y)
                break
        return result

    def move(self):
        '''Move to an open, neighboring position '''
        if not self.moved:
            location = self.checkGrid(int)
            if location:
                # print 'Move, %s, from %d,%d to %d,%d'% \
                #       (type(self),self.x,self.y,location[0],location[1])
                self.island.remove(self)  # remove from current spot
                self.x = location[0]  # new coordinates
                self.y = location[1]
                self.island.register(self)  # register new coordinates
                self.moved = True

    def breed(self):
        ''' Breed a new Animal.If there is room in one of the 8 locations
        place the new Prey there. Otherwise you have to wait.
        '''
        if self.breedClock <= 0:
            location = self.checkGrid(int)
            if location:
                self.breedClock = self.breedTime
                # print 'Breeding Prey %d,%d'%(self.x,self.y)
                theClass = self.__class__
                newAnimal = theClass(self.island, x=location[0], y=location[1])
                self.island.register(newAnimal)

    def clearMovedFlag(self):
        self.moved = False


class Prey(Animal):
    def __init__(self, island, x=0, y=0, s="O"):
        Animal.__init__(self, island, x, y, s)
        self.breedClock = self.breedTime
        # print 'Init Prey %d,%d, breed:%d'%(self.x, self.y,self.breedClock)

    def clockTick(self):
        '''Prey only updates its local breed clock
        '''
        self.breedClock -= 1
        # print 'Tick Prey %d,%d, breed:%d'%(self.x,self.y,self.breedClock)


class Predator(Animal):
    def __init__(self, island, x=0, y=0, s="X"):
        Animal.__init__(self, island, x, y, s)
        self.starveClock = self.starveTime
        self.breedClock = self.breedTime
        # print 'Init Predator %d,%d, starve:%d, breed:%d'% \
        #       (self.x,self.y,self.starveClock,self.breedClock)

    def clockTick(self):
        ''' Predator updates both breeding and starving
        '''
        self.breedClock -= 1
        self.starveClock -= 1
        # print 'Tick, Predator at %d,%d starve:%d, breed:%d'% \
        #       (self.x,self.y,self.starveClock,self.breedClock)
        if self.starveClock <= 0:
            # print 'Death, Predator at %d,%d' % (self.x,self.y)
            self.island.remove(self)

    def eat(self):
        ''' Predator looks for one of the 8 locations with Prey. If found
        moves to that location, updates the starve clock, removes the Prey
        '''
        if not self.moved:
            location = self.checkGrid(Prey)
            if location:
                # print 'Eating: pred at %d,%d, prey at %d,%d'% \
                #       (self.x,self.y,location[0],location[1])
                self.island.remove(self.island.animal(location[0], location[1]))
                self.island.remove(self)
                self.x = location[0]
                self.y = location[1]
                self.island.register(self)
                self.starveClock = self.starveTime
                self.moved = True


###########################################
def main(predBreed=6, predStarve=3, predInit=10, preyBreed=3, preyInit=50, \
         size=10, ticks=300):
    ''' main simulation. Sets defaults, runs event loop, plots at the end
    '''
    # initialization values
    Predator.breedTime = predBreed
    Predator.starveTime = predStarve
    Prey.breedTime = preyBreed

    # for graphing
    predList = []
    preyList = []

    # make an island
    isle = Island(size, preyInit, predInit)
    print(isle)

    # event loop.
    # For all the ticks, for every x,y location.
    # If there is an animal there, try eat, move, breed and clockTick
    for i in range(ticks):
        # important to clear all the moved flags!
        isle.clearAllMovedFlags()
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)
                if animal:
                    if isinstance(animal, Predator):
                        animal.eat()
                    animal.move()
                    animal.breed()
                    animal.clockTick()

        # record info for display, plotting
        preyCnt = isle.preyCount()
        predCnt = isle.predatorCount()
        if preyCnt == 0:
            print('Lost the Prey population. Quiting.')
            break
        if predCnt == 0:
            print('Lost the Predator population. Quitting')
            break
        preyList.append(preyCnt)
        predList.append(predCnt)
        # print out every 10th cycle, see what's going on
        if not i % 10:
            print(preyCnt, predCnt)
            # print the island, hold at the end of each cycle to get a look
            # print '*'*20
            # print isle
            # ans = raw_input("Return to continue")


    # pylab.plot(predList)
    # pylab.plot(preyList)
    # pylab.show()

if __name__ == "__main__":
    '''When the Python interpreter reads a source file, it executes all of the code found in it. Before
    executing the code, it will define a few special variables. For example, if the python interpreter
    is running that module (the source file) as the main program, it sets the special __name__ variable
    to have a value "__main__". If this file is being imported from another module, __name__ will be set
    to a different value. For example, this means that you can import to IDLE and run functions separately
    which may be useful for testing'''
    main()
