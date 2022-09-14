# Description: Runs a Monte Carlo simulation of the game of Texas Hold'em hands 
#              with two user-specified cards against a random hand.

import random
import argparse

# Returns true if card is a valid card in text format (Rank in [A,2,3,4,5,6,7,8,9,T,J,Q,K] and Suit in [h,d,c,s])
def is_valid_card(card):
    if len(card) != 2:
        return False
    if card[0] not in 'A23456789TJQKatjqk':
        return False
    if card[1] not in 'hdcsHDCS':
        return False
    return True

def hand_as_numeric(hand):
    # Converts alphanumeric hand to numeric values for easier comparisons, and sorts cards based on rank
    card_rank = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12, "t": 8, "j": 9, "q": 10, "k": 11, "a": 12}
    card_suit = {"c": 0, "d": 1, "h": 2, "s": 3, "C": 0, "D": 1, "H": 2, "S": 3}

    result = []
    for i in range (len(hand)//2):
        result.append([card_rank[hand[i*2]], card_suit[hand[i*2+1]]])
    result.sort()
    result.reverse()
    return result

def main():
    # Process command line arguments
    parser = argparse.ArgumentParser(description='Simulates a game of Texas Hold\'em with two cards.')
    parser.add_argument('--iterations', type=int, help='Number of iterations to run the simulation. For best results, use a large number. (>500)')
    parser.add_argument('--your_cards', type=str, help='Your two cards. Format: "2h3d"')
    args = parser.parse_args()
    if args.iterations < 500:
        print('Warning: Number of iterations is less than 500. Results may be inaccurate.')
    iterations = args.iterations

    if not is_valid_card(args.your_cards[0:2]):
        exit("Player 1 Card 1 Invalid")
    if not is_valid_card(args.your_cards[2:4]):
        exit("Player 1 Card 2 Invalid")

    player_hand = args.your_cards
    player_hand_numeric = hand_as_numeric(player_hand)
    print(player_hand_numeric)
    
if __name__ == "__main__":
    main()