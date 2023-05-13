import random
import math
import itertools
import copy
from prettytable import PrettyTable
from hypoParlay import hypoParlay
import numpy as np
from helper_testing import helper
import csv
from sim_game import simGame
from week import week

        #self.binWidth = binWidth
        # self.binsList = binsList
        # self.hpID = hypoParlay.parlayID()
        # self.numOutcomes = sum(len(x) for x in binsList)
        # self.numBins = len(binsList)
        # self.AmericanOdds = "Not Yet Assigned"
        # self.ImpliedProbability = "Not Yet Assigned"
        # self.H_misses = 0
        # self.H_hits = 0
        # self.H_hitMissRatio = 0
        # self.H_total_profit = 0
        # self.H_seasonsProfit = []
        # self.H_profitFailRatio = 0
        # self.T_misses = 0
        # self.T_hits = 0
        # self.T_hitMissRatio = 0
        # self.T_total_profit = 0
        # self.T_seasonsProfit = []
        # self.T_profitFailRatio = 0

# O(n) Complexity, where n is the number of games in a week.
def sim_week(hypoParlay, week):
    gameList = week.gamesList
    binWidth = hypoParlay.binWidth
    binsList = copy.deepcopy(hypoParlay.binsList)
    weekWinners = []
    parlayPicks = []
    hit = True
    profit = True
    parlay_picks_IPs = []
    weeklyProfit = 0

    for game in gameList:
        weekWinners.append(game.winner)
        indexF = (float(game.favWinP) // binWidth) #hash function
        indexU = (float(game.favWinP) // binWidth) #hash function

        if indexF in binsList:
            if 'x' in binsList[binsList.index(indexF)]:
                i = binsList[binsList.index(indexF)].index('x')
                del binsList[binsList.index(indexF)][i]
                parlayPicks.append(game.favoredTeam)
                parlay_picks_IPs.append(game.favWinP)

        elif indexU in binsList:
            if 'x' in binsList[binsList.index(indexU)]:
                j = binsList[binsList.index(indexU)].index('x')
                del binsList[binsList.index(indexU)][i]
                parlayPicks.append(game.underdog)
                parlay_picks_IPs.append(game.undWinP)

    hypoParlay.ImpliedProbability = float(math.prod(parlay_picks_IPs)) / float(pow(100, len(parlay_picks_IPs)))
    hypoParlay.dOdds = 1 / hypoParlay.ImpliedProbability


    for bin in binsList:
        if 'x' in bin:
            hypoParlay.T_misses += 1
            hit = False
            # print('miss: ' + str(hypoParlay.hpID) + " week:" + str(week.SeasonWeek_ID))
            break
    
    if hit:
        hypoParlay.T_hits =+ 1
        print('hit: ' + str(hypoParlay.hpID)+ " week:" + str(week.SeasonWeek_ID))

    #10 is hardcoded here as the dollar bet placed on the parlay each week
    for winner in parlayPicks:
        if winner not in weekWinners:
            hypoParlay.T_total_fails += 1
            hypoParlay.T_total_profit -= 10
            weeklyProfit -= 10
            profit = False
            break

    if profit:
        hypoParlay.T_total_times_profited += 1
        hypoParlay.T_total_profit += 10 * hypoParlay.dOdds
        weeklyProfit += 10 * hypoParlay.dOdds

    
    return weeklyProfit

    


#iterates through all weeks and all parlay objects, so its complexity is O(n^2), where n is the number of weeks. 
def simulate(parlayList,fileName):
    
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        gameList = []
        weekList = []
        currSWid = 0.0
        currSeason = 0
        seasonProfit = 0
        

        for row in reader:
            # with the row, instantiate an object
            gameList.append(simGame(row['Game_ID'],row['gameDate'],row['FavoredTeam_ID'],row['Underdog_ID'],row['Fav_Implied_Win_P'],row['UndD_Implied_Win_P'],row['Winner_ID']))

            if(float(row['SeasonWeek_ID']) > currSWid):
                weekList.append(week(row['SeasonWeek_ID'],gameList))
                gameList = []
                currSWid = float(row['SeasonWeek_ID'])


        for hypoParlay in parlayList:

            for w in weekList:

                if( math.floor(float(w.SeasonWeek_ID)) > currSeason):
                    hypoParlay.T_seasonsProfit.append(seasonProfit)
                    seasonProfit = 0
                    currSeason += 1

                weeklyProfit = sim_week(hypoParlay, w)
                seasonProfit += weeklyProfit

    maxValue_T(parlayList,6)

#has two nested loops and calls a function with O(n) complexity, so its complexity is O(n^2).
def maxValue_T(parlayList,num):
    bestValParlays = []

    while len(bestValParlays) < num:
        maxProfit = 0
        best = 0

        for x in parlayList:

            if x.T_total_profit > maxProfit:
                
                maxProfit = x.T_total_profit 
                best = x

        if best not in bestValParlays:

            bestValParlays.append(best)
            parlayList.remove(best)

        maxProfit = 0
        best = 0

        for x in parlayList:
            x.T_profitFailRatio = float(x.T_total_times_profited) / float(x.T_total_times_profited) + float(x.T_total_fails)

            if x.T_profitFailRatio > maxProfit:
                
                maxProfit = x.T_profitFailRatio 
                best = x

        if best not in bestValParlays:

            bestValParlays.append(best)
            parlayList.remove(best)

    print("Best Performing Parlays By overall Profit: \n")
    for u in bestValParlays:
        helper.hypoParlayPrint(u)


    
                

def main():

        #input fileName containing serialized hypoParlays
        numFiles = int(input())
        simDataFileName = input()
        parlayList = []

        for i in range(numFiles):
             
            fileName = input()
            parlayList.append(helper.deserializeParlayList(fileName))

        
        for x in parlayList:
            for u in x:
                helper.hypoParlayPrint(u)
                
            #simulate(x,simDataFileName)

    # sf = sort_and_file(AllParlays)

    # for x in range(len(sf)):
    #     optimals[x] = valueSim.maxValue(sf[x])


main()