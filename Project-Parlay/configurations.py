from db_operations import db_operations
import random
import copy

class configurations:
    cID = 0
        
    def americanOddsToString(config):

        if(type(config.AmericanOdds) != str):

            if(config.AmericanOdds > 0):
                return "+" + str(round(config.AmericanOdds, 2))
            else:
                return "-" + str(-1 * round(config.AmericanOdds, 2))
            
        else:
            return config.AmericanOdds

            
    #TODO: Make accurate 'value' function from historical/theoretical factors using data science and back testing
    # Profit/risk are different representations of the same stat, so their ratio will always be 10
    #config.value = config.theoreticalProfit * config.profitChance
    def value(config):
        #config.value = (1 - config.profitChance)
        config.value = 1 - abs(config.decimalOdds - 3.15)
        
        return config.value
    
    #Sorts a list of configs by value - is not essential if needs to be cut due to efficiency concerns
    def sort(configList):
        cList = copy.deepcopy(configList)

        # Define a variable to keep track of whether a swap has occurred
        swapped = True

        # Keep looping until no swaps occur during a full pass through the list
        while swapped:

            # Assume no swaps occur during this pass
            swapped = False

            # Iterate through the list, comparing adjacent elements
            for i in range(len(cList) - 1):

                if cList[i].value > cList[i + 1].value:

                    # If the current element is greater than the next element, swap them
                    temp = copy.deepcopy(cList[i])
                    cList[i] = copy.deepcopy(cList[i + 1])
                    cList[i + 1] =  copy.deepcopy(temp)

                    # Set swapped to True, indicating that a swap has occurred during this pass
                    swapped = True

        #sort outcomes within configs 
        for config in cList:
            oList = list(copy.deepcopy(config.outcomeList))

            # Define a variable to keep track of whether a swap has occurred
            oSwapped = True

            # Keep looping until no swaps occur during a full pass through the list
            while oSwapped:

                # Assume no swaps occur during this pass
                oSwapped = False

                # Iterate through the list, comparing adjacent elements
                for i in range(len(oList) - 1):

                    if oList[i].ImpliedProbability  > oList[i + 1].ImpliedProbability:

                        # If the current element is greater than the next element, swap them
                        temp = copy.deepcopy(oList[i])
                        oList[i] = copy.deepcopy(oList[i + 1])
                        oList[i + 1] =  copy.deepcopy(temp)

                        # Set swapped to True, indicating that a swap has occurred during this pass
                        oSwapped = True

            config.outcomeList = oList


        # return the sorted list
        return(cList)
        
    

    def configID():
        configurations.cID += 1

        return configurations.cID

        
    #Calculates potential profit for parlay assuming "True Odds"
    #TODO Add web-Scraper support for the fixed odds of popular online casinos, maybe store tables of fixed odds for different size parlays and update as frequently as needed
    @staticmethod
    def profit(config):
        # Win Percentage = Implied Probability
        # Implied probability = negative American odds/(negative American odds + 100) * 100
        # Implied probability = 100 / (positive American odds + 100) * 100
        # positive American odds = ((1 – implied probability) / implied probability)  * 100
        # negative American odds = –1 * ( implied probability / (1 – implied probability)) * 100
        # decimal odds (From +American) = (AmericanOdds + 100) / 100
        # decimal odds (From -American) = (AmericanOdds + 100) / AmericanOdds (Please note that for the purposes of this calculation, the negative sign in the odds is ignored.)

  
        theoreticalCapital = 10
        configDecimalOdds = 1
        outcomeList = config.outcomeList
        
        for outcome in outcomeList:
            iP = outcome.ImpliedProbability/100

            if(outcome.underdog):

                outcome.AmericanOdds = ((1 - iP) / iP) * 100
                outcome.decimalOdds = (outcome.AmericanOdds + 100) / 100
            else:
                outcome.AmericanOdds = -1 * (iP / (1 - iP)) * 100
                outcome.decimalOdds = ((-1 *  outcome.AmericanOdds) + 100) / (-1 * outcome.AmericanOdds)

            configDecimalOdds *= outcome.decimalOdds

        config.decimalOdds = configDecimalOdds

        if(configDecimalOdds > 2):

            config.AmericanOdds = (configDecimalOdds - 1) * 100
            config.ImpliedProbability = 100 / (config.AmericanOdds + 100) * 100
        else:
            config.AmericanOdds = -1 * (100 / (configDecimalOdds - 1))
            config.ImpliedProbability = config.AmericanOdds / (config.AmericanOdds + 100) * 100

        config.theoreticalProfit = (configDecimalOdds * theoreticalCapital)

        configurations.value(config)

    #determines if two configs are the same
    @staticmethod
    def equals(configA, configB):
        setA = set(configurations.outcomeIDs(configA.outcomeList))
        setB = set(configurations.outcomeIDs(configB.outcomeList))

        if(setA == setB):
            return True
        else:
            return False
        
    @staticmethod
    def outcomeIDs(outcomesList):
        outcomeIdList = []

        for outcome in outcomesList:
            outcomeIdList.append(outcome.outcomeID)
        
        return outcomeIdList
    
    @staticmethod
    def offset(configA, configB):
        SA_Offset = 0

        #increments SA_Offset if the best solution contains a outcome that it does not
        for o in configurations.outcomeIDs(configA.outcomeList):
            exist_count = (configurations.outcomeIDs(configB.outcomeList)).count(o)

            if(exist_count <= 0):
                SA_Offset += 1

        #increments SA_Offset if the it contains a outcome that best solution does not
        for o in configurations.outcomeIDs(configB.outcomeList):
            exist_count = (configurations.outcomeIDs(configA.outcomeList)).count(o)

            if(exist_count <= 0):
                SA_Offset += 1

        return SA_Offset


    #TODO(SOLVED): Needs work to calculate for underdogs as well, currently assumes every team is a favorite
    #TODO(SOLVED): Needs to be fixed to properly asses risk
    @staticmethod
    def risk(outcomeList):
        risk = 1

        for outcome in outcomeList:
            risk *= (outcome.ImpliedProbability/100)

        return risk


    
    def __init__(self, outcomeList):
        self.numOutcomes = len(outcomeList)
        self.configID = configurations.configID()
        self.outcomeList = outcomeList
        
        #checks for empty configuration
        if(self.numOutcomes > 0):

            self.profitChance = configurations.risk(outcomeList)
            self.theoreticalProfit = "Not Yet Assigned"
            self.AmericanOdds = "Not Yet Assigned"
            self.ImpliedProbability = "Not Yet Assigned"
            self.decimalOdds = "Not Yet Assigned"
            #TODO: Needs to have attribute 'value' that represents parlay quality
            # 'value' will be attribute maximized by simulated annueling
            self.value = "Not Yet Assigned"

            configurations.profit(self)

        else:
            self.profitChance = "Not Yet Assigned"
            self.theoreticalProfit = "Not Yet Assigned"
            self.AmericanOdds = "Not Yet Assigned"
            self.ImpliedProbability = "Not Yet Assigned"
            self.decimalOdds = "Not Yet Assigned"
            #TODO: Needs to have attribute 'value' that represents parlay quality
            # 'value' will be attribute maximized by simulated annueling
            self.value = 0



