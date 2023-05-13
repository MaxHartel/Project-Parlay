import random
import math
import itertools
from prettytable import PrettyTable
from hypoParlay import hypoParlay
import numpy as np
from helper_testing import helper
import copy
import time
from getpass import getpass


optimals = []


def binFit():
    pass

# The function first initializes a variable size which takes O(1) time.
# The outer for loop iterates 16 times, which is a constant factor and takes O(1) time.
# The inner for loop iterates through all combinations with replacement of size i, which takes O(2^i) time.
# Inside the inner loop, the function initializes a new list and performs a deep copy of bins which takes O(len(bins)) time. 
# It then performs another loop over the combo and appends 'x' to some elements in newList. The length of the combo is at most size, 
# so this loop takes O(size) time.
# Finally, the function appends newList to a list allShapesForCombo. Since this operation takes constant time, 
# the total time taken is proportional to the number of elements added to allShapesForCombo, which is the sum of O(2^i) for all i from 0 to 15. This simplifies to O(2^16 - 1) = O(65535).
# Therefore, the big-O runtime of parlaySizeStep(bins) is O(size * (2^16 - 1)) = O(size * 65535).
def parlaySizeStep(bins):
    size = len(bins)
    allShapesForCombo = []
    newList = []

    for i in range(16):
        for combo in itertools.combinations_with_replacement(range(size),i):
            newList = copy.deepcopy(bins)
            for indexElement in combo:
                newList[indexElement].append('x')
                
            allShapesForCombo.append(newList)

    return allShapesForCombo

    
# The function first initializes allBinsListLength and allBinsList, which takes O(1 + 100/binWidth) time.
# The first loop iterates allBinsListLength times and performs constant time operations, so it takes O(allBinsListLength) = O(100/binWidth) time.
# The second loop iterates over all combinations of bins of size i and calls parlaySizeStep(combo) on each combination.
# The length of combo is at most allBinsListLength, so there are O(allBinsListLength^2) combinations in total. 
# The parlaySizeStep() function is called on each combination, which takes O(size * 65535) time. 
# Therefore, the total time spent on this loop is O((100/binWidth)^2 * 65535).
# The third loop iterates over a list of length len(listA) and calls hypoParlay() on each element. 
# The length of listA is at most (100/binWidth)^2 * 65535, so this loop takes O((100/binWidth)^2 * 65535 * m) time, 
# where m is the time taken by hypoParlay().
# Therefore, the big-O runtime of parlayBuilder(binWidth) is O((100/binWidth)^2 * 65535 * m).
def parlayBuilder(binWidth):
    allBinsListLength = int(100/binWidth)
    allBinsList = []
    listA = []
    listB = []

    #creates list of bins for the potential parlay, and assigns each bin the value of its index as a placeholder
    for x in range(0,allBinsListLength):
        allBinsList.append(list([str(x)]))

    for i in range(allBinsListLength, 0, -1):
        allBinWidthCombos= itertools.combinations(allBinsList,i)

        for combo in allBinWidthCombos:
            listA.extend(parlaySizeStep(combo))

    for u in listA:
        listB.append(hypoParlay(u,binWidth))
        continue


    return listB


#Complexity: O(2^21 * n^2), where n is the length of the input list bins to parlaySizeStep. 
def main():
    #binWidths = [3,5,7,9,10,11,13,15,20]
    binWidths = [20]
    AllParlays = []

    start_time = time.time()

    print(str(len(binWidths)))
    print(input())

    for x in binWidths:
        fileName = "serializedHypoParlaysBW_" + str(x)
        print(fileName + "\n",end="")
        p = parlayBuilder(x)
        helper.serializeParlayList(p, fileName)

    #helper.serializeParlayList(AllParlays,fileName)

    

main()
# start_time = time.time()
# main()
# end_time = time.time()
# runtime = end_time - start_time
# print("runtime: " + str(runtime))
