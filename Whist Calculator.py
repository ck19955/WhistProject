# Whist Calculator
import numpy as np
import random


class Player:
    def __init__(self, name, card):
        self.name = name
        self.card = card


def create_deck():
    lst = list(np.arange(0, 52))
    random.shuffle(lst)
    return lst


def create_players(card_deck, num_players):
    lst = [Player("player1", card_deck[0])]*num_players
    for i in range(num_players):
        name_str = "player" + str(i+1)
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
    elif get_suit(card2) == trump_suit:
        return True
    else:
        return False


def play_round(info, trump_suit):
    best_player = 0

    for i in range(1, len(info)):
        if compare_cards(info[best_player].card, info[i].card, trump_suit):
            best_player = i
    return best_player


number_of_players = 4
suit_trump = 3
deck = create_deck()
player_info = create_players(deck, number_of_players)
print(deck)
print("Player " + str(play_round(player_info, suit_trump) + 1) + " Wins!")

