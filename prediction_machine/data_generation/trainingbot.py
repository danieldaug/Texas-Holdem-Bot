#python file for creating poker dummy bot in order to create training input data
import random
from enum import Enum

class Hand(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

    # Define less-than comparison
    def __lt__(self, other):
        if isinstance(other, Hand):
            return self.value < other.value
        return NotImplemented

    # Define less-than-or-equal-to comparison
    def __le__(self, other):
        if isinstance(other, Hand):
            return self.value <= other.value
        return NotImplemented

    # Define greater-than comparison
    def __gt__(self, other):
        if isinstance(other, Hand):
            return self.value > other.value
        return NotImplemented

    # Define greater-than-or-equal-to comparison
    def __ge__(self, other):
        if isinstance(other, Hand):
            return self.value >= other.value
        return NotImplemented


class DummyBot:
   
    def __init__(self):
        self.hand = [] #dummy hand
        self.table = [] #cards on table
        self.suits = [set() for _ in range(12)] #tracks any repeated card generations
        self.opponents = [] #opponent hand
        

    #generate dummy's hand and flop
    def generate_hand_and_table(self):
        #hand
        for i in range(2):
            card = random.randint(2,14) #14 technically counts as 1 and 14 (ace)
            suit = random.randint(1,4)
            while suit in self.suits[card-3]: #check for existing card
                suit = ((suit)%4)+1
            self.suits[card-3].add(suit)
            self.hand.append((card,suit)) 
        
        #flop
        for i in range(3):
            card = random.randint(2,14)
            suit = random.randint(1,4)
            while len(self.suits[card-3]) == 4: #make sure not more than 4 of card number/face
                card = random.randint(2,14)
            while suit in self.suits[card-3]: #check for existing card
                suit = ((suit)%4)+1
            self.suits[card-3].add(suit)
            self.table.append((card,suit))


    #generate opponent for chance of losing/winning
    def generate_opponent(self):
        self.opponents.append([])
        for i in range(2):
            card = random.randint(2,14) #14 technically counts as 1 and 14 (ace)
            suit = random.randint(1,4)
            while len(self.suits[card-3]) == 4: #make sure not more than 4 of card number/face
                card = random.randint(2,14)
            while suit in self.suits[card-3]: #check for existing card
                suit = ((suit)%4)+1
            self.suits[card-3].add(suit)
            self.opponents[-1].append((card,suit)) 

    #generate another table card each round
    def generate_cards(self):
        card = random.randint(2,14)
        suit = random.randint(1,4)
        while len(self.suits[card-3]) == 4: #make sure not more than 4 of card number/face
            card = random.randint(2,14)
        while suit in self.suits[card-3]: #check for existing card
            suit = ((suit)%4)+1
        self.suits[card-3].add(suit)
        self.table.append((card,suit))

    def decide_winner(self):
        if len(self.hand + self.table) < 5 and len(self.opponents) < 1:
            print("not enough cards")
            return
        else:
            #create own hand
            bot_hand = self.check_hand(self.hand + self.table)
            #create opponent hands
            op_hands = []
            for o in self.opponents:
                op_hands.append(self.check_hand(o + self.table))

            res = 1
            #check if opponent has better hand
            for hand in op_hands:
                if hand[0] > bot_hand[0]:
                    return -1
                elif hand[0] == bot_hand[0]:
                    if hand[0] != Hand.STRAIGHT and hand[0] != Hand.FLUSH and hand[0] != Hand.STRAIGHT_FLUSH and hand[0] != Hand.ROYAL_FLUSH:
                        if hand[2] < bot_hand[2]:
                            res = 1
                        elif hand[2] > bot_hand[2]:
                            return -1
                        elif hand[1] > bot_hand[1]:
                            return -1
                    elif hand[1] > bot_hand[1]:
                        return -1
                    elif hand[1] == bot_hand[1]:
                        res = 1
            #if not, bot wins
            return res


    def check_hand(self, hand):
        card_nums = [x[0] for x in hand]
        card_nums += [x[0] for x in self.table]
        card_nums.sort()
        card_suits = [x[1] for x in hand]
        card_suits += [x[1] for x in self.table]

        high = card_nums[-1]
        combo = Hand.HIGH_CARD
        #check for duplicate combos
        new_val = False
        combo_high = 0
        for i in range(1,len(card_nums)):
            if card_nums[i] == card_nums[i-1] and new_val == False:
                if combo == Hand.HIGH_CARD:
                    combo = Hand.PAIR
                    combo_high = card_nums[i]
                elif combo == Hand.PAIR:
                    combo = Hand.THREE_KIND
                    combo_high = card_nums[i]
                elif combo == Hand.THREE_KIND:
                    combo = Hand.FOUR_KIND
                    combo_high = card_nums[i]
            elif card_nums[i] == card_nums[i-1] and new_val:
                if combo == Hand.HIGH_CARD:
                    combo = Hand.PAIR
                    combo_high = card_nums[i]
                elif combo == Hand.PAIR:
                    combo = Hand.TWO_PAIR
                    combo_high = max(combo_high, card_nums[i])
                elif combo == Hand.THREE_KIND:
                    combo = Hand.FULL_HOUSE
            elif card_nums[i] != card_nums[i-1] and combo != Hand.HIGH_CARD:
                new_val = True

        #check for same suit
        suit = card_suits[0]
        flush = True
        for i in range(1,len(card_suits)):
            if card_suits[i] != suit:
                flush = False
        
        #check for straight
        straight = False
        if combo == Hand.HIGH_CARD:
            straight = True
            for i in range(1,len(card_nums)):
                if card_nums[i] != card_nums[i-1]+1 and not (card_nums[i-1] == 14 and card_nums[i] == 2):
                    straight = False
                
        if straight and flush:
            if card_nums[-1] == 14:
                combo = Hand.ROYAL_FLUSH
            else:
                combo = Hand.STRAIGHT_FLUSH
        elif combo != Hand.FOUR_KIND and combo != Hand.FULL_HOUSE:
            if flush:
                combo = Hand.FLUSH
            elif straight:
                combo = Hand.STRAIGHT

        return (combo, high, combo_high)
    
    def get_hand(self):
        return self.hand
    
    def get_table(self):
        return self.table
    
    def get_opponents(self):
        return self.opponents