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
    for i in range(num_players):
        name_str = "player" + str(i + 1)
        lst[i] = Player(name_str, card_deck[i])
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

    for i in range(1, len(info)):
        if compare_cards(info[best_player].card, info[i].card, trump_suit):
            best_player = i
    return best_player


def calculate_bid(info, trump_suit):
    player1_card = info[0].card
    player1_suit = get_suit(player1_card)
    num_players = len(info)

    if player1_suit == trump_suit:
        winning_cards = 12 - (player1_card % 13)
    else:
        winning_cards = 13 + 12 - (player1_card % 13)
    probability = (pow(51 - winning_cards, num_players)) * math.factorial(51 - num_players) / math.factorial(51)
    print("Probability to win: " + str(probability))
    if probability >= 0.5:
        return True
    else:
        return False


number_of_players = 4
suit_trump = 3
deck = create_deck()
player_info = create_players(deck, number_of_players)
winning_player = play_round(player_info, suit_trump)
print(deck)
print("Player " + str(winning_player + 1) + " Wins!")

if calculate_bid(player_info, suit_trump):
    print("Predicted to win")
    if winning_player == 0:
        print("Bonus 10 points!")

elif winning_player != 0:
    print("Bonus 10 points!")

