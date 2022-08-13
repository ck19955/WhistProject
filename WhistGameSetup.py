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
        while bid + sum_bids == len(player_hand):
            bid = random.randint(0, len(player_hand))
    return bid


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


def play_round(game_info, start_player):
    num_players = len(game_info)
    table_cards = [0]*num_players
    winning_pos = 0
    winning_player = 0

    for player in range(num_players):
        current_player = (player + start_player) % num_players
        current_hand = game_info[current_player].card
        played_card = random.choice(current_hand)
        game_info[current_player].card.remove(played_card)
        table_cards[current_player] = played_card

    for player in range(1, num_players):
        current_player = (player + start_player - 1) % num_players
        if compare_cards(table_cards[winning_pos], table_cards[player], 5):
            winning_player = current_player
            winning_pos = player
    print(winning_pos)
    return table_cards, winning_player


deck_of_cards = create_deck()
player_info = create_players(deck_of_cards, 4, 13)
starting_player = 0

while player_info[starting_player].card:
    table, starting_player = play_round(player_info, starting_player)
    print(str(table))




