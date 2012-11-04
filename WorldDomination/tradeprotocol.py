FOOD     = 1
PEASANTS = 2
SOLDIERS = 3

PARTNERID     = 0
GOODWANTED    = 1
WANTEDAMOUNT  = 2
OFFEREDGOOD   = 3
OFFEREDAMOUNT = 4



FOODNAME     = "food"
PEASANTSNAME = "peasants"
SOLDIERSNAME = "soldiers"

TRADELOOKUP = { (FOOD,PEASANTS):(FOODNAME,PEASANTSNAME),
                (FOOD,SOLDIERS):(FOODNAME,SOLDIERSNAME),
                (PEASANTS,FOOD):(PEASANTSNAME,FOODNAME),
                (PEASANTS,SOLDIERS):(PEASANTSNAME,SOLDIERSNAME),
                (SOLDIERS,FOOD):(SOLDIERSNAME,FOODNAME),
                (SOLDIERS,PEASANTS):(SOLDIERSNAME,PEASANTSNAME)}

class tradeprotocol(object):
    def cantrade(self,tradeId,territories,trader):
        if tradeId >= 0 and tradeId < len(territories):
            if trader != territories[tradeId]:
                if ((territories[tradeId].rulertype == trader.rulertype) or (trader in territories[tradeId].neighbors)): 
                    return True
        return False
    def legaltrade(self,trader,partner,tradedata):
        if ((tradedata[WANTEDAMOUNT]>=0) and (tradedata[OFFEREDAMOUNT]>=0)):
            if tradedata[GOODWANTED] != tradedata[OFFEREDGOOD]:
                lookup = (tradedata[GOODWANTED],tradedata[OFFEREDGOOD])
                if (TRADELOOKUP.has_key(lookup)):
                    tradermethod,partnermethod = TRADELOOKUP[lookup]
                    if ((tradedata[OFFEREDAMOUNT] <= trader.__getattribute__(tradermethod)) and (tradedata[WANTEDAMOUNT]  <= partner.__getattribute__(partnermethod))):
                        return True
        return False
    def trade(self,territories,rulers,period):
        for trader in territories:
            trader.ruler.trade()
            tradedata = list(trader.ruler.tradedata)
            
            if self.cantrade(tradedata[PARTNERID],territories,trader):
                partner = territories[tradedata[PARTNERID]] 
                
                if self.legaltrade(trader,partner,tradedata):
                    partner.ruler.acceptTrade(partner, tradedata[WANTEDAMOUNT], tradedata[GOODWANTED], tradedata[OFFEREDAMOUNT], tradedata[OFFEREDGOOD])
                    if(partner.ruler.acceptTrade):
                        lookup = (tradedata[GOODWANTED],tradedata[OFFEREDGOOD])
                        tradermethod,partnermethod = TRADELOOKUP[lookup]
                        trader.__setattr__(tradermethod,trader.__getattr__(tradermethod)   - tradedata[OFFEREDAMOUNT])
                        trader.__setattr__(partnermethod,trader.__getattr__(partnermethod) + tradedata[WANTEDAMOUNT])
                        partner.__setattr__(tradermethod,partner.__getattr__(tradermethod)   + tradedata[OFFEREDAMOUNT])
                        partner.__setattr__(partnermethod,partner.__getattr__(partnermethod) - tradedata[WANTEDAMOUNT])
                        trader.ruler.tradeOutcome(period, trader.key,  tradedata, True);
                        partner.ruler.tradeOutcome(period, trader.key, tradedata, True);
                    else:
                        trader.ruler.tradeOutcome(period, trader.key,  tradedata, False);
                        partner.ruler.tradeOutcome(period, trader.key, tradedata, False);                       