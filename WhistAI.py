# Creates and Trains Whist AI

# CODE LAYOUT
# Create deck (perhaps make it short deck?)
# Create AI Player who will play for all positions

import numpy as np
from WhistGameSetup import create_deck, create_players, bidding, get_suit, compare_cards, calculate_score

if __name__ == "__main__":

    # -------------------------------------------------- GAME SET-UP --------------------------------------------------
    bidding_matrix = np.load("BiddingMatrix.npy")  # Distribution of how AI bids
    num_of_runs = 1000  # Number of simulations
    counter = 0
    user_input = False  # If we are using a user input (almost never)
    number_of_players = 4
    number_of_cards = 13
    player_number = number_of_players + 1  # Effectively an invalid player

    deck_of_cards = create_deck()  # Creating a deck of cards

    # Choosing the bidding distribution required for the number of players and number of cards
    bidding_distribution = bidding_matrix[(13*(number_of_players - 2) + number_of_cards - 1)]

    # Creating the players with their properties
    player_info = create_players(deck_of_cards, number_of_players, number_of_cards, player_number, bidding_distribution)

