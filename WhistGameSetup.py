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


def create_players(card_deck, num_players, number_cards, user_number, bid_dis):
    card_counter = 0
    bid_list = [0] * num_players
    lst = [Player("player's name", "list of cards", "bid number")] * num_players
    for player in range(num_players):
        name_str = "player" + str(player + 1)
        player_hand = card_deck[card_counter:number_cards + card_counter]
        player_hand.sort()

        if player == user_number:
            print("Here is your hand: ", hand_converter(player_hand))
            bid = get_user_input([0, number_of_cards], "bid")
        else:
            bid = bidding(player_hand, num_players - 1 - player, sum(bid_list), bid_dis)
        bid_list[player] = bid

        lst[player] = Player(name_str, player_hand, bid)
        if len(player_hand) != number_cards:
            raise ValueError("Not enough cards to deal between players, try reducing players or cards per player")
        card_counter += number_cards
    return lst


def bidding(player_hand, num_players_after, sum_bids, bid_dis):
    bidding_range = list(range(14))
    bid = np.random.choice(bidding_range, 1, p=bid_dis)
    if num_players_after == 0:
        while bid + sum_bids == len(player_hand):
            bid = np.random.choice(bidding_range, 1, p=bid_dis)
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
            print("Your hand: ", hand_converter(hand))
            print("Valid cards from your hand: ", hand_converter(valid_cards))
            print("Choice indicated by index : ", list(range(0, len(valid_cards))))
            try:
                played_card_index = int(input("Choose a valid card from your hand: "))
                if played_card_index < len(valid_cards):
                    played_card = valid_cards[played_card_index]
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
    table_cards = []  # Cards on the table
    winning_pos = 0  # The position of the best player so far
    winning_player = start_player  # The player who won (not necessarily the same as position)
    position_strings = ["st", "nd", "rd"]

    for player in range(num_players):
        current_player = (player + start_player) % num_players
        current_hand = game_info[current_player].card
        is_user = game_info[current_player].user

        leading_suit = 4  # Invalid suit value on purpose
        if player != 0:
            leading_suit = get_suit(table_cards[0])

        if is_user:
            if player < 3:
                placement = str(player + 1) + position_strings[player]
            else:
                placement = str(player + 1) + "th"
            print("You are playing " + placement)
            print("Current cards on the table: ", hand_converter(table_cards[:player]))
        played_card = play_card(current_hand, leading_suit, is_user)

        game_info[current_player].card.remove(played_card)
        table_cards.append(played_card)

    for player in range(1, num_players):
        current_player = (player + start_player) % num_players
        if compare_cards(table_cards[winning_pos], table_cards[player], 5):
            winning_player = current_player
            winning_pos = player
    #print('Winner of round is player', winning_player + 1)
    return table_cards, winning_player


def calculate_score(game_info):
    num_players = len(game_info)
    player_scores = [0] * num_players
    tricks_won = [0] * num_players
    for player in range(num_players):
        player_scores[player] += game_info[player].score
        tricks_won[player] = player_scores[player]
        if game_info[player].score == game_info[player].bid:
            player_scores[player] += 10
    return player_scores, tricks_won


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


def hand_converter(hand):
    suit_list = ["♣", "♦",  "♥", "♠"]
    card_list = ["J", "Q", "K", "A"]
    hand_list = [""]*len(hand)
    counter = 0

    for card in hand:
        suit_index = get_suit(card)
        card_suit = suit_list[suit_index]
        card = card % 13
        if card > 8:
            card_val = card_list[card - 9]
        else:
            card_val = str(card + 2)
        card_str = card_val + card_suit
        hand_list[counter] = card_str
        counter += 1

    return hand_list


if __name__ == "__main__":
    bidding_matrix = np.load("BiddingMatrix.npy")
    num_of_runs = 1000
    counter = 0
    user_input = False
    number_of_players = 4
    number_of_cards = 13
    collection_counter = 0
    player_number = number_of_players + 1  # Effectively an invalid player

    while True:
        counter += 1
        deck_of_cards = create_deck()
        if user_input:
            number_of_players = get_user_input([2, 6], "total number of players")
            card_limit = math.floor(52/number_of_players)
            number_of_cards = get_user_input([1, card_limit], "number of cards per person")
            player_number = get_user_input([1, number_of_players], "player number")
            player_number -= 1

        bidding_distribution = bidding_matrix[(13*(number_of_players - 2) + number_of_cards - 1)]
        player_info = create_players(deck_of_cards, number_of_players, number_of_cards, player_number, bidding_distribution)

        """
        print("\n\n")
        for player in range(number_of_players):
            print("Player " + str(player + 1) + " Hand ", hand_converter(player_info[player].card))
        print("\n\n")
        """
        if user_input:
            player_info[player_number].user = True

        starting_player = 0

        while player_info[starting_player].card:
            table, starting_player = play_round(player_info, starting_player)
            player_info[starting_player].score += 1
            #print(hand_converter(table))
            #print("Next Round!\n")

        final_scores, tricks_scores = calculate_score(player_info)

        for player in range(number_of_players):
            print("Player " + str(player + 1) + " tricks won: " + str(player_info[player].score) + "  Bid: "
                  + str(player_info[player].bid))
        print("Final scores for players ", final_scores)
        print("\n\n")

        if user_input:
            user_game_decision = input("Would you like to play another game? Type 'y' for yes, enter any key for no")
            if user_game_decision != "y":
                break
        if counter >= num_of_runs:
            break

