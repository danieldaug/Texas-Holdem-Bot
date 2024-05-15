import itertools
from perceptron import Perceptron
import pandas as pd
import numpy as np
import itertools
import os
import pickle
import random

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
        return 1
    elif player_best_value < opponent_best_value:
        return 0
    else:
        # If main values are equal, compare the kickers
        player_kickers = player_best_value[1]
        opponent_kickers = opponent_best_value[1]

        if player_kickers > opponent_kickers:
            return 1
        elif player_kickers < opponent_kickers:
            return 0
        else:
            return 1


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
def load_perceptrons(filename="perceptronObjects"):
    try:
        with open(filename, 'rb') as f:
            perceptrons = pickle.load(f)
        return perceptrons
    except FileNotFoundError:
        print("Error", f"Perceptrons file '{filename}' not found. Please train perceptrons first.")
        raise SystemExit(1)  # Exit application gracefully
    except Exception as e:
        print("Error", f"Error loading perceptrons: {str(e)}")
        raise SystemExit(1)  # Exit application gracefully
    
    
def main():
    perceptrons = load_perceptrons()
    trials = int(input("How many trials would you like to test:"))
    preflopS = 0
    flopS = 0
    turnS = 0
    riverS = 0
    totalS = 0
    noFoldS = 0
    for i in range(trials):
       # Deal player and opponent hands
        player_table = []
        opponent_table = []
        player_hand = []
        opponent_hand = []
        table = []
        deck = create_deck()
        random.shuffle(deck)
        
        # Get player's hand
        player_hand = generate_preflop_hand(deck)
        
        player_table.extend([card for sublist in player_hand for card in sublist])
        
        # Get opponent's hand
        opponent_hand = generate_preflop_hand(deck)
    
        hand = np.array(player_table).reshape(1, -1)

        
        preflop_decision = perceptrons[0].predict(hand)

        # Deal the flop and run perceptron decision
        flop = generate_flop(deck)  # The first three community cards
        table.extend([card for sublist in flop for card in sublist])
    
        # Use perceptron to decide next step based on flop data
        player_table.extend([card for sublist in flop for card in sublist])
        hand = np.array(player_table).reshape(1, -1)

        
        flop_decision = perceptrons[1].predict(hand)

        turn = generate_turn(deck)

        
        table.extend([card for sublist in [turn] for card in sublist])
        player_table.extend([card for sublist in [turn] for card in sublist])
        hand = np.array(player_table).reshape(1, -1)

 
        turn_decision = perceptrons[2].predict(hand)
           
        river = generate_river(deck)


        table.extend([card for sublist in [river] for card in sublist])
        player_table.extend([card for sublist in [river] for card in sublist])
        hand = np.array(player_table).reshape(1, -1)


        river_decision = perceptrons[3].predict(hand)
    
        # Determine the winner
        winner = compare_poker_hands(player_hand,opponent_hand,table)
        
        if winner == 1 and preflop_decision == 1 or winner != 1 and preflop_decision != 1:
            preflopS += 1
        if winner == 1 and flop_decision == 1 or winner != 1 and flop_decision != 1:
            flopS += 1
        if winner == 1 and turn_decision == 1 or winner != 1 and turn_decision != 1:
            turnS += 1
        if winner == 1 and river_decision == 1 or winner != 1 and river_decision != 1:
            riverS += 1
        if (winner == 1 and  river_decision == 1 and turn_decision == 1 and flop_decision == 1 and preflop_decision == 1) or (winner !=1 and (river_decision != 1 or winner !=1) and (turn_decision != 1) or (winner !=1 and flop_decision != 1)  or (winner !=1 and preflop_decision != 1)):
            totalS += 1
        if (winner == 1 and  river_decision == 1 and turn_decision == 1 and flop_decision == 1 and preflop_decision == 1):
            noFoldS += 1
    
    preflopA = preflopS / trials
    flopA = flopS / trials
    turnA = turnS / trials
    riverA = riverS / trials
    totalA = totalS / trials
    totalNoFoldA = noFoldS / trials
    print(f'The preflop Accuracy is {preflopA}')
    print(f'The flop Accuracy is {flopA}')
    print(f'The turn Accuracy is {turnA}')
    print(f'The river Accuracy is {riverA}')
    print(f'The total Accuracy is {totalA}')
    print(f'The total Accuracy with no Fold {totalNoFoldA}')

main()