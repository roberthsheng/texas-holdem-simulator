# Description: Runs a Monte Carlo simulation of the game of Texas Hold'em hands 
#              with two user-specified cards against a random hand.

import random
import argparse

def copy_hand(cards):
    #
    # Returns copy of hand (replaces deepcopy with 20x speed improvement)
    #
    results = []
    for i in cards:
        results.append(i)
    return results

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

def check_flush(hand):
    #
    # Returns True if hand is a Flush, otherwise returns False
    #
    hand_suit = [hand[0][1], hand[1][1], hand[2][1], hand[3][1], hand[4][1]]
    for i in range(4):
        if hand_suit.count(i) == 5:
            return True
    return False


def check_straight(hand):
    # Return True if hand is a Straight, otherwise returns False
    if hand[0][0] == (hand[1][0] + 1) == (hand[2][0] + 2) == (hand[3][0] + 3)\
            == (hand[4][0] + 4):
        return True
    elif (hand[0][0] == 12) and (hand[1][0] == 3) and (hand[2][0] == 2)\
            and (hand[3][0] == 1) and (hand[4][0] == 0):
        return True
    return False


def check_straightflush(hand):
    # Return True if hand is a Straight Flush, otherwise returns False
    if check_flush(hand) and check_straight(hand):
        return True
    return False


def check_fourofakind(hand):
    # Return True if hand is Four-of-a-Kind, otherwise returns False
    # Also returns rank of four of a kind card and rank of fifth card
    # (garbage value if no four of a kind)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for quad_card in range(13):
        if hand_rank.count(quad_card) == 4:
            for kicker in range(13):
                if hand_rank.count(kicker) == 1:
                    return True, quad_card, kicker
    return False, 13, 13


def check_fullhouse(hand):
    # Return True if hand is a Full House, otherwise returns False
    # Also returns rank of three of a kind card and two of a kind card
    # (garbage values if no full house)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for trip_card in range(13):
        if hand_rank.count(trip_card) == 3:
            for pair_card in range(13):
                if hand_rank.count(pair_card) == 2:
                    return True, trip_card, pair_card
    return False, 13, 13


def check_threeofakind(hand):
    # Return True if hand is Three-of-a-Kind, otherwise returns False
    # Also returns rank of three of a kind card and remaining two cards
    # (garbage values if no three of a kind)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for trip_card in range(13):
        if hand_rank.count(trip_card) == 3:
            for n in range(13):
                if hand_rank.count(n) == 1:
                    for m in range(n+1, 13):
                        if hand_rank.count(m) == 1:
                            return True, trip_card, [m, n]
    return False, 13, [13, 13]


def check_twopair(hand):
    # Return True if hand is Two Pair, otherwise returns False
    # Also returns ranks of paired cards and remaining card
    # (garbage values if no two pair)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for low_pair_card in range(13):
        if hand_rank.count(low_pair_card) == 2:
            for high_pair_card in range(low_pair_card + 1, 13):
                if hand_rank.count(high_pair_card) == 2:
                    for kicker in range(13):
                        if hand_rank.count(kicker) == 1:
                            return True, [high_pair_card, low_pair_card], \
                                kicker
    return False, [13, 13], 13


def check_onepair(hand):
    # Return True if hand is One Pair, otherwise returns False
    # Also returns ranks of paired cards and remaining three cards
    # (garbage values if no pair)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for pair_card in range(13):
        if hand_rank.count(pair_card) == 2:
            for kicker1 in range(13):
                if hand_rank.count(kicker1) == 1:
                    for kicker2 in range(kicker1 + 1, 13):
                        if hand_rank.count(kicker2) == 1:
                            for kicker3 in range(kicker2 + 1, 13):
                                if hand_rank.count(kicker3) == 1:
                                    return True, pair_card, \
                                        [kicker3, kicker2, kicker1]
    return False, 13, [13, 13, 13]


def highest_card(hand1, hand2):
    # Return 0 if hand1 is higher
    # Return 1 if hand2 is higher
    # Return 2 if equal
    hand1_rank = \
        [hand1[0][0], hand1[1][0], hand1[2][0], hand1[3][0], hand1[4][0]]
    hand2_rank = \
        [hand2[0][0], hand2[1][0], hand2[2][0], hand2[3][0], hand2[4][0]]
    #
    # Compare
    #
    if hand1_rank > hand2_rank:
        return 0
    elif hand1_rank < hand2_rank:
        return 1
    return 2


def highest_card_straight(hand1, hand2):
    # Return 0 if hand1 is higher
    # Return 1 if hand2 is higher
    # Return 2 if equal
    #
    # Compare second card first (to account for Ace low straights)
    # if equal, we could have Ace low straight, so compare first card.
    # If first card is Ace, that is the lower straight
    #
    if hand1[1][0] > hand2[1][0]:
        return 0
    elif hand1[1][0] < hand2[1][0]:
        return 1
    elif hand1[0][0] > hand2[0][0]:
        return 1
    elif hand1[0][0] < hand2[0][0]:
        return 0
    return 2

def compare_hands(hand1, hand2):
    # Compares two hands and returns 1 if hand1 is better, 2 if hand2 is better, and 0 if they are equal
    result1 = []
    result2 = []

    # Check for straight flush
    if check_straightflush(hand1):
        if check_straightflush(hand2):
            return(highest_card_straight(hand1, hand2))
        else:
            return 0
    elif check_straightflush(hand2):
            return 1
    #
    # Check for four of a kind
    #
    result1 = check_fourofakind(hand1)
    result2 = check_fourofakind(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    #
    # Check for full house
    #
    result1 = check_fullhouse(hand1)
    result2 = check_fullhouse(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    #
    # Check for flush
    #
    if check_flush(hand1):
        if check_flush(hand2):
            return(highest_card(hand1, hand2))
        else:
            return 0
    elif check_flush(hand2):
        return 1
    #
    # Check for straight
    #
    if check_straight(hand1):
        if check_straight(hand2):
            temp = highest_card_straight(hand1, hand2)
            return temp
        else:
            return 0
    elif check_straight(hand2):
        return 1
    #
    # Check for three of a kind
    #
    result1 = check_threeofakind(hand1)
    result2 = check_threeofakind(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    #
    # Check for two pair
    #
    result1 = check_twopair(hand1)
    result2 = check_twopair(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    #
    # Check for one pair
    #
    result1 = check_onepair(hand1)
    result2 = check_onepair(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    return (highest_card(hand1, hand2))


def best_five(hand, community):
    #
    # Takes hand and community cards in numeric form
    # Returns best five cards
    #
    currentbest = copy_hand(community)
    currentbest.sort()
    currentbest.reverse()
    #
    # Compare current best to five cards including only one player card
    #
    for m in range(2):
        for n in range(5):
            comparehand = copy_hand(community)
            comparehand[n] = hand[m]
            comparehand.sort()
            comparehand.reverse()
            if compare_hands(currentbest, comparehand) == 1:
                currentbest = copy_hand(comparehand)
    #
    # Compare current best to five cards including both player cards
    #
    for m in range(5):
        for n in range(m + 1, 5):
            comparehand = copy_hand(community)
            comparehand[m] = hand[0]
            comparehand[n] = hand[1]
            comparehand.sort()
            comparehand.reverse()
            if compare_hands(currentbest, comparehand) == 1:
                currentbest = copy_hand(comparehand)
    return currentbest

def create_random_hand(numcards):
    # Creates a random hand
    hand = []
    for i in range(numcards):
        card = []
        card.append(random.randint(0, 12))
        card.append(random.randint(0,3))
        hand.append(card)
    return hand

def intersection(lst1, lst2, lst3):
    tup1 = map(tuple, lst1)
    tup2 = map(tuple, lst2) 
    tup3 = map(tuple, lst3)
    return list(map(list, set(tup1).intersection(tup2).intersection(tup3)))

def create_randomized_cards(player_hand_numeric):
    while True:
        opponent_hand_numeric = create_random_hand(2)
        if (player_hand_numeric != opponent_hand_numeric):
            break

    while True:
        community_cards_numeric = create_random_hand(5)
        if intersection(player_hand_numeric, opponent_hand_numeric, community_cards_numeric) == []:
            break
    
    return opponent_hand_numeric, community_cards_numeric

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

    opponent_hand_numeric, community_cards_numeric = create_randomized_cards(player_hand_numeric)

    # Initialize counters
    totals = [0, 0, 0]
    # Monte Carlo Simulation
    for _ in range(iterations):
        best_hand1 = best_five(player_hand_numeric, community_cards_numeric)
        best_hand2 = best_five(opponent_hand_numeric, community_cards_numeric)

        while True:
            opponent_hand_numeric = create_random_hand(2)
            if (player_hand_numeric != opponent_hand_numeric):
                break

        while True:
            community_cards_numeric = create_random_hand(5)
            if intersection(player_hand_numeric, opponent_hand_numeric, community_cards_numeric) == []:
                break

        totals[compare_hands(best_hand1, best_hand2)] += 1
    # Print results
    print ("Total Hands: %i" % (iterations))
    print ("Hand1: %i Hand2: %i Ties: %i" % (totals[0], totals[1], totals[2]))
    print ("Hand1: %.2f%% Hand2: %.2f%% Ties: %.2f%%" % \
        (100 * round((totals[0] / (iterations + 0.0)), 4),
         100 * round((totals[1] / (iterations + 0.0)), 4),
         100 * round((totals[2] / (iterations + 0.0)), 4)))

    
if __name__ == "__main__":
    main()