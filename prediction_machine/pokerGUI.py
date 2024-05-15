import tkinter as tk
from tkinter import messagebox
import random
from data_generation.trainingbot import DummyBot
from perceptron import Perceptron
import pandas as pd
import numpy as np
import itertools
import os
import pickle
import random

# Function to create a complete deck
def create_deck():
    card_ranks = list(range(2, 15))  # 2 to Ace (2 to 14)
    card_suits = list(range(1, 5))   # 1 to 4 (Spades, Hearts, Diamonds, Clubs)

    # All combinations of ranks and suits to form a full deck
    deck = [(rank, suit) for rank in card_ranks for suit in card_suits]
    return deck

# Function to generate a 2-card pre-flop hand
def generate_preflop_hand(deck):
    # Draw two unique cards from the deck
    card1 = deck.pop()
    card2 = deck.pop()

    # Represent the hand as [rank1, suit1, rank2, suit2]
    hand = [(card1[0], card1[1]), (card2[0], card2[1])]

    return hand

# Function to generate the flop (3 community cards)
def generate_flop(deck):
    # Draw three unique cards from the deck for the flop
    flop = tuple(deck.pop() for _ in range(3))

    return flop

# Function to generate the river (1 community card)
def generate_river(deck):
    # Draw one card from the deck for the river
    river = deck.pop()

    # Return the card in the format [rank, suit]
    return (river[0], river[1])


# Function to generate the turn (1 community card)
def generate_turn(deck):
    # Draw one card from the deck for the turn
    turn = deck.pop()

    # Return the card in the format [rank, suit]
    return (turn[0], turn[1])


def convert_to_tuples(flat_list):
    if len(flat_list) % 2 != 0:
        raise ValueError("The input list must contain an even number of elements")

    # Create tuples from pairs of elements (rank, suit)
    return [(flat_list[i], flat_list[i + 1]) for i in range(0, len(flat_list), 2)]

# Function to evaluate poker hands and determine the winner
def compare_poker_hands(player_hand, opponent_hand, table):
    # Convert flat lists to tuples
    table_tuples = convert_to_tuples(table)

    # Combine each hand with the table to create all 5-card combinations
    player_full_hand = player_hand + table_tuples
    opponent_full_hand = opponent_hand + table_tuples
    print(player_full_hand)
    print(opponent_full_hand)
    # Function to get all possible 5-card combinations from a 7-card hand
    def get_combinations(full_hand):
        if len(full_hand) != 7:
            raise ValueError("Each full hand must contain 7 cards")

        return list(itertools.combinations(full_hand, 5))
    
    # Function to evaluate a poker hand and return a numeric value representing its strength
    def evaluate_poker_hand(hand):
    # Extract ranks and suits
        ranks = sorted([card[0] for card in hand])
        suits = [card[1] for card in hand]

        # Define poker hand values
        if is_royal_flush(ranks, suits):
            return (10, [])  # Royal Flush
        elif is_straight_flush(ranks, suits):
            return (9, [ranks[-1]])  # Straight Flush, kicker is the highest card
        elif is_four_of_a_kind(ranks):
            # Find the rank that has four of a kind
            four_rank = next(rank for rank in ranks if ranks.count(rank) == 4)
            kicker = next(rank for rank in ranks if rank != four_rank)
            return (8, [four_rank, kicker])  # Four of a Kind with kicker
        elif is_full_house(ranks):
            # Identify the triplet and pair
            triple_rank = next(rank for rank in ranks if ranks.count(rank) == 3)
            pair_rank = next(rank for rank in ranks if ranks.count(rank) == 2)
            return (7, [triple_rank, pair_rank])  # Full House
        elif is_flush(suits):
            # Return the sorted card ranks for flush (highest is the main value)
            return (6, ranks[::-1])  # Flush with kickers
        elif is_straight(ranks):
            # Straight is primarily determined by the highest card
            return (5, [ranks[-1]])  # Straight with highest card as kicker
        elif is_three_of_a_kind(ranks):
            # Identify the triplet and kickers
            triple_rank = next(rank for rank in ranks if ranks.count(rank) == 3)
            kickers = sorted([rank for rank in ranks if rank != triple_rank], reverse=True)
            return (4, [triple_rank] + kickers)  # Three of a Kind with kickers
        elif is_two_pair(ranks):
            # Identify both pairs and the highest kicker
            pairs = [rank for rank in set(ranks) if ranks.count(rank) == 2]
            kicker = max([rank for rank in ranks if ranks.count(rank) == 1])
            return (3, pairs + [kicker])  # Two Pair with kickers
        elif is_one_pair(ranks):
            # Identify the pair and the three highest kickers
            pair_rank = next(rank for rank in set(ranks) if ranks.count(rank) == 2)
            kickers = sorted([rank for rank in ranks if rank != pair_rank], reverse=True)
            return (2, [pair_rank] + kickers)  # One Pair with kickers
        else:
            # For High Card, the order of all cards is the key
            return (1, ranks[::-1])  # High Card, reversed to sort by highest


    # Functions to determine specific poker hands
    def is_royal_flush(ranks, suits):
        return set(ranks) == {10, 11, 12, 13, 14} and len(set(suits)) == 1

    def is_straight_flush(ranks, suits):
        return is_straight(ranks) and is_flush(suits)

    def is_four_of_a_kind(ranks):
        return any(ranks.count(rank) == 4 for rank in ranks)

    def is_full_house(ranks):
        return len(set(ranks)) == 2 and any(ranks.count(rank) == 3  for rank in ranks)

    def is_flush(suits):
        return len(set(suits)) == 1

    def is_straight(ranks):
        return all(ranks[i] + 1 == ranks[i + 1] for i in range(4))

    def is_three_of_a_kind(ranks):
        return any(ranks.count(rank) == 3 for rank in ranks)

    def is_two_pair(ranks):
        return len(set(ranks)) == 3

    def is_one_pair(ranks):
        return len(set(ranks)) == 4

    # Get all 5-card combinations for each hand
    player_combinations = get_combinations(player_full_hand)
    opponent_combinations = get_combinations(opponent_full_hand)

    # Evaluate the best 5-card combination for each hand
    player_best_hand = max(player_combinations, key=evaluate_poker_hand)
    opponent_best_hand = max(opponent_combinations, key=evaluate_poker_hand)

    # Compare the evaluated values of the best hands
    player_best_value = evaluate_poker_hand(player_best_hand)
    opponent_best_value = evaluate_poker_hand(opponent_best_hand)

    # Determine the winner, considering the main hand value and kickers
    if player_best_value > opponent_best_value:
        return "Player wins!"
    elif player_best_value < opponent_best_value:
        return "Opponent wins!"
    else:
        # If main values are equal, compare the kickers
        player_kickers = player_best_value[1]
        opponent_kickers = opponent_best_value[1]

        if player_kickers > opponent_kickers:
            return "Player wins (kickers)!"
        elif player_kickers < opponent_kickers:
            return "Opponent wins (kickers)!"
        else:
            return "It's a tie!"


# Utility function to map card numbers to names
def get_card_name(card):
    card_dict = {
        11: "J",
        12: "Q",
        13: "K",
        14: "A",
    }
    card_number = card[0]
    card_suit = card[1]
    suit_dict = {
        1: "♠",
        2: "♥",
        3: "♦",
        4: "♣",
    }
    return f"{card_dict.get(card_number, card_number)}{suit_dict[card_suit]}"

# Function to load perceptrons from a file
def load_perceptrons(filename="perceptronObjects"):
    try:
        with open(filename, 'rb') as f:
            perceptrons = pickle.load(f)
        return perceptrons
    except FileNotFoundError:
        messagebox.showerror("Error", f"Perceptrons file '{filename}' not found. Please train perceptrons first.")
        raise SystemExit(1)  # Exit application gracefully
    except Exception as e:
        messagebox.showerror("Error", f"Error loading perceptrons: {str(e)}")
        raise SystemExit(1)  # Exit application gracefully

# Enum-like values to track game stages
PRE_FLOP = 0
FLOP = 1
TURN = 2
RIVER = 3
WINNER = 4
PLAYAGAIN = 5

# Basic GUI setup for Poker Texas Hold'em
class PokerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Poker Texas Hold'em")
        self.geometry("400x400")
         # Create an outer frame to simulate the red border
        border_width = 10  # Adjust the border width as desired
        self.outer_frame = tk.Frame(self, bg='red', padx=border_width, pady=border_width)  # Red border
        self.outer_frame.pack(fill=tk.BOTH, expand=True)  # Fill the window

        # Create an inner frame for the content
        self.inner_frame = tk.Frame(self.outer_frame, bg='green')  # Your original background color
        self.inner_frame.pack(fill=tk.BOTH, expand=True)  # Fill the inner frame
       
        self.perceptrons = load_perceptrons()  # Load perceptrons
        
        self.create_widgets()
        self.game_stage = PRE_FLOP  # Initialize game stage
        self.deck = []
        self.table = []

    def create_widgets(self):
        # Create poker game widgets with color customization
        self.player_hand_label = tk.Label(self.inner_frame, text="Player Hand:", bg='green', fg='white')  # Green with white text
        self.flop_label = tk.Label(self.inner_frame, text="Flop:", bg='green', fg='white')  # Green with white text
        self.turn_label = tk.Label(self.inner_frame, text="Turn:", bg='green', fg='white')  # Green with white text
        self.river_label = tk.Label(self.inner_frame, text="River:", bg='green', fg='white')  # Green with white text
        self.opponent_hand_label = tk.Label(self.inner_frame, text="Opponent Hand:", bg='green', fg='firebrick1')  # Green with white text
        
        self.deal_button = tk.Button(self.inner_frame, text="Deal", command=self.deal, bg='red', fg='black')  # Red for deal button
        
        self.result_label = tk.Label(self.inner_frame, text="", bg='green', fg='white')  # Green with white text
        
        # Pack widgets with padding
        self.player_hand_label.pack(pady=5)
        self.flop_label.pack(pady=5)
        self.turn_label.pack(pady=5)
        self.river_label.pack(pady=5)
        self.opponent_hand_label.pack(pady=5)
        self.deal_button.pack(pady=10)
        self.result_label.pack(pady=5)

    def clear_labels(self):
        # Clear all card-related labels
        self.player_hand_label.config(text="Player Hand:")
        self.flop_label.config(text="Flop:")
        self.turn_label.config(text="Turn:")
        self.river_label.config(text="River:")
        self.opponent_hand_label.config(text="Opponent Hand:")
        self.result_label.config(text="")
        
        self.player_hand_label.pack(pady=5)
        self.flop_label.pack(pady=5)
        self.turn_label.pack(pady=5)
        self.river_label.pack(pady=5)
        self.opponent_hand_label.pack(pady=5)
    def deal(self):
        if self.game_stage == PRE_FLOP:
            # Deal player and opponent hands
            self.player_table = []
            self.opponent_table = []
            self.player_hand = []
            self.opponent_hand = []
            self.table = []
            self.deck = create_deck()
            random.shuffle(self.deck)
            
            # Get player's hand
            self.player_hand = generate_preflop_hand(self.deck)
            player_hand_str = ", ".join([get_card_name(card) for card in self.player_hand])
            self.player_hand_label.config(text=f"Player Hand: {player_hand_str}")
            
            self.player_table.extend([card for sublist in self.player_hand for card in sublist])
            hand = np.array(self.player_table).reshape(1, -1)
            
            # Get opponent's hand
            self.opponent_hand = generate_preflop_hand(self.deck)
            opponent_hand_str = ", ".join([get_card_name(card) for card in self.opponent_hand])
            self.opponent_hand_label.config(text=f"Opponent Hand: {opponent_hand_str}")
            
            hand = np.array(self.player_table).reshape(1, -1)

            try:
                preflop_decision = self.perceptrons[0].predict(hand)
                if preflop_decision == 1:
                    self.result_label.config(text="POKER BOT says: Play on Pre-Flop")
                else:
                    self.result_label.config(text="POKER BOT says: Fold on Pre-Flop")
            except Exception as e:
                messagebox.showerror("Error", f"Perceptron prediction error on pre-flop: {str(e)}")
                return

            # Change Deal button text to "Deal Flop"
            self.deal_button.config(text="Deal Flop")
            self.game_stage = FLOP  # Move to next stage

        elif self.game_stage == FLOP:
            # Deal the flop and run perceptron decision
            flop = generate_flop(self.deck)  # The first three community cards
            self.table.extend([card for sublist in flop for card in sublist])
            flop_str = ", ".join([get_card_name(card) for card in flop])
            self.flop_label.config(text=f"Flop: {flop_str}")

            # Use perceptron to decide next step based on flop data
        
            self.player_table.extend([card for sublist in flop for card in sublist])
            hand = np.array(self.player_table).reshape(1, -1)

            try:
                flop_decision = self.perceptrons[1].predict(hand)
                if flop_decision == 1:
                    self.result_label.config(text="POKER BOT says: Play on Flop")
                else:
                    self.result_label.config(text="POKER BOT says: Fold on Flop")
            except Exception as e:
                messagebox.showerror("Error", f"Perceptron prediction error on flop: {str(e)}")
                return

            # Change Deal button text to "Deal Turn"
            self.deal_button.config(text="Deal Turn")
            self.game_stage = TURN

        elif self.game_stage == TURN:
            # Deal the turn and run perceptron prediction
              # Add a card for the turn
            turn = generate_turn(self.deck)
            turn_str = get_card_name(turn)
            self.turn_label.config(text=f"Turn: {turn_str}")
            self.table.extend([card for sublist in [turn] for card in sublist])
            self.player_table.extend([card for sublist in [turn] for card in sublist])
            hand = np.array(self.player_table).reshape(1, -1)

            try:
                turn_decision = self.perceptrons[2].predict(hand)
                if turn_decision == 1:
                    self.result_label.config(text="POKER BOT says: Play on Turn")
                else:
                    self.result_label.config(text="POKER BOT says: Fold on Turn")
            except Exception as e:
                messagebox.showerror("Error", f"Perceptron prediction error on turn: {str(e)}")
                return

            # Change Deal button text to "Deal River"
            self.deal_button.config(text="Deal River")
            self.game_stage = RIVER

        elif self.game_stage == RIVER:
            # Deal the river and run perceptron prediction
            river = generate_river(self.deck)
            river_str = get_card_name(river)
            self.river_label.config(text=f"River: {river_str}")

            self.table.extend([card for sublist in [river] for card in sublist])
            self.player_table.extend([card for sublist in [river] for card in sublist])
            hand = np.array(self.player_table).reshape(1, -1)

            try:
                river_decision = self.perceptrons[3].predict(hand)
                if river_decision == 1:
                    self.result_label.config(text="POKER BOT says: Play on River")
                else:
                    self.result_label.config(text="POKER BOT says: Fold on River")
            except Exception as e:
                messagebox.showerror("Error", f"Perceptron prediction error on river: {str(e)}")
                return
            
            self.deal_button.config(text="Decide Winner")
            self.game_stage = WINNER
        
            # Determine the winner
        elif self.game_stage == WINNER:
            print(self.player_hand)
            print(self.opponent_hand)
            print(self.table)
            winner = compare_poker_hands(self.player_hand,self.opponent_hand,self.table)
            
            self.result_label.config(text=winner)
                
            self.deal_button.config(text="Play Again")
            self.game_stage = PLAYAGAIN
        elif self.game_stage == PLAYAGAIN:
            # Change Deal button text to "Start New Game"
            self.clear_labels()
            self.game_stage = PRE_FLOP
        
# Create and run the GUI application
if __name__ == "__main__":
    app = PokerGUI()
    app.mainloop()
