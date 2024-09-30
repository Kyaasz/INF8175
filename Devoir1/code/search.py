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
    start_state = (problem.getStartState(), 0) #Ajout d'un placeholder pour la direction
    fringe = util.Stack()
    fringe.push(start_state)
    mem = set() # mémoire des états étendus
    dico = dict() # dictionnaire contenant les parents et les directions
    path = [] #chemin qui sera retourné

    while not fringe.isEmpty():
        current_s = fringe.pop()[0] #Récupération du nouvel état à étendre

        if problem.isGoalState(current_s): #cas où on est à l'état final
            # reconstruction du chemin
            temp_s = current_s
            while temp_s != start_state[0]:
                path.append(dico[temp_s][1])
                temp_s = dico[temp_s][0]
            path.reverse()
            return path
        
        #Traitement des successors, ajout s'ils ne sont pas déjà dans la mem
        else:
            temp = problem.getSuccessors(current_s)
            successorsNotVisited = [x for x in temp if x[0] not in mem] #on retire les successors déjà étendus
            for x in successorsNotVisited:
                # ajout dans la fringe des états
                fringe.push(x)
                # ajout de ces états dans le dictionnaire
                dico[x[0]] = (current_s, x[1])
            mem.add(current_s) #on ajoute l'état étendu à la mémoire

    return [] # pas de solution


def breadthFirstSearch(problem:SearchProblem)->List[Direction]:
    """Search the shallowest nodes in the search tree first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 2 ICI
    '''
    start_state = (problem.getStartState(), 0)
    fringe = util.Queue()
    fringe.push(start_state)
    mem = set() # mémoire des états étendus
    dico = dict() # dictionnaire contenant les parents et les directions
    path = []
    discovered_s = set() #ensemble des états déjà empilés ou visités
    discovered_s.add(start_state[0])
    
    while not fringe.isEmpty():
        current_s = fringe.pop()[0] #Récupération du nouvel état à étendre
       
        if problem.isGoalState(current_s): #cas où on est à l'état final
            # reconstruction du chemin
            temp_s = current_s
            while temp_s != start_state[0]:
                path.append(dico[temp_s][1])
                temp_s = dico[temp_s][0]

            path.reverse()
            return path
        
        #Traitement des successors, ajout s'ils ne sont pas déjà rencontrés        
        else:
            temp = problem.getSuccessors(current_s)
            successorsNotVisited = [x for x in temp if x[0] not in discovered_s] #on retire les successors déjà rencontrés
            for x in successorsNotVisited:
                # ajout dans la fringe des états
                fringe.push(x)
                # ajout de ces états dans le dictionnaire
                dico[x[0]] = (current_s, x[1])
                discovered_s.add(x[0])
            mem.add(current_s)

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
    
    while not fringe.isEmpty():
        current_s = fringe.pop() #Récupération du nouvel état à étendre

        #Assignation du coût jusqu'à l'état courant
        if current_s == start_state: 
            current_cost = 0
        else:
            current_cost = dico[current_s][2] # cost

        if problem.isGoalState(current_s): #cas où on est à l'état final
            # reconstruction du chemin
            temp_s = current_s
            while temp_s != start_state:
                path.append(dico[temp_s][1])
                temp_s = dico[temp_s][0]

            path.reverse()
            return path
        
        #Traitement des successors, ajout s'ils ne sont pas déjà rencontrés        
        else:
            temp = problem.getSuccessors(current_s)
            successorsNotVisited = [x for x in temp if x[0] not in mem]
            for x in successorsNotVisited:
                #mise à jour du coût
                updated_cost = current_cost + x[2]
                # ajout dans la fringe des états
                fringe.update(x[0], updated_cost)
                # ajout de ces états dans le dictionnaire
                if (not x[0] in dico) or (x[0] in dico and updated_cost < dico[x[0]][2]) :
                    dico[x[0]] = (current_s, x[1], updated_cost)

            mem.add(current_s)
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
    
    
    while not fringe.isEmpty():
        current_s = fringe.pop() #Récupération du nouvel état à étendre

        #Assignation du coût jusqu'à l'état courant
        if current_s == start_state: 
            current_cost = 0
        else:
            current_cost = dico[current_s][2] # cost

        if problem.isGoalState(current_s): 
            # reconstruction du chemin
            temp_s = current_s
            while temp_s != start_state:
                path.append(dico[temp_s][1])
                temp_s = dico[temp_s][0]

            path.reverse()
            return path
        
        #Traitement des successors, ajout s'ils ne sont pas déjà rencontrés        
        else:
            temp = problem.getSuccessors(current_s)
            successorsNotVisited = [x for x in temp if x[0] not in mem]
            for x in successorsNotVisited:
                updated_cost = current_cost + x[2] 
                heuristic_cost = updated_cost + heuristic(x[0], problem)
                # ajout dans la fringe des états
                fringe.update(x[0], heuristic_cost)
                # ajout de ces états dans le dictionnaire
                if (not x[0] in dico) or (x[0] in dico and updated_cost < dico[x[0]][2]) :
                    dico[x[0]] = (current_s, x[1], updated_cost)

            mem.add(current_s)
    return [] # pas de solution


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
