from helper_testing import helper
from db_operations_testing import db_operations
from configurations_testing import configurations
from outcome_testing import outcome
from game_testing import game
import itertools
from prettytable import PrettyTable
from SA_MP_testing_version import outputs_SA
from config_group_testing import configGroup
import time
#from flask import Flask
#from flask import render_template
#app = Flask(__name__)

#db_ops = db_operations("allGameHistory.db")
allConfigs = []
bestConfigsBF = []
bestConfigsSA = []


#@app.route('/')
def startScreen():
    message = "Welcome to your Project Parlay!"
    #return render_template('index.html', message=message)

#if __name__ == '__main__':
    #app.run(debug=True)


def search_by_year():
       year=input("Enter the last two digits of the year you'd like to see data for: ")
       #query="SELECT * FROM NFLHistory WHERE schedule_date LIKE '%/"+year+"'"
       query="SELECT * FROM NFLHistory WHERE schedule_date LIKE '%" +1/15/67+"'"

       #print(db_ops.simple_query(query))
      # helper.pretty_print(results)
    
def search_by_games():
    #get a list of all artists
    query = '''
    SELECT game_id, team_home, team_away, winning_team
    FROM NFLHistory
    GROUP BY game_id;
    '''

    print("Games in database: ")
    dictionary = {}
    #games = db_ops.name_placeholder_query2(query, dictionary)
    
    #commenting out for lack of relevence to project; delete later
    '''
    #show all artists an create a dictionary of choices
    choices = {}
    for i in range(len(games)):
        print(i, games[i])
        choices[i] = games[i]
    index = helper.get_choice(choices.keys())

    print("How many songs do you want returned for "+choices[index]+"?")
    print("Enter 1, 5 or 0 for all songs")
    num = helper.get_choice([1,5,0])

    '''
    
# #@app.route('/')
# def calculateWinP(spread):
#     percent = (-.0303*spread) + .50
#     if(percent > .99):
#           return render_template('index.html', percent=.99)
#     else:
#           return render_template('index.html', percent=percent)
    
    
def permutations(numGamesPool, outcomesList):
    query = '''
    SELECT DISTINCT team_home
    FROM NFLHistory
    '''

    dictionary = {}
    #games = db_ops.name_placeholder_query2(query, dictionary)
    #list1 = ["a", "b", "c", "x", "y", "z"]

    numOutcomesPool = 2 * numGamesPool
    
    #print("\nYour Options..\n")

    #Generates all unique combination of elements in set up to set size numOutcomesPool
    for numOutcomesPool in range(numOutcomesPool, 0, -1):
        #TODO: May need to check if this is most efficient way to generate all combinations
        #TODO: Needs to use Delayed Column Generation Via Knapsack algorithm or other comination set approximation algorithm if total set of combinations is too large to be practical to generate quickly

        perm = list(itertools.combinations(outcomesList, numOutcomesPool))

        #TODO: Needs to utilize SQL insert to store configurations instead of list
        for i in perm:
            gameIDs = helper.gameIDs(i)

            #TODO: the if-statement in this for-loop checks the list for multiple outcomes with duplicate gameIDs (Which would make it impossible for both outcomes to occur), we need to research if there is a more efficient way to do this
            if(len(gameIDs) == len(set(gameIDs))):
                  
                x = configurations(i)
                allConfigs.append(x)

    #TODO: Needs to pull from SQL Database instead of list before printing
    #helper.config_print(allConfigs)

def calculate_runtime(func, configX, outcomeList, bestConfigsSA, T_0):
    start_time = time.time()
    x = func(configX, outcomeList, bestConfigsSA, T_0)
    end_time = time.time()
    runtime = end_time - start_time

    return x , runtime 



#TODO: Needs to pull from SQL Database instead of list of configs
#TODO: (SOLVED) Needs to evaluate based on (potential profit)/(risk) ratio, currently calculates on lowest risk only
#TODO: Needs to use simulated annueling to approximate best configs when total set of configs is too large to be practical
#TODO: (SOLVED) Needs to find a generalized way to find relative potential profit from a configuration before we assign a share of capital to it (Maybe Average?)
#TODO: Needs to use stock cutting algorithm to find final most optimal grouping from set of "best parlays" to fit user specifications
def bestConfig(configList,outcomeList):
      
    #Brute force evaluate all configs and then select best ones:
    while len(bestConfigsBF) < numParlays:
        maxValue = 0
        best = 0

        for x in configList:

            if x.value > maxValue:
                
                maxValue = x.value
                best = x

        if best not in bestConfigsBF:
    
            bestConfigsBF.append(best)
            configList.remove(best)

    #Dynamic best config finder using simulated annueling
    configX = configurations([])
    bestConfigsSA = []

    runtime = 0
    starting_thresh = outputs_SA.getThresh()

    while len(bestConfigsSA) < numParlays:
        SA_runtime = calculate_runtime(outputs_SA.outputs_simulated_annealing, configX, outcomeList, bestConfigsSA, outputs_SA.getThresh())
        bestConfigsSA.append(SA_runtime[0])
        runtime += SA_runtime[1]

    print("Runtime (SA): " + f"{runtime:.4f}")
    print("SA StartingThreshold: " + f"{starting_thresh:.3f}")

    SAresults = configGroup(bestConfigsSA)
    BFresults = configGroup(bestConfigsBF)
    crossover = configGroup.crossover(BFresults, SAresults)

    numSameConfigs = crossover[0]

    SA_Offset = configurations.multiOffset(crossover[2],crossover[3])

    if(SA_Offset[1] == 0):
        SA_Correctness = 1

    elif((numSameConfigs / numParlays) == 0):
        SA_Correctness = (1 -  (float(SA_Offset[0]) / float(SA_Offset[1]))) 
    else:
        SA_Correctness = ((1 -  (float(SA_Offset[0]) / float(SA_Offset[1]))) * (1 - (numSameConfigs / numParlays))) + (numSameConfigs / numParlays)

    print("SA Correctness: " + f"{SA_Correctness:.5f}")
    print("SA Combined Offset From Best Parlay Group: " + str(SA_Offset[0]))
    print("Number of exact matches betweeen Parlays in SA Parlay group and best possible: " + str(numSameConfigs))

    print("\n Best Parlays to Bet (BF):\n")
    helper.config_print(bestConfigsBF)

    print("\n Best Parlays to Bet (SA):\n")
    helper.config_print(bestConfigsSA)

    

    
#Main Program
startScreen()
#permutations()
#print statement unnessary
#print(calculateWinP(-11))

#search_by_year() WIP

#TODO: Program should calculate how many parlays would be optimal to use, instead of asking for user input
# An Idea for that is to use simulated annueling again on possible sets of best parlays looking to maximize "Total Value" (refrencing 'value' attribute of configuration obj)
#TODO: Each configuration group needs to keep track of its 'string factor'
#String factor refers to when one instance of a team winning is included in multiple configurations
#By the nature of parlays, including the same pick in multiple configurations in the same grouping would make it liable for the entire grouping to fail with a single unexpected loss
#Therefore a high "String Factor" would increase the total risk for the grouping, but shouldn't neccicarily be a dealbreaker if stringing a pick adequately improves total profit possibility.
numParlays = input()
print("Number of Parlays:" + numParlays)
numGamesPool = input()
print("Number of Games:" + numGamesPool)
totalUserCapital = input()

numParlays = int(numParlays)
totalUserCapital = int(totalUserCapital)
numGamesPool = int(numGamesPool)
gameList = []
outcomeList = []

#initializes all game objects from user input, and thus al outcome objecs are internally initialized inside the game initialization function
for x in range(numGamesPool):
    
    favoredTeam = input()
    underdog = input()

    
    favoredWinP = int(input())

    gameX = game(favoredTeam, underdog, favoredWinP, x)
    gameList.append(gameX)

for gameInstance in gameList:
    outcomeList.extend(gameInstance.outcomes)
    


permutations(numGamesPool, outcomeList)
bestConfig(allConfigs, outcomeList)
# search_by_games()
print("\nYour Options..\n")
helper.config_print(allConfigs)


#deconstruct at end
#db_ops.destructor()




#TODO: Need to design and Implement simple, clean, dynamic, colorful, interactive, web-based, easilly accessable with an internet connection, UI
#TODO: UI should have live parlay tracker feature with good visual design that tracks the state of each leg of a parlay (W,L, Yet To Start, Ongoing)
#If leg is a 'Win' that leg should light up green
#If leg is a 'Loss" whole parlay should light up red
#If All legs in parlay are a 'Win' then whole parlay should turn gold
#While Parlay has legs in either the 'Yet to start' or 'Ongoing' states, it should give a live percentage chance of that parlay hitting
#While Parlay grouping has parlays with legs in either the 'Yet to start' or 'Ongoing' states, it should give a live 'Max potential Win' and a percentage chance of it happening, it should also give a 'Most likely potential win' and a percentage chance of that happening as well
#TODO: UI should have a 'test and learn' tab where a user can enter a user made custom parlay and the algorithm will give it a score out of 10 on how good it is, as well as othr addition stats used for evaluating our own parlays
#TODO: UI should have option to generate 'Best Bet of the day' where it generates the most optimal parlay of games that are being played that day
#TODO: Computer Generate Additional SQL Database that contains 'Theoretical Games' where win percentages and odds are randomly generated, and outcomes are randomly generated based on those win percentages, for aditional testing
#TODO: Complete SQL database of NFL games up until current (Past games are subject to different rule changes and a different style of play, but still useful)
#TODO: Create SQL Database of stats for 'average parlay bettors' as well as 'Pro parlay bettors' to compare against algorithm for effectiveness
#TODO: UI should present user with three different options for parlay groupings to choose from: (High Profit/High Risk), (Optimal), (Lowest Risk)
#High and low risk options should still be relatively optimal
#TODO: Create a linear regression model to test if most profitable parlay groupings will always be profitable in a wide variety of contexts
#Stats for bettors could include (Profitable bet percentage), (Average amount of profit), as well as all stats we use to evaluate our own parlays and parlay groupings
#UI should have click and scrollable 'Input' from a list of web-scraped, upcoming games and bets to save user from wasting time entering data manually
#TODO: Need to implement web scraper to feed live/soon games to UI for easy user selection by click
#TODO:Need to be able to work with 'correlated parlays' as well, and their boosted odds (Ex: Patriots Win + Tom Brady Scores 2 Touchdowns + Patriots Defence allows less than 10 points)
#A decent amount of online betting services do not allow correlated parlays, so there needs to be an option to have the program aviod corredlated parlays as well
#User would have to indicate which bets are directly correlated and give a guess at how correlated they are
#It would be better to avoid additional user input for correlation strength, we could use web scraping to find bets then calculate correlation ourselves using mathematical means
#TODO: Need to create object to hold possible groupings of best parlays, should have the following attributes for later analysis: (Average number of legs in each parlay), (String Factor), (Number of parlays), (Total Value), (Max Profit Possible), (Average Profit Possible), (Percent Chance of profit occuring at all), 
#TODO: Program should calculate how many parlays would be optimal to use in final grouping, instead of asking for user input
# An Idea for that is to use simulated annueling again on possible sets of best parlays looking to maximize "Total Value" (refrencing 'value' attribute of configuration obj), we should also consider a historical factor when calculating "Total Value" so that backtesting with SQL database can be
#TODO: Each configuration group needs to keep track of its 'string factor'
#String factor refers to when one instance of a team winning is included in multiple configurations
#By the nature of parlays, including the same pick in multiple configurations in the same grouping would make it liable for the entire grouping to fail with a single unexpected loss
#Therefore a high "String Factor" would increase the total risk for the grouping, but shouldn't neccicarily be a dealbreaker if stringing a pick adequately improves total profit possibility
    