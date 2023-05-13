# Algorithim Analysis Final Project: Project Parlay

## How to Run
* Open a terminal inside the Project_parlay Folder
* Run **make run**
* Once the program is finsihed running, you can open index.html in a browser to see the data in a more convenient way

## Introduction
Our group consists of James Tran, Jason Bohlinger, Andrew Broek, and Max Hartel. 

Project Parlay is a program made for the purposes of sports betting. It takes the data available in a given sports league and the input of the user's desired amount of capital and bets to return the most optimal way to use that capital for parlays.

The program uses a sqlite database of NFL games with data such as teams, odds, outcomes, and dates as a sample to test simulated annealing as an algorithm for finding the most optimal bets. The bulk of our backend code is done in python. There are two options for our front-end:
* When running the code in a command line, **results.py** will show a Tkinter window that prints the results of the parlays.
* The user can also open index.html in a browser after running the code to see the results in a more accessible environment. 

## Literature Review


## Testing

## Complications/Challenges
One of the most significant challenges we faced during the project was developing an efficient communication channel between our back-end and front-end. While we had initially planned on implementing a more sophisticated front-end, we ultimately had to make some compromises due to time and resource constraints. We shifted to a tkinter window and an HTML webpage printing the ASCII version of our output. The important and essential information is there, albeit in a less elegant way. Ultimately, the entire project can be done with one command in the command line and/or opening an HTML file in a browser, which is the ease of use we wanted. We also did not have the time to implement web scraping for live results. However, this did not affect the quality of our algorithm, and we were still able to achieve our goal of delivering accurate and optimal parlays to users.

## Contributions
* Max:
* James: Initial Simulated Annealing Research, Front-End Design and Implementation (Tkinter, HTML)
* Jason: Setup, maintenance, and formatting of the SQLite database for the group's needs.
* Andrew: SQL Testing, Knapsack research, and Simulated Annealing implementation.  

## Future Directions
* Web scraping from an online database, yielding live results, would allow for easy automation. This means you could run this program for an entire season, hands-off, as it places bets for you and you can simply cash your checks!
* Having a more sophisticated UI would help with the average user's understanding of what is going on. Hopefully, a nice and effective web app would showcase the potential of this program.

## References
* References for algorithms:  https://algorithmsbook.com/optimization/#
* Tkinter implementation: https://www.geeksforgeeks.org/python-tkinter-text-widget/
* HTML: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe


## MVP
[Link to the MVP Google Doc](https://docs.google.com/document/d/13wJoVv6TtfDdh3ldmpE6DFQjKy5D8gcNz_RNbGRM4Nw/edit?usp=sharing)
