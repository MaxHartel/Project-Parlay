# import random
# import math
# from configurations import configurations
# from helper import helper
# import copy

# #https://www.researchgate.net/publication/227061666_Computing_the_Initial_Temperature_of_Simulated_Annealing#:~:text=The%20classical%20version%20of%20simulated,with%20a%20given%20acceptance%20ratio.
# #http://what-when-how.com/artificial-intelligence/a-comparison-of-cooling-schedules-for-simulated-annealing-artificial-intelligence/

# class outputs_SA():
#     parlaysOutput = 0

#     #Simulated Annueling Algorithm that finds best configuration from a set of total outputs
#     def outputs_simulated_annealing(initial_config, allOutputsList, bestConfigurationsList, temp_threshold):
#         outputs_SA.parlaysOutput += 0.01
#         current_config = initial_config
#         best_config = initial_config
#         temperature = 100
#         temperature_init = temperature
#         countIter = 0
#         bestConfigurationsList
#         acceptance_probability = -1 #remove later

#         while (temperature > (temp_threshold - outputs_SA.parlaysOutput)):
#             #cooling_rate = abs(temperature_init / (1 + math.log(1 + countIter)))

#             neighbor_config = outputs_SA.get_neighbor(current_config, allOutputsList)
#             # current_value = configurations.value(current_config)
#             # neighbor_value = configurations.value(neighbor_config)
#             current_value = current_config.value
#             neighbor_value = neighbor_config.value

#             # helper.outputListPrint(str(countIter)+"Curr config:" ,current_config.outcomeList)
#             # helper.outputListPrint("Neighbor config:", neighbor_config.outcomeList)

#             #print("Best Value: " + str(best_config.value) + ", Curr Value: " + str(current_value) + ", neighbor_value: " + str(neighbor_value))
#             if (neighbor_value > current_value):
#                 current_config = neighbor_config

#                 if (neighbor_value > best_config.value):
#                     #TODO:potential solution to 2nd best issue: if neighbor config is the same as a config in the existing "best configs set",
#                     # then do not set best_config to neighbor config and continue

#                     potential_best_exists = False

#                     for existingBestConfig in bestConfigurationsList:
#                         if(configurations.equals(neighbor_config, existingBestConfig)):
#                             potential_best_exists = True

#                     if(potential_best_exists):
#                         pass
#                     else:
#                         best_config = neighbor_config

#             else:
#                 delta_value = (current_value - neighbor_value)
#                 acceptance_probability = math.exp(-delta_value / temperature)
#                 #print("AP: " + str(acceptance_probability))

#                 if (random.uniform(0, 1) < acceptance_probability):
#                     current_config = neighbor_config
                    
#             # helper.outputListPrint("Curr config:" ,current_config.outcomeList)
#             # helper.outputListPrint("Best Config:" ,best_config.outcomeList)
#             #if(temperature % 17 < 2):
#             # print("temp: " + str(temperature))
#             # print("AP: " + str(acceptance_probability))

#             temperature = temperature_init / (1 + (3 *countIter))
#             countIter += 1

#         return configurations(best_config.outcomeList)



#     def get_neighbor(config, allOutputsList):
#         # Generate a random 'neighbor' of the current config
#         # Configs are 'Neighbors if they only differ by one output

#         neighborOutcomeList = []
#         cOutputList = copy.deepcopy(config.outcomeList)
#         localAllOutputs = copy.deepcopy(allOutputsList)
#         breakout = False

#         #checks to see if a smaller neighbor exists
#         if(len(cOutputList) > 0):

#             rand = random.randint(0,10)
#         else:
#             rand = 5

#         #slight bias towards building bigger parlays to avoid initial backtracking
#         #later will make bias dynamic as most testing data can be analyzed
#         if (rand > 4):
#             #Generate Larger neighbor
#             count = 0

#             while(True):
#                 #generates list of the gameID's of the outputs in the current config's outPutList
#                 #[*cOutputList, 'e']
#                 if (len(localAllOutputs) > 1):
#                     randomIndex = random.randint(0,len(localAllOutputs) - 1)
#                 else:
#                     randomIndex = 0
#                     breakout = True
                
#                 #print(str(len(localAllOutputs)) + " , " + str(randomIndex))

#                 potentialNeighborOptList = [*cOutputList,localAllOutputs[randomIndex]]
#                 gameIDs = helper.gameIDs(potentialNeighborOptList)

#                 # print("\n--Inside getneighbor:")
#                 #print("gameIDs:" + str(gameIDs))
#                 # helper.outputListPrint("AllOpts:" ,allOutputsList)
#                 # helper.outputListPrint("pNeigOpts", potentialNeighborOptList)
#                 # print("--Exit getneighbor:\n")


#                 #TODO: the if-statement in this loop checks the list for multiple outcomes with duplicate gameIDs (Which would make it impossible for both outcomes to occur), we need to research if there is a more efficient way to do this
#                 if((len(gameIDs) == len(set(gameIDs)))):
#                     break
#                 elif(breakout):
#                     potentialNeighborOptList.pop()
#                     break
#                 else:
#                     del localAllOutputs[randomIndex]

#             neighborOutcomeList = potentialNeighborOptList


#         else:
#             #generate smaller neighbor
#             ri = random.randint(0,len(cOutputList)-1)
#             del cOutputList[ri]

#             # print("\n--Inside getneighbor D:")
#             # helper.outputListPrint("negOpts:" ,cOutputList)
#             # print("--Exit getneighbor:\n")

#             neighborOutcomeList = cOutputList



#         #may want to consider working with outcome list directly and only creating new object once SA finsihes, for efficiency reasons
#         return configurations(neighborOutcomeList)




import random
import math
from configurations import configurations
from helper import helper
import copy

#https://www.researchgate.net/publication/227061666_Computing_the_Initial_Temperature_of_Simulated_Annealing#:~:text=The%20classical%20version%20of%20simulated,with%20a%20given%20acceptance%20ratio.
#http://what-when-how.com/artificial-intelligence/a-comparison-of-cooling-schedules-for-simulated-annealing-artificial-intelligence/

class outputs_SA():
    parlaysOutput = 0
    #threshold = 0.02
    threshold = 0.03
    thresholdMod = 0.8

    def getThresh():
        return outputs_SA.threshold

    #Simulated Annueling Algorithm that finds best configuration from a set of total outputs
    def outputs_simulated_annealing(initial_config, allOutputsList, bestConfigurationsList):
        outputs_SA.parlaysOutput += 1
        current_config = initial_config
        best_config = initial_config
        temperature = 100
        temperature_init = temperature
        countIter = 0
        bestConfigurationsList
        
        #outputs_SA.threshold = temp_threshold

        for i in range(outputs_SA.parlaysOutput):
            outputs_SA.threshold *= outputs_SA.thresholdMod



        while (temperature > outputs_SA.threshold):

            neighbor_config = outputs_SA.get_neighbor(current_config, allOutputsList)

            current_value = current_config.value
            neighbor_value = neighbor_config.value

            if (neighbor_value > current_value):
                current_config = neighbor_config

                if (neighbor_value > best_config.value):
                    #TODO: (SOLVED) solution to 2nd best issue: if neighbor config is the same as a config in the existing "best configs set",
                    # then do not set best_config to neighbor config and continue

                    potential_best_exists = False

                    for existingBestConfig in bestConfigurationsList:
                        if(configurations.equals(neighbor_config, existingBestConfig)):
                            potential_best_exists = True

                    if(potential_best_exists):
                        pass
                    else:
                        best_config = neighbor_config

            else:
                delta_value = (current_value - neighbor_value)
                acceptance_probability = math.exp(-delta_value / temperature)

                if (random.uniform(0, 1) < acceptance_probability):
                    current_config = neighbor_config
                    

            temperature = temperature_init / (1 + (3 *countIter))
            countIter += 1

        return configurations(best_config.outcomeList)



    def get_neighbor(config, allOutputsList):
        # Generate a random 'neighbor' of the current config
        # Configs are 'Neighbors if they only differ by one output

        neighborOutcomeList = []
        cOutputList = copy.deepcopy(config.outcomeList)
        localAllOutputs = copy.deepcopy(allOutputsList)
        breakout = False

        #checks to see if a smaller neighbor exists
        if(len(cOutputList) > 0):

            rand = random.randint(0,10)
        else:
            rand = 5

        #slight bias towards building bigger parlays to avoid initial backtracking
        #later will make bias dynamic as most testing data can be analyzed
        if (rand > 4):
            #Generate Larger neighbor
            count = 0

            while(True):
                #generates list of the gameID's of the outputs in the current config's outPutList
                if (len(localAllOutputs) > 1):
                    randomIndex = random.randint(0,len(localAllOutputs) - 1)
                else:
                    randomIndex = 0
                    breakout = True

                potentialNeighborOptList = [*cOutputList,localAllOutputs[randomIndex]]
                gameIDs = helper.gameIDs(potentialNeighborOptList)


                #TODO: the if-statement in this loop checks the list for multiple outcomes with duplicate gameIDs (Which would make it impossible for both outcomes to occur), we need to research if there is a more efficient way to do this
                if((len(gameIDs) == len(set(gameIDs)))):
                    break
                elif(breakout):
                    potentialNeighborOptList.pop()
                    break
                else:
                    del localAllOutputs[randomIndex]

            neighborOutcomeList = potentialNeighborOptList


        else:
            #generate smaller neighbor
            ri = random.randint(0,len(cOutputList)-1)
            del cOutputList[ri]

            neighborOutcomeList = cOutputList



        #may want to consider working with outcome list directly and only creating new object once SA finsihes, for efficiency reasons
        return configurations(neighborOutcomeList)


