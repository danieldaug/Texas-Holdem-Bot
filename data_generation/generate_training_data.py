from trainingbot import DummyBot
def main():
    user_in = input("How many records would you like to generate? ")
    record_num = int(user_in.strip().split()[0])
    pre_flop_f = input("What would you like the name of the pre-flop data file to be? ")
    flop = input("The flop data file? ")
    turn = input("The turn data file? ")
    river = input("The river data file? ")
    try:
        pre_flop = open(pre_flop_f, 'w')
        flop = open(flop, 'w')
        turn = open(turn, 'w')
        river = open(river, 'w')
        for _ in range(record_num):
            dummy = DummyBot()
            #simulate game to create data record
            dummy.generate_hand_and_table()
            hand = dummy.get_hand()
            table = dummy.get_table()
            for card in hand:
                pre_flop.write(str(card[0]) + "," + str(card[1]) + ",")
                flop.write(str(card[0]) + "," + str(card[1]) + ",")
                turn.write(str(card[0]) + "," + str(card[1]) + ",")
                river.write(str(card[0]) + "," + str(card[1]) + ",")
            for card in table:
                flop.write(str(card[0]) + "," + str(card[1]) + ",")
                turn.write(str(card[0]) + "," + str(card[1]) + ",")
                river.write(str(card[0]) + "," + str(card[1]) + ",")
            
            #4 opponents
            dummy.generate_opponent()
            dummy.generate_opponent()
            dummy.generate_opponent()
            dummy.generate_opponent()
            #dummy.generate_opponent()

            dummy.generate_cards()
            card = dummy.get_table()[-1]
            turn.write(str(card[0]) + "," + str(card[1]) + ",")
            river.write(str(card[0]) + "," + str(card[1]) + ",")
            
            dummy.generate_cards()
            card = dummy.get_table()[-1]
            river.write(str(card[0]) + "," + str(card[1]) + ",")
            
            winner = dummy.decide_winner()
            pre_flop.write(str(winner) + "\n")
            flop.write(str(winner) + "\n")
            turn.write(str(winner) + "\n")
            river.write(str(winner) + "\n")

        pre_flop.close()
        flop.close()
        turn.close()
        river.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()