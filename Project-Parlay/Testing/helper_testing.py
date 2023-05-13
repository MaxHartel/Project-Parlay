from prettytable import PrettyTable
from configurations_testing import configurations
import pickle

class helper():
    # function parses a string and converts to appropriate type
    @staticmethod
    def convert(value):
        types = [int,float,str] # order needs to be this way
        if value == '':
            return None
        for t in types:
            try:
                return t(value)
            except:
                pass

    # function reads file path to clean up data file
    @staticmethod
    def data_cleaner(path):
        with open(path,"r",encoding="utf-8") as f:
            data = f.readlines()

        data = [i.strip().split(",") for i in data]
        data_cleaned = []
        for row in data[:]:
            row = [helper.convert(i) for i in row]
            data_cleaned.append(tuple(row))
        return data_cleaned

    # function checks for user input given a list of choices
    @staticmethod
    def get_choice(lst):
        choice = input("Enter choice number: ")
        while choice.isdigit() == False:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")

        while int(choice) not in lst:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")
        return int(choice)

    # function prints a list of strings nicely
    @staticmethod
    def pretty_print(lst):
        
        for i in lst:
            print(i)
        print("")

     # function prints a list of configurations nicely
    @staticmethod
    def config_print(configList):
        
        for y in configList:
            config = y.outcomeList

            # creating an empty PrettyTable
            x = PrettyTable()

            # adding data into the table row by row
            x.field_names = ["Team", "Win Percentage"]

            for i in config:    
                x.add_row([i.name, i.ImpliedProbability])
            
            #print config
            if(type(y.value == str)):
                print("\n|Parlay Odds: " + str(configurations.americanOddsToString(y)) + "|\n|Value: " + str(y.value) + 
                "|\n|Theoretical Payout: $" + str(y.theoreticalProfit) + "|" +
                "|\n|Decimal Odds: " + str(y.decimalOdds) + "|" +
                "|\n|Cid: " + str(y.configID) + "|")
            else:
                print("\n|Parlay Odds: " + configurations.americanOddsToString(y) + "|\n|Value: " + str(round(y.value, 2)) + 
                "|\n|Theoretical Payout: $" + str(round(y.theoreticalProfit, 2)) + "|" +
                "|\n|Decimal Odds: " + str(round(y.decimalOdds, 2)) + "|" +
                "|\n|Cid: " + str(y.configID) + "|")

            print(x)

    def outputListPrint(i, outcomeList):
        s = "["
        for outcome in outcomeList:
            s = s + outcome.name
            s = s + ","
        s = s + "]"

        print(i + s)

    
    @staticmethod
    def gameIDs(outcomesList):
        gameIdList = []

        for outcome in outcomesList:
            gameIdList.append(outcome.gameID)
        
        return gameIdList
    
    @staticmethod
    def hypoParlayPrint(arr):

        print("--------------------")
        print("BinWidth: " + str(arr.binWidth))
        print("hpID: " + str(arr.hpID))
        print("total Theoretical Profit: " + str(arr.T_total_profit))
        print("Viability: " + str(arr.T_hitMissRatio))
        print("Profit Happening Percentage: " + str(arr.T_profitFailRatio))

        arr = arr.binsList

        for row in arr:
            for item in row:
                print(item, end=" ")
            print()
        print("--------------------")
        
        print()

    @staticmethod
    def serializeParlayList(parlayList, fileName):
    # Serialize list of objects to binary file
        with open(fileName, 'wb') as f:
            pickle.dump(parlayList, f)

    @staticmethod
    def deserializeParlayList(fileName):
        # Load list of objects from binary file
        parlayList = []

        with open(fileName, 'rb') as f:
            parlayList = pickle.load(f)

        return parlayList
    


