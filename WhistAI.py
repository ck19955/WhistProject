# Creates and Trains Whist AI

# CODE LAYOUT
# Create deck (perhaps make it short deck?)
# Create AI Player who will play for all positions

# NOTES TO SELF:
# - Make sure rewards are values less than 1


import random
import time
import numpy as np
import tensorflow as tf
import keras
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D
from tensorflow.keras.models import load_model
from collections import deque

from WhistGameSetup import create_deck, create_players, bidding, get_suit, compare_cards, calculate_score


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.6
        self.epsilon = 0.9995
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.009
        self.tau = 0.125
        self.model = self.build_model()
        self.target_model = self.build_model()

    def build_model(self):
        self.state_size = np.reshape(self.state_size, (1, 9))
        model = Sequential()
        model.add(Dense(9, input_shape=(self.state_size.shape[1],), activation="relu"))
        model.add(Dense(18, activation="relu"))
        model.add(Dense(9, activation="linear"))
        model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def act_decision(self):
        if random.random() <= self.epsilon:
            return "random"
        else:
            return "neural network"

    def replay(self, batch_size):
        # Training the neural network
        minibatch = random.sample(memory, batch_size)
        for state, action, reward, next_state, done, test_probability_matrix in minibatch:
            if not done:
                # print("reward: ", reward)

                # Predicted future Q-values
                prediction_for_next_state = self.target_model.predict(np.reshape(next_state, (1, 9)))[0]

                # Maximum Q-value for current state using max future Q-value
                target_q_value = reward + self.gamma * np.amax(prediction_for_next_state)
            else:
                target_q_value = reward

            # Calculating difference in Q-values
            q_value_nn_prediction = self.target_model.predict(np.reshape(state, (1, 9)))  # Current NN prediction
            q_value_nn_prediction = np.reshape(q_value_nn_prediction, (3, 3))
            q_value_nn_prediction[action[0], action[1]] = target_q_value  # New Q-value for specified action
            q_value_nn_prediction = np.reshape(q_value_nn_prediction, (1, 9))

            # Readjusting model for new Q-value learnt
            self.model.fit(np.reshape(state, (1, 9)), q_value_nn_prediction, epochs=1, verbose=0)
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)


if __name__ == "__main__":
    memory = []

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

