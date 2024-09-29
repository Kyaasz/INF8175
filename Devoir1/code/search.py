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
Pacman agents (in searchAgents.py).
"""

from custom_types import Direction
from pacman import GameState
from typing import Any, Tuple,List
import util

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self)->Any:
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state:Any)->bool:
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state:Any)->List[Tuple[Any,Direction,int]]:
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions:List[Direction])->int:
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()



def tinyMazeSearch(problem:SearchProblem)->List[Direction]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem:SearchProblem)->List[Direction]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 1 ICI
    '''
    start_state = problem.getStartState()
    fringe = util.Stack()
    fringe.push(start_state)
    mem = set() # mémoire des états étendus
    dico = dict() # dictionnaire contenant les parents et les directions
    path = []
    if problem.isGoalState(start_state):
        return path
    else:
        while not fringe.isEmpty():
            s = fringe.pop()
            if s== start_state: 
                pred_s = s
            else:
                pred_s = s[0]
            if problem.isGoalState(pred_s): 
                # reconstruire le chemin
                current_s = s[0]
                while current_s != start_state:
                    path.append(dico[current_s][1])
                    current_s = dico[current_s][0]
                path.reverse()
                return path
            else:
                temp = problem.getSuccessors(pred_s)
                l = [x for x in temp if x[0] not in mem]
                for x in l:
                    # ajout dans la fringe des états
                    fringe.push(x)
                     # ajout de ces états dans le dictionnaire
                    dico[x[0]] = (pred_s, x[1])
                mem.add(pred_s)
        return [] # pas de solution


def breadthFirstSearch(problem:SearchProblem)->List[Direction]:
    """Search the shallowest nodes in the search tree first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 2 ICI
    '''
    start_state = problem.getStartState()
    fringe = util.Queue()
    fringe.push(start_state)
    mem = set() # mémoire des états étendus
    dico = dict() # dictionnaire contenant les parents et les directions
    path = []
    discovered_s = []
    discovered_s.append(start_state)
    if problem.isGoalState(start_state):
        return path
    else:
        while not fringe.isEmpty():
            s = fringe.pop()
            if s== start_state: 
                pred_s = s
            else:
                pred_s = s[0]
            if problem.isGoalState(pred_s): 
                # reconstruire le chemin
                current_s = s[0]
                while current_s != start_state:
                    path.append(dico[current_s][1])
                    current_s = dico[current_s][0]
                path.reverse()
                return path
            else:
                temp = problem.getSuccessors(pred_s)
                l = [x for x in temp if x[0] not in discovered_s]
                for x in l:
                    # ajout dans la fringe des états
                    fringe.push(x)
                    # ajout de ces états dans le dictionnaire
                    dico[x[0]] = (pred_s, x[1])
                    discovered_s.append(x[0])

                mem.add(pred_s)
    return [] # pas de solution

def uniformCostSearch(problem:SearchProblem)->List[Direction]:
    """Search the node of least total cost first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 3 ICI
    '''
    start_state = problem.getStartState()
    fringe = util.PriorityQueue()
    fringe.push(start_state, 0)
    mem = set()  # mémoire des états étendus
    dico = dict() # dictionnaire contenant les parents et les directions
    path = []
    if problem.isGoalState(start_state):
        return path
    else:
        while not fringe.isEmpty():
            s = fringe.pop()
            if s == start_state: 
                current_cost = 0
            else:
                current_cost = dico[s][2] # cost
            if problem.isGoalState(s): 
                # reconstruire le chemin
                current_s = s
                while current_s != start_state:
                    path.append(dico[current_s][1])
                    current_s = dico[current_s][0]
                path.reverse()
                return path
            else:
                temp = problem.getSuccessors(s)
                l = [x for x in temp if x[0] not in mem]
                for x in l:
                    real_cost = current_cost + x[2]
                    # ajout dans la fringe des états
                    fringe.update(x[0], real_cost)
                    # ajout de ces états dans le dictionnaire
                    if (not x[0] in dico) or (x[0] in dico and real_cost < dico[x[0]][2]) :
                        dico[x[0]] = (s, x[1], real_cost)

                mem.add(s)
    return [] # pas de solution


def nullHeuristic(state:GameState, problem:SearchProblem=None)->List[Direction]:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem:SearchProblem, heuristic=nullHeuristic)->List[Direction]:
    """Search the node that has the lowest combined cost and heuristic first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 4 ICI
    '''
    start_state = problem.getStartState()
    fringe = util.PriorityQueue()
    fringe.push(start_state, 0)
    mem = set()  # mémoire des états étendus
    dico = dict() # dictionnaire contenant les parents et les directions
    path = []
    if problem.isGoalState(start_state):
        return path
    else:
        while not fringe.isEmpty():
            s = fringe.pop()
            if s == start_state: 
                current_cost = 0
            else:
                current_cost = dico[s][2] # cost
            if problem.isGoalState(s): 
                # reconstruire le chemin
                current_s = s
                while current_s != start_state:
                    path.append(dico[current_s][1])
                    current_s = dico[current_s][0]
                path.reverse()
                return path
            else:
                temp = problem.getSuccessors(s)
                l = [x for x in temp if x[0] not in mem]
                for x in l:
                    real_cost = current_cost + x[2] 
                    heuristic_cost = current_cost + x[2] + heuristic(x[0], problem)
                    # ajout dans la fringe des états
                    fringe.update(x[0], heuristic_cost)
                    # ajout de ces états dans le dictionnaire
                    if (not x[0] in dico) or (x[0] in dico and real_cost < dico[x[0]][2]) :
                        dico[x[0]] = (s, x[1], real_cost)

                mem.add(s)
    return [] # pas de solution


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
