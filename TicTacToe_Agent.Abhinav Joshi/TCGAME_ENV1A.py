from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():
    def __init__(self):

        # initialise state as an array
        self.state = [np.nan for _ in range(9)] # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = list(range(1, len(self.state) + 1)) # , can initialise to an array or matrix

        self.reset()

    def reset(self):
        return self.state


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        # (s[0] + s[1] + s[2]) == 15
        # 0 1 2
        # 3 4 5
        # 6 7 8
        winning_combination = [(0,1,2),(0,3,6),(0,4,8),(1,4,7),(2,4,6),(2,5,8),(3,4,5),(6,7,8)]
        for combination in winning_combination:
            if not np.isnan(curr_state[combination[0]]) and not np.isnan(curr_state[combination[1]]) and not np.isnan(curr_state[combination[2]]):
                combination_state = curr_state[combination[0]] + curr_state[combination[1]] + curr_state[combination[2]]
                if combination_state == 15:
                    return True
        return False 
            

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up
        ## current state is the list of the 9 values

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) == 0:
            return True, 'Tie'
        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        ## curr_state is a list
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]
        ## enumerate will return index-value pair
        ## if np.isnan(val) RETURNS ONLY THOSE INDEXES WHERE THE VALUE IS A NAN VALUE
        ## this will return the index of the blank position 


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""
        ## allowed values: Player 1:odd , Player 2: even
        ## returns two value lists: agent value and env value

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0] ## odd nos. not pressent in the used values
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0] ## even nos. not pressent in the used values

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""
        
        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)

    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        curr_state[curr_action[0]] = curr_action[1]
        return curr_state


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        final_state = False
        intermediate_state = self.state_transition(curr_state, curr_action)
        final_state, game_status = self.is_terminal( intermediate_state)
        if final_state == True:
            if game_status == 'Win':
                reward = 10
            else:
                reward = 0
        else:
            position = random.choice(self.allowed_positions(intermediate_state))
            value = random.choice(self.allowed_values(intermediate_state)[1])
            intermediate_state[position] = value
            final_state, game_status = self.is_terminal( intermediate_state)
            if final_state==True:
                if game_status == 'Win':
                    reward = 10
                else:
                    reward = 0
            else:
                reward = -1
        return intermediate_state, reward, final_state
