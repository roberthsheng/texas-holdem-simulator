# Description: Runs a Monte Carlo simulation of the game of Texas Hold'em hands 
#              with two user-specified cards against a random hand.

import random
import argparse

rank = ['A23456789TJQKatjqk']
suit = ['hdcsHDCS']

# Returns true if card is a valid card in text format (Rank in [A,2,3,4,5,6,7,8,9,T,J,Q,K] and Suit in [h,d,c,s])
def is_valid_card(card):
    if len(card) != 2:
        return False
    if card[0] not in 'A23456789TJQKatjqk':
        return False
    if card[1] not in 'hdcsHDCS':
        return False
    return True




def main():
    # Process command line arguments
    parser = argparse.ArgumentParser(description='Simulates a game of Texas Hold\'em with two cards.')
    parser.add_argument('iterations', metavar = 'num_iters',type=int, help='Number of iterations to run the simulation. For best results, use a large number. (>500)')
    parser.add_argument('--your_cards', type=str, help='Your two cards. Format: "2h3d"')
    args = parser.parse_args()
    if args.num_iters < 500:
        print('Warning: Number of iterations is less than 500. Results may be inaccurate.')
    iterations = args.num_iters

    if not is_valid_card(args.your_cards[0:2]):
        exit("Player 1 Card 1 Invalid")
    if not is_valid_card(args.your_cards[2:4]):
        exit("Player 1 Card 2 Invalid")

    player_hand = args.your_cards
    
