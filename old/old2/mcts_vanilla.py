
from mcts_node import MCTSNode
import operator
from random import choice
from math import sqrt, log
import rollout_bot
import random

num_nodes = 1000
explore_faction = 2.
current_node = None

def traverse_nodes(node, state, identity):
    exploration_coefficient = 2
    exploration_values = {}
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    if len(node.untried_actions)!= 0:
        untried = node.untried_actions.pop()
        n = MCTSNode(parent = node, parent_action=untried, action_list=state.legal_moves)
        return n

    x = 0
    for p in node.child_nodes:
        n = node.child_nodes[p]
        print("in traversing")
        print(str(n))
        traversing = (n.wins/n.visits)+(2*exploration_coefficient*sqrt((2*log(node.visits)/n.visits)))
        exploration_values[x]= traversing
        print("traversing = "+str(traversing))
        print("dict value is "+str(exploration_values[x]))
        x+=1
    maximum = 0
    print("dict is")
    print(exploration_values)
    for i in range(len(exploration_values)):
        if exploration_values[i]>maximum:
            maximum=exploration_values[i]



    return maximum
    pass
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    action = rollout(state)
    n = MCTSNode(parent= node, parent_action=action, action_list=state.legal_moves)
    #n.parent = node
    node.child_nodes[action] = n
    #n.parent_action = action
    return n
    pass
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    #rollout_bot.think(state)
    current_state = state.copy()
    return random.choice(current_state.legal_moves)


    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node!=None:
        node.visits+=1
        if won:
            node.wins+=1
        node = node.parent
    pass

def think(state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)
    me = state.player_turn

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state.copy()
        # Start at root
        node = root_node

        while not sampled_game.is_terminal():
        # Do MCTS - This is all you!
            if sampled_game.player_turn!=me:
                rollout_move=rollout_bot.think(sampled_game.copy())
                sampled_game.apply_move(rollout_move)
                print("rollout bot")
                continue
            if len(node.child_nodes)!=0:
                node=traverse_nodes(node,sampled_game, me)
                sampled_game.apply_move(node.parent_action)
                print("traversing result")
                print(str(node.parent_action))
            #while not state.is_terminal():
            node=expand_leaf(node,sampled_game)
            sampled_game.apply_move(node.parent_action)
            print("expanding leaf result")
            print(str(node.parent_action))
        if me ==sampled_game.winner:
            won = True
        else:
            won = False
        backpropagate(node, won)
    node = traverse_nodes(root_node, state)
    move = node.parent_action
    return move
    #return check_tree(root_node, state)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
