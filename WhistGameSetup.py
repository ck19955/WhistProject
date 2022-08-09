# Creates the setup for a game of whist.

# Inputs: Num of players, Num of cards per player, trump suit selected?, short deck?
import numpy as np
import random
import math


class Player:
    def __init__(self, name, card, bid):
        self.name = name
        self.card = card
        self.bid = bid


def create_deck():
    lst = list(np.arange(0, 52))
    random.shuffle(lst)
    return lst


def create_players(card_deck, num_players, number_cards):
    card_counter = 0
    bid_list = [0]*num_players
    lst = [Player("player's name", "list of cards", "bid number")] * num_players
    for player in range(num_players):
        name_str = "player" + str(player + 1)
        player_hand = card_deck[card_counter:number_cards + card_counter]
        bid = bidding(player_hand, num_players - 1 - player, sum(bid_list))
        bid_list[player] = bid
        lst[player] = Player(name_str, player_hand, bid)
        if len(player_hand) != number_cards:
            raise ValueError("Not enough cards to deal between players, try reducing players or cards per player")
        card_counter += number_cards
    return lst


def bidding(player_hand, num_players_after, sum_bids):
    bid = random.randint(0, len(player_hand))
    if num_players_after == 0:
        print("wow")
        while bid + sum_bids == len(player_hand):
            bid = random.randint(0, len(player_hand))
    return bid


deck_of_cards = create_deck()
player_info = create_players(deck_of_cards, 4, 13)



