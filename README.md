# Texas-Holdem-Bot

Program that generates poker data through a simple Texas Hold'em simulation, loads the data to be trained and tested in multiple perceptrons, and predicts whether to fold or check/bet on a given stage of Texas Hold'em.  

## Data Generation

In order to simulate games, we used the file trainingbot.py, which is able to generate cards and players and determine the winner. To generate data through running the games, we used the file generate_training_data.py, which runs simulation games with 4 opponents and records the data to 4 csv files (preflop, flop, turn, and river).  
  
## Predicting Poker Decisions

In order to train the perceptrons, we use the file perceptron.py, which loads in the csv to a Pandas dataframe and then trains them to each respective perceptron on a 80/20 train test split. The perceptron objects are then saved to a file using Pickle. The files, play_accuracy.py and pokerGUI.py, are used to test and simulate the trained machines.
