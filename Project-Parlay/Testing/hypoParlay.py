import random
import copy
from helper_testing import helper


class hypoParlay:
    hpID = -1

    def parlayID():
        hypoParlay.hpID += 1

        return hypoParlay.hpID
    

    def __init__(self, binsList, binWidth):
        self.binWidth = binWidth
        self.binsList = binsList
        self.hpID = hypoParlay.parlayID()
        self.numOutcomes = sum(len(x) for x in binsList)
        self.numBins = len(binsList)
        self.ImpliedProbability = "Not Yet Assigned"
        self.H_misses = 0
        self.H_hits = 0
        self.H_hitMissRatio = 0
        self.H_total_fails = 0
        self.H_total_times_profited = 0
        self.H_total_profit = 0
        self.H_seasonsProfit = []
        self.H_profitFailRatio = 0
        self.T_misses = 0
        self.T_hits = 0
        self.T_hitMissRatio = 0
        self.T_total_profit = 0
        self.T_total_fails = 0
        self.T_total_times_profited = 0
        self.T_seasonsProfit = []
        self.T_profitFailRatio = 0

