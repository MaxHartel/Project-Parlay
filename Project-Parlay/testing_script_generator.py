import random

# Open a file for writing
with open("testing_script.txt", "w") as file:
    
    rInt = random.randint(2, 3)
    # Write some text to the file

    #How many parlays would you like to bet on?
    file.write(str(rInt)+ "\n")

    #From How many games would you like us to consider before we calculate best?
    numGames = rInt + 8
    file.write(str(numGames)+ "\n")

    #How much capital would you like to bet($)
    rInt = random.randint(5, 100)
    file.write(str(rInt)+ "\n")

    for x in range(numGames):
        #Please Enter The Favored Team for game x:
        favored_team_id = random.choice([chr(x) for x in range(65, 91)])
        file.write(str(favored_team_id)+ "\n")

        #Please Enter The Underdog for game x:
        underdog_id = favored_team_id
        while underdog_id == favored_team_id:
            underdog_id = random.choice([chr(x) for x in range(65, 91)])
        file.write(str(underdog_id)+ "\n")

        #Please enter the win percentage chance for the favored team:
        fav_implied_win_p = random.randint(51, 99)
        file.write(str(fav_implied_win_p)+ "\n")


