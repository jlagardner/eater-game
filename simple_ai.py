import Tkinter as tk
import time
import math
import random
import sys
sys.path.insert(0, './background-research')
import games
#next: dynamically build q table as encounter new states
class q_table_learner:
    def __init__(self,environment,learning_rate,epsilon_rate,discount):
        self.env = environment
        self.learning_rate = learning_rate
        self.epsilon_rate = epsilon_rate
        self.discount = discount
        self.initialise_q_table()

    def initialise_q_table(self):
        self.q_table = []
        for state in range(self.env.number_of_possible_states):
            q_row = [None]*self.env.number_of_possible_actions
            for action in self.env.possible_actions_for_[state]:
                q_row[action] = 0
            self.q_table.append(list(q_row))

    def log_q_table(self):
        for row in self.q_table:
            print(row)

    def update_q_table(self):
        # newQ(moved from state, with action) = Q + learning rate * (reward for being in that state and taking that action + discount * max(Q for new state and all possible actions) - Q)
        current_state_number = self.env.current_state_number
        moved_from_state_number = self.env.moved_from_state_number
        Q = self.q_table[moved_from_state_number][self.env.action_made]
        newQ = Q *(1-self.learning_rate)
        newQ += self.learning_rate*self.env.current_reward
        q_row_for_allowed_actions = []
        for q in self.q_table[current_state_number]:
            if q is not None:
                q_row_for_allowed_actions.append(q)
        maxQ = max(q_row_for_allowed_actions)
        newQ += self.learning_rate*self.discount*maxQ
        self.q_table[moved_from_state_number][self.env.action_made] = newQ

    def choose_action(self,training):
        rand = random.uniform(0,1)
        q_row_for_allowed_actions = {}
        for i in range(self.env.number_of_possible_actions):
            if self.q_table[self.env.current_state_number][i] is not None:
                q_row_for_allowed_actions[i] = self.q_table[self.env.current_state_number][i]
        if training:
            if rand < self.epsilon:
                action = random.choice(list(q_row_for_allowed_actions.keys()))
            else:
                action = max(q_row_for_allowed_actions,key=q_row_for_allowed_actions.get)
        else:
            action = max(q_row_for_allowed_actions,key=q_row_for_allowed_actions.get)
        return action

    def train(self,episodes):
        self.epsilon = 1
        self.env.rendering = False
        for episode in range(episodes):
            print("training, on episode: {}, epsilon: {}".format(episode,self.epsilon))
            self.env.reset()
            while self.env.episode_ongoing():
                action_to_make = self.choose_action(training=True)
                self.env.do_action(action_to_make)
                #  move on to game self.measure_reward()
                self.update_q_table()
                if self.epsilon > 0.01:
                    self.epsilon -= self.epsilon_rate
            print("optimal route: {}".format(self.play(show=False)))

    def play(self,show):
        self.env.reset()
        if show:
            self.env.rendering = True
        route = [self.env.current_state_number]
        while self.env.episode_ongoing():
            if show:
                time.sleep(.5)
            action_to_make = self.choose_action(training=False)
            self.env.do_action(action_to_make)
            route.append(self.env.current_state_number)
            if stuck_in_loop(route):
                break
        if show:
            time.sleep(10)
        return route


def stuck_in_loop(list):
    if len(list) > 2:
        current_state = list[-1]
        if current_state in list[:-1]:
            return True
    return False

ioce_breaker = games.ice_maze_game()
qlearn = q_table_learner(ioce_breaker,0.1,0.0001,0.9)
qlearn.train(5000)
qlearn.play(True)
