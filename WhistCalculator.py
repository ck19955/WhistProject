# Whist Calculator
import numpy as np
import random
import math


class Player:
    def __init__(self, name, card):
        self.name = name
        self.card = card


def create_deck():
    lst = list(np.arange(0, 52))
    random.shuffle(lst)
    return lst


def create_players(card_deck, num_players):
    lst = [Player("player1", card_deck[0])] * num_players
    for player in range(num_players):
        name_str = "player" + str(player + 1)
        lst[player] = Player(name_str, card_deck[player])
    return lst


def get_suit(card_number):
    if card_number < 13:
        return 0
    elif 13 <= card_number < 26:
        return 1
    elif 26 <= card_number < 39:
        return 2
    else:
        return 3


def compare_cards(card1, card2, trump_suit):
    if get_suit(card1) == get_suit(card2) and card2 > card1:
        return True
    elif get_suit(card2) == trump_suit and get_suit(card1) != trump_suit:
        return True
    else:
        return False


def play_round(info, trump_suit):
    best_player = 0

    for player in range(1, len(info)):
        if compare_cards(info[best_player].card, info[player].card, trump_suit):
            best_player = player
    return best_player


def calculate_bid(info, player, trump_suit):
    player_card = info[player].card
    player_suit = get_suit(player_card)
    num_cards = 51
    num_players = len(info)
    extra_prob = 1
    if player_suit == trump_suit:
        lose_cards = num_cards - 12 + (player_card % 13)
    else:
        if player_suit != trump_suit:  # If target player isn't playing first
            # Calculate the probability that the first player has the same suit as the target player
            num_players -= 1
            extra_prob = (player_card % 13) / num_cards
            num_cards -= 1
        lose_cards = num_cards - 13 - 12 + (player_card % 13)
    probability = extra_prob * (math.factorial(lose_cards) / math.factorial(lose_cards - num_players) *
                                math.factorial(num_cards - num_players) / math.factorial(num_cards))

    if probability >= 0.5:
        return 1  # Predicted to win
    else:
        return 0  # Predicted to lose


def collect_bids(info, num_players, trump_suit):
    bid_list = np.zeros(num_players)
    for player in range(num_players):
        bid = calculate_bid(info, player, trump_suit)  # Calculate bid
        if player == num_players - 1 and bid + sum(bid_list) == 1:  # Makes sure that players wont allow for all players
            # to make their bid
            bid_list[player] = 1 - bid  # Adjustment
        else:
            bid_list[player] = bid
    return bid_list


def collect_scores(winner, num_players, bids):
    bonus_winners_list = np.zeros(num_players)
    bonus_winners_list[winner] = 1
    diff = bonus_winners_list - bids
    bonus_winners = np.where(diff == 0)[0]
    return bonus_winners


# Set up globals
number_of_players = 5
num_runs = 1000
scores = np.zeros(number_of_players)

for i in range(num_runs):
    # Info for this run
    suit_trump = random.randint(0, 4)  # Random suit of the four suits
    deck = create_deck()  # Create a random deck
    player_info = create_players(deck, number_of_players)  # Give players a card
    bidding_list = collect_bids(player_info, number_of_players, suit_trump)  # Calculate each players bids

    # Winning player calculation
    winning_player = play_round(player_info, suit_trump)

    # Find who bidded correctly
    correct_players = collect_scores(winning_player, number_of_players, bidding_list)

    # Add scores to the cumulative count
    for j in correct_players:
        scores[j] += 10
    scores[winning_player] += 1

print("Best Possible Score: " + str(num_runs * 11))
print("Result: " + str(scores))
