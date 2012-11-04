import random as r

class warprotocol(object):
    def attacksucceeded(self,attackintensity,defenseintensity):
        attacknum = attackintensity / (attackintensity + defenseintensity * 1.0)
        if (r.uniform(0,1.0)>= attacknum): return False
        return True
        
    def canattack(self,attacker,attackIntensity,attackedTerritoryID,numterritories,defender):
        if ( attackIntensity <= 0 or 
             attackIntensity > attacker.getSoldiers()  or
             attackedTerritoryID < 0 or 
             attackedTerritoryID > numterritories - 1 or 
             attacker == defender or
            ( attacker.isAbove(defender)==False or
              defender not in attacker.neighbors)) :
                return False          
        return True
    def adjustdefensiveintensity(self,intensity,defender):
        if ( intensity < 0 or intensity > defender.soldiers ):            
                return 0.0            
        return intensity
    def getSoldierModifier(self,succeeded):
        if (succeeded):
            return 4.0
        else:
            return 2.0
    def war(self,territories,rulers,period):
        
        for attacker in territories:
            attacker.ruler.attack()
            attackIntensity = attacker.getRuler().attackingSoldiers
            attackedTerritoryID = attacker.getRuler().attackedTerritoryID
            defender = territories[attackedTerritoryID]
            if self.canattack(attacker,attackIntensity,attackedTerritoryID,len(territories),defender):
                    defender.getRuler().defend(attacker, attackIntensity)
                    defenseIntensity = self.adjustdefensiveintensity(defender.getRuler().defendingSoldiers,defender)
                    attackSucceeded = self.attacksucceeded(attackIntensity,defenseIntensity)
                    attacker.soldiers += - attackIntensity / self.getSoldierModifier(attackSucceeded)
                    defender.soldiers += - defenseIntensity/ self.getSoldierModifier(not attackSucceeded)
                    
                    attacker.ruler.battleOutcome(period, attacker.key, attackIntensity, defender.key, defenseIntensity, attackSucceeded)
                    defender.ruler.battleOutcome(period, attacker.key, attackIntensity, defender.key, defenseIntensity, not attackSucceeded)
                    
                    if ( attackSucceeded ):
                        if ( defender.superior != None):
                            defender.superior.subordinates.remove(defender)
                        if ( attacker.isAbove(defender) ):
                            attacker.superior.subordinates.remove(attacker)
                            attacker.superior = None
                        defender.superior = attacker
                        attacker.subordinates.append(defender)
                        attacker.updateNeighbors()
                        defender.updateNeighbors()