# Creates the setup for a game of whist.

# Inputs: Num of players, Num of cards per player, trump suit selected?, short deck?
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


def create_players(card_deck, num_players, number_cards):
    card_counter = 0
    lst = [Player("player1", card_deck[card_counter:number_cards + card_counter])] * num_players
    for player in range(num_players):
        name_str = "player" + str(player + 1)
        lst[player] = Player(name_str, card_deck[card_counter:number_cards + card_counter])
        if len(card_deck[card_counter:number_cards + card_counter]) != number_cards:
            raise ValueError("Not enough cards to deal between players, try reducing players or cards per player")
        card_counter += number_cards
    return lst


deck_of_cards = create_deck()
player_info = create_players(deck_of_cards, 4, 13)

