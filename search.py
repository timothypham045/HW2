# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os

# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def is_wall(self, state):
        """
          state: Search state

        Returns True if and only if the state is a wall.
        """
        util.raise_not_defined()


    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    """Search the deepest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    start = problem.get_start_state()
    start_hits = 1 if problem.is_wall(start) else 0

    frontier.push((start, [], start_hits))  # (pos, actions, and hitWalls)
    visited = set()

    while not frontier.is_empty():
        pos, actions, hits = frontier.pop()

        if (pos, hits) in visited:
            continue
        visited.add((pos, hits))

        if problem.is_goal_state(pos) and 1 <= hits <= 2:
            return actions

        for succ, action, step_cost in problem.get_successors(pos):
            new_hits = hits + (1 if problem.is_wall(succ) else 0)
            if new_hits <= 2 and (succ, new_hits) not in visited:
                frontier.push((succ, actions + [action], new_hits))

    return []


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    start = problem.get_start_state()
    start_hits = 1 if problem.is_wall(start) else 0

    frontier.push((start, [], start_hits))
    visited = set()

    while not frontier.is_empty():
        pos, actions, hits = frontier.pop()

        if (pos, hits) in visited:
            continue
        visited.add((pos, hits))

        if problem.is_goal_state(pos) and 1 <= hits <= 2:
            return actions

        for succ, action, step_cost in problem.get_successors(pos):
            new_hits = hits + (1 if problem.is_wall(succ) else 0)

            if new_hits <= 2 and (succ, new_hits) not in visited:
                frontier.push((succ, actions + [action], new_hits))

    return []


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    start = problem.get_start_state()
    start_hits = 1 if problem.is_wall(start) else 0

    frontier.push((start, [], 0, start_hits), 0)
    dist = {(start, start_hits): 0}

    while not frontier.is_empty():
        pos, actions, cost_so_far, hits = frontier.pop()

        if problem.is_goal_state(pos) and 1 <= hits <= 2:
            return actions

        for succ, action, step_cost in problem.get_successors(pos):
            new_hits = hits + (1 if problem.is_wall(succ) else 0)
            if new_hits > 2:
                continue

            new_cost = cost_so_far + step_cost
            key = (succ, new_hits)

            if key not in dist or new_cost < dist[key]:
                dist[key] = new_cost
                frontier.push((succ, actions + [action], new_cost, new_hits), new_cost)

    return []
#
# heuristics
#
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

def your_heuristic(state, problem=None):
    """ Your Custom Heuristic """
    "*** YOUR CODE HERE ***"
    x1, y1 = state
    x2, y2 = problem.goal
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(problem, heuristic=null_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    start = problem.get_start_state()
    start_hits = 1 if problem.is_wall(start) else 0

    frontier.push((start, [], 0, start_hits), heuristic(start, problem))
    dist = {(start, start_hits): 0}

    while not frontier.is_empty():
        pos, actions, g, hits = frontier.pop()

        if problem.is_goal_state(pos) and 1 <= hits <= 2:
            return actions

        for succ, action, step_cost in problem.get_successors(pos):
            new_hits = hits + (1 if problem.is_wall(succ) else 0)
            if new_hits > 2:
                continue

            new_g = g + step_cost
            key = (succ, new_hits)

            if key not in dist or new_g < dist[key]:
                dist[key] = new_g
                f = new_g + heuristic(succ, problem)
                frontier.push((succ, actions + [action], new_g, new_hits), f)

    return []
# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search
