
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf
import rollout_bot
import random_bot
import random
import operator

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, state, identity):
    exploration_coefficient = .01 #changed(this may have helped a lot)
    exploration_values = {}
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    
    #print(node.untried_actions)
    if len(node.untried_actions)!= 0:
        untried = node.untried_actions.pop()
        leaf_node = MCTSNode(parent=node, parent_action=untried, action_list=state.legal_moves)
        node.child_nodes[untried] = leaf_node
        return leaf_node
        #return node.untried_actions.pop()

    changer = float(-inf)
    leaf_node = MCTSNode
    for p in node.child_nodes:
        n = node.child_nodes[p]
        #print(n.visits)
        #print(node.visits)
        #print("in traversing")
        if (n.visits == 0):
            leaf_node = n
            node.child_nodes[leaf_node.parent_action] = leaf_node #added
            return leaf_node
        if(node.visits == 0):
            traversing = (n.wins/n.visits)+(2*exploration_coefficient*sqrt((2*log(1)/n.visits)))
        else:
            traversing = (n.wins/n.visits)+(2*exploration_coefficient*sqrt((2*log(node.visits)/n.visits)))
        exploration_values[n] = traversing
        if exploration_values[n] > changer:
            changer = exploration_values[n]
            leaf_node = n
    node.child_nodes[leaf_node.parent_action] = leaf_node
    return leaf_node
    """
    minimum_threshold = min(sqrt(node.visits), len(node.child_nodes))
    while not state.is_terminal() and node.tries < minimum_threshold:
        child_node = max(node.child_nodes.values(), key= ucb)
        state.apply_move(child_node, parent_action)
        node.tries += 1
        node = child_node
    return node
    pass
    # Hint: return leaf_node

def avg_score(node):
    return (node.wins/node.visits)

def mixmax(node):
    return .8*(avg_score(node)) + .2*(max(node.child_nodes, key=avg_score))

def ucb(child_node):
    parent_node = child_node.parent
    w_rate = mixmax(child_node)
    return w_rate + sqrt(log(parent_node.visits)/child_node.visits)


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    """
    action = random.choice(node.untried_actions)
    new_node = MCTSNode(parent=node, parent_action=action, action_list=state.legal_moves)
    #n.parent = node
    node.child_nodes[action] = new_node
    #n.parent_action = action
    return new_node
    pass
    # Hint: return new_node
    """
    action = rollout(state)
    #q = action
    for r in action:
        q = r
    new_node = MCTSNode(parent= node, parent_action=q, action_list=state.legal_moves)
    #n.parent = node
    node.child_nodes[q] = new_node
    #n.parent_action = action
    return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    #current_state = state.copy()
    #return random.choice(current_state.legal_moves)

    moves = state.legal_moves

    best_move = moves[0]
    best_expectation = float('-inf')

    me = state.player_turn

    # Define a helper function to calculate the difference between the bot's score and the opponent's.
    def outcome(score):
        red_score = score.get('red', 0)
        blue_score = score.get('blue', 0)
        return red_score - blue_score if me == 'red' else blue_score - red_score

    for move in moves:
        total_score = 0.0


        # Sample a set number of games where the target move is immediately applied.
        for r in range(10):
            rollout_state = state.copy()
            rollout_state.apply_move(move)

            # Only play to the specified depth.
            while True:
                if rollout_state.is_terminal():
                    break
                rollout_move = random.choice(rollout_state.legal_moves)
                rollout_state.apply_move(rollout_move)

            total_score += outcome(rollout_state.score)

        expectation = float(total_score) / 10

        # If the current move has a better average score, replace best_move and best_expectation
        if expectation > best_expectation:
            best_expectation = expectation
            best_move = move
            actual_move = {best_move:best_expectation}
    return actual_move


    pass



def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node.parent!=None:
        node.visits+=1
        if won:
            node.wins+=1
        node = node.parent


def think(state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    """
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)
    me = state.player_turn
    move = None
    possible_move = {}

        # Copy the game for sampling a playthrough
    sampled_game = state.copy()

        # Start at root
    node = root_node
        #print(MCTSNode.tree_to_string(node))

    for step in range(10):
        # Do MCTS - This is all you!
        n = traverse_nodes(node, sampled_game, me)
        #print (str(n.parent_action))
            #return node.parent_action
        #while not state.is_terminal():
        new_node = expand_leaf(n, sampled_game)
        roll = rollout(sampled_game)
        for r in roll:
            possible_move[r] = roll[r]
            if roll[r] > 0:
                won = True
            else:
                won = False
        backpropagate(new_node, won)
        #print (MCTSNode.tree_to_string(root_node))
        #print("f"))
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    test = float(-inf)
    for q in possible_move:
        if possible_move[q] > test:
            test = possible_move[q]
            move = q
    return move
    """
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)
    me = state.player_turn
    move = None
    i = 0;
    for step in range(40):
        # Copy the game for sampling a playthrough
        sampled_game = state.copy()
        # Start at root
        node = root_node
        holder = root_node
        print ("foo", i)
        i += 1

        while not sampled_game.is_terminal():
            # Do MCTS - This is all you!
            if sampled_game.player_turn!=me:
                rollout_move= rollout_bot.think(sampled_game.copy()) #chaged bot(won 9/10, with rollout still 8/10)
                sampled_game.apply_move(rollout_move)   #applies multiple moves taking away from legal moves to traverse
                #print("rollout bot")
                continue
            node=traverse_nodes(node,sampled_game, me)
            sampled_game.apply_move(node.parent_action)
            #print("traversing result")
            #print(str(node.parent_action))
            #while not state.is_terminal():
            if not sampled_game.is_terminal():
                node=expand_leaf(node,sampled_game)
                #sampled_game.apply_move(new.parent_action)
                #print("expanding leaf result")
                #print(str(node.parent_action))
            if not sampled_game.is_terminal():
                #print("rolling")
                new_roll = rollout(sampled_game)
                action = None
                for r in new_roll:
                    action = r
                    if new_roll[r] > 0:
                        won = True
                    else:
                        won = False
                sample = MCTSNode(parent=node, parent_action=action)
                node.child_nodes[action] = sample
                backpropagate(sample,won)
                if(node.parent.parent == root_node):
                    root_node.visits +=1

            #holder = node
            #print("q", root_node.visits)
            #print (node.visits)
        if me == sampled_game.winner:
            won = True
        else:
            won = False
        backpropagate(node, won)
        move = traverse_nodes(root_node,sampled_game,me)

        #root_node.visits+=1
    #for q in root_node.child_nodes:
        #print(root_node.child_nodes[q])
    #print(move.parent_action)
    print("red") #to tell me which bot it was
    return move.parent_action
