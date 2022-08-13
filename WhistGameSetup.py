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
        self.score = 0
        self.user = False


def create_deck():
    lst = list(np.arange(0, 52))  # List representing a deck of cards
    random.shuffle(lst)
    return lst


def create_players(card_deck, num_players, number_cards):
    card_counter = 0
    bid_list = [0] * num_players
    lst = [Player("player's name", "list of cards", "bid number")] * num_players
    for player in range(num_players):
        name_str = "player" + str(player + 1)
        player_hand = card_deck[card_counter:number_cards + card_counter]
        player_hand.sort()
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
    # Finds suit of card selected
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


def play_card(hand, valid_suit, user):
    valid_cards = []
    for card in hand:
        if 13 * valid_suit <= card < 13 * (valid_suit + 1):
            valid_cards.append(card)
    if user:
        if not valid_cards:
            valid_cards = hand

        while True:
            print("Your hand: ", hand)
            print("Valid cards from your hand: ", valid_cards)
            try:
                played_card = int(input("Choose a valid card from your hand: "))
                if played_card in valid_cards:
                    break
                print("Please choose a valid card from list given")
            except ValueError:
                print("Please choose one of the valid cards and write it as an integer")

    else:
        if valid_cards:
            played_card = random.choice(valid_cards)
        else:
            played_card = random.choice(hand)
    return played_card


def play_round(game_info, start_player):
    num_players = len(game_info)  # Collect player information
    table_cards = [0] * num_players  # Cards on the table
    winning_pos = 0  # The position of the best player so far
    winning_player = start_player  # The player who won (not necessarily the same as position)

    for player in range(num_players):
        current_player = (player + start_player) % num_players
        current_hand = game_info[current_player].card
        is_user = game_info[current_player].user

        leading_suit = 4  # Invalid suit value on purpose
        if player != 0:
            leading_suit = get_suit(table_cards[0])

        if is_user:
            print("Current cards on the table: ", table_cards[:player])
        played_card = play_card(current_hand, leading_suit, is_user)

        game_info[current_player].card.remove(played_card)
        table_cards[current_player] = played_card

    for player in range(1, num_players):
        current_player = (player + start_player) % num_players
        if compare_cards(table_cards[winning_pos], table_cards[player], 5):
            winning_player = current_player
            winning_pos = player
    print(winning_pos)
    print('player', winning_player + 1)
    return table_cards, winning_player


def calculate_score(game_info):
    num_players = len(game_info)
    player_scores = [0] * num_players
    for player in range(num_players):
        player_scores[player] += game_info[player].score
        if game_info[player].score == game_info[player].bid:
            player_scores[player] += 10
    return player_scores


def get_user_input(input_range, info_string):
    while True:
        try:
            output_value = int(input("Choose a " + str(info_string) + " from " + str(input_range[0]) + " to "
                                     + str(input_range[1]) + ": "))
            if input_range[0] <= output_value <= input_range[1]:
                break
            print("Your input must be within the range stated")
        except ValueError:
            print("Input must be an integer between range stated")
    return output_value


user_input = True
while True:
    deck_of_cards = create_deck()
    if user_input:
        number_of_players = get_user_input([2, 6], "total number of players")
        card_limit = math.floor(52/number_of_players)
        number_of_cards = get_user_input([1, card_limit], "number of cards per person")
    else:
        number_of_players = 4
        number_of_cards = 13

    player_info = create_players(deck_of_cards, number_of_players, number_of_cards)
    print("Player 1 Hand ", player_info[0].card)
    print("Player 2 Hand ", player_info[1].card)
    print("Player 3 Hand ", player_info[2].card)
    print("Player 4 Hand ", player_info[3].card)

    if user_input:
        player_number = get_user_input([1, number_of_players], "player number")
        player_number -= 1

        print("Here is your hand: " + str(player_info[player_number].card))

        player_bid = get_user_input([0, number_of_cards], "bid")
        player_info[player_number].bid = player_bid
        player_info[player_number].user = True

    starting_player = 0

    while player_info[starting_player].card:
        table, starting_player = play_round(player_info, starting_player)
        player_info[starting_player].score += 1
        print(str(table))

    final_scores = calculate_score(player_info)

    print("Player 1 Score ", player_info[0].score)
    print("Player 2 Score ", player_info[1].score)
    print("Player 3 Score ", player_info[2].score)
    print("Player 4 Score ", player_info[3].score)
    print(final_scores)
    print("\n\n")

    if user_input:
        user_game_decision = input("Would you like to play another game? Type 'y' for yes, enter any key for no")
        if user_game_decision != "y":
            break

# Single Player Notes
# They choose their starting position (i.e what player they are from 1-4)
# They see their hand and choose a bid from 0 to the number of cards in their hand
# Play each round
# Find out their score
# Give them a choice to play another game with the same number of cards, one less, one more or to stop
