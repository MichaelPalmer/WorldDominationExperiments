
def checkforbadinput(input,resource):
    if resource == 0: return 0
    if input > resource: return resource
    return input


class territory(object):
    def __init__(self,id=None,name=None,peasantGrowth=None,foodGrowth=None,alpha=None):
        this.id = id
        this.peasantGrowth = farmsGrowth
        this.foodGrowth    = foodGrowth
        this.alpha         = alpha
        this.peasants      = 0
        this.food          = 0
        this.soldiers      = 0

    def produceSoldiers(self,food,peasants):
        food     = correctforbadinput(food,self.food)
        peasants = correctforbadinput(peasants,self.peasants)

        self.soldiers = self.soldiers + (self.food**alpha  * self.peasants **(1 - alpha) )
        self.peasants -= peasants;
        self.food     -= food;

    def grow(self):
        self.food     += self.foodGrowth
        self.peasants += slef.peasantGrowth

    def feedSoldiers(self):
        if self.soldiers <= self.food:
            self.food -= self.soldiers
        else:
            self.soldiers = self.food
            self.food     = 0


