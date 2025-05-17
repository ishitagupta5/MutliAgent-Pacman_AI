# multi_agents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattan_distance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def get_action(self, game_state: GameState):
        """
        You do not need to change this method, but you're welcome to.

        get_action() chooses among the best options according to the evaluation function.

        Just like in the previous project, get_action takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legal_moves = game_state.get_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices) # Pick randomly among the best







        "Add more of your code here if you want to"
        





        

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current games state (from which you 
        can retrieve proposed successor GameStates) (pacman.py) and returns a number, 
        where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (all_food) and Pacman position after moving (pacman_position).
        new_scared_times holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successor_game_state = current_game_state.generate_pacman_successor(action)

        if successor_game_state.is_lose():
            return float('-inf')
        if successor_game_state.is_win():
            return float('inf')
        
        pacman_position = successor_game_state.get_pacman_position()
        all_food = successor_game_state.get_food()
        ghost_states = successor_game_state.get_ghost_states()
        scared_times = [ghost_state.scared_timer for ghost_state in ghost_states]

        food_grid = successor_game_state.get_food()
        score = successor_game_state.get_score()

        for ghost_state in ghost_states:
            ghost_position = ghost_state.get_position()
            dist_to_ghost = util.manhattan_distance(pacman_position, ghost_position)
            if dist_to_ghost <= 1:
                return float('-inf')

        food_list = food_grid.as_list()
        if len(food_list) > 0:
            distances_to_food = [
                util.manhattan_distance(pacman_position, food_pos)
                for food_pos in food_list
            ]
            min_food_distance = min(distances_to_food)
            score += 1.0 / (min_food_distance + 1.0)

        return score
        

        

def score_evaluation_function(current_game_state: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.get_score()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, eval_fn = 'score_evaluation_function', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluation_function = util.lookup(eval_fn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def get_action(self, game_state: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluation_function.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
        Returns a list of legal actions for an agent
        agent_index=0 means Pacman, ghosts are >= 1

        game_state.generate_successor(agent_index, action):
        Returns the successor game state after an agent takes an action

        game_state.get_num_agents():
        Returns the total number of agents in the game

        game_state.is_win():
        Returns whether or not the game state is a winning state

        game_state.is_lose():
        Returns whether or not the game state is a losing state
        """      
        best_action = None
        best_value = float('-inf')

        # Get legal moves for Pacman (agentIndex=0)
        legal_actions = game_state.get_legal_actions(0)

        for action in legal_actions:
            successor_state = game_state.generate_successor(0, action)
            # For the next step, agentIndex goes to 1 (ghost 1),
            # depth remains the same if we haven't finished a ply yet.
            value = self.minimax_value(successor_state, agent_index=1, depth=self.depth)

            # Choose the action with the highest minimax value
            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    def minimax_value(self, game_state, agent_index, depth):
        if game_state.is_win() or game_state.is_lose() or depth == 0:
            return self.evaluation_function(game_state)

        if agent_index == 0:
            return self.max_value(game_state, depth)
        else:
            return self.min_value(game_state, agent_index, depth)

    def max_value(self, game_state, depth):
        best_value = float('-inf')
        actions = game_state.get_legal_actions(0)

        if not actions:
            return self.evaluation_function(game_state)

        for action in actions:
            successor_state = game_state.generate_successor(0, action)
            value = self.minimax_value(successor_state, agent_index=1, depth=depth)
            best_value = max(best_value, value)

        return best_value

    def min_value(self, game_state, agent_index, depth):
        best_value = float('inf')
        actions = game_state.get_legal_actions(agent_index)

        if not actions:
            return self.evaluation_function(game_state)

        next_agent = agent_index + 1
        
        if next_agent == game_state.get_num_agents():
            next_agent = 0
            next_depth = depth - 1
        else:
            next_depth = depth

        for action in actions:
            successor_state = game_state.generate_successor(agent_index, action)
            value = self.minimax_value(successor_state, next_agent, next_depth)
            best_value = min(best_value, value)

        return best_value 
        
 

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state: GameState):
        """
        Returns the minimax action using self.depth and self.evaluation_function
        """
        best_action = None
        best_value = float('-inf')

        alpha = float('-inf')
        beta = float('inf')

        legal_actions = game_state.get_legal_actions(0)
        for action in legal_actions:
            successor_state = game_state.generate_successor(0, action)
            value = self.alpha_beta_value(
                game_state=successor_state,
                agent_index=1,
                depth=self.depth,
                alpha=alpha,
                beta=beta
            )

            if value > best_value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

        return best_action
    
    def alpha_beta_value(self, game_state, agent_index, depth, alpha, beta):
        if game_state.is_win() or game_state.is_lose() or depth == 0:
            return self.evaluation_function(game_state)

        if agent_index == 0:
            return self.max_value(game_state, depth, alpha, beta)
        else:
            return self.min_value(game_state, agent_index, depth, alpha, beta)

    def max_value(self, game_state, depth, alpha, beta):
        value = float('-inf')
        actions = game_state.get_legal_actions(0)

        if not actions:
            return self.evaluation_function(game_state)

        for action in actions:
            successor_state = game_state.generate_successor(0, action)
            val = self.alpha_beta_value(successor_state, 1, depth, alpha, beta)
            value = max(value, val)

            alpha = max(alpha, value)
            if alpha > beta:
                break

        return value

    def min_value(self, game_state, agent_index, depth, alpha, beta):
        """
        MIN node for a ghost
        """
        value = float('inf')
        actions = game_state.get_legal_actions(agent_index)

        if not actions:
            return self.evaluation_function(game_state)

        next_agent = agent_index + 1
        next_depth = depth
        if next_agent == game_state.get_num_agents():
            next_agent = 0
            next_depth = depth - 1

        for action in actions:
            successor_state = game_state.generate_successor(agent_index, action)
            val = self.alpha_beta_value(successor_state, next_agent, next_depth, alpha, beta)
            value = min(value, val)

            beta = min(beta, value)
            if alpha > beta:
                break

        return value
         
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def get_action(self, game_state: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluation_function

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        best_action = None
        best_value = float('-inf')

        legal_actions = game_state.get_legal_actions(0)
        for action in legal_actions:
            successor = game_state.generate_successor(0, action)
            value = self.expectimax_value(successor, agent_index=1, depth=self.depth)

            if value > best_value:
                best_value = value
                best_action = action

        return best_action      

    def expectimax_value(self, game_state, agent_index, depth):
        if game_state.is_win() or game_state.is_lose() or depth == 0:
            return self.evaluation_function(game_state)

        if agent_index == 0:
            return self.max_value(game_state, depth)
        else:
            return self.exp_value(game_state, agent_index, depth)

    def max_value(self, game_state, depth):
        best_value = float('-inf')
        actions = game_state.get_legal_actions(0)

        if not actions:
            return self.evaluation_function(game_state)

        for action in actions:
            successor = game_state.generate_successor(0, action)
            val = self.expectimax_value(successor, agent_index=1, depth=depth)
            best_value = max(best_value, val)

        return best_value

    def exp_value(self, game_state, agent_index, depth):
        actions = game_state.get_legal_actions(agent_index)

        if not actions:
            return self.evaluation_function(game_state)

        next_agent = agent_index + 1
        next_depth = depth
        if next_agent == game_state.get_num_agents():
            next_agent = 0
            next_depth = depth - 1

        total_value = 0.0
        for action in actions:
            successor = game_state.generate_successor(agent_index, action)
            val = self.expectimax_value(successor, agent_index=next_agent, depth=next_depth)
            total_value += val

        return total_value / len(actions)    
        

def better_evaluation_function(game_state: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    I combine several features:
      - The raw game score
      - A bonus for being closer to food
      - A penalty for the number of food pellets left
      - A big penalty if non-scared ghosts are close (risk of losing)
      - A bonus if ghosts are scared and close (potential to eat them)
      - A penalty for leftover capsules
      - Positive infinite for winning states, negative infinite for losing states
    """
    if game_state.is_win():
        return float('inf')
    if game_state.is_lose():
        return float('-inf')

    pacman_pos = game_state.get_pacman_position()
    food_grid = game_state.get_food()  
    ghost_states = game_state.get_ghost_states()
    capsules = game_state.get_capsules() 

    score = game_state.get_score()

    food_list = food_grid.as_list()
    if len(food_list) > 0:
        distances_to_food = [util.manhattan_distance(pacman_pos, food_pos)
                             for food_pos in food_list]
        min_food_dist = min(distances_to_food)
        score += 1.0 / (min_food_dist + 1.0)

    score -= 3.0 * len(food_list)

    for ghost_state in ghost_states:
        ghost_pos = ghost_state.get_position()
        dist = util.manhattan_distance(pacman_pos, ghost_pos)

        if ghost_state.scared_timer > 0:
            if dist <= 2:
                score += 10.0
        else:
            if dist <= 1:
                score += -100
            elif dist <= 3:
                score += -5.0 / dist

    score -= 4.0 * len(capsules)

    return score


# Abbreviation
better = better_evaluation_function
