# searchAgents.py
# ---------------
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

## Lab 1 : Juliette Mathivet 2077885, Yassine Mehmouden 2412865
"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

'''
    INSÉREZ VOTRE SOLUTION À LA QUESTION XX ICI
'''


The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # DO NOT CHANGE; Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
  
        '''
            INSÉREZ VOTRE SOLUTION À LA QUESTION 5 ICI
        '''
        
        #tuple indiquant l'état des coins (mangés = 1 ou non = 0)
        self.corners_state = (0,0,0,0)


    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """

        '''
            INSÉREZ VOTRE SOLUTION À LA QUESTION 5 ICI
        '''
        
        return (self.startingPosition, self.corners_state)


    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """

        '''
            INSÉREZ VOTRE SOLUTION À LA QUESTION 5 ICI
        '''
        cornerState = state[1]
        pos = state[0]
        eatenCorners = sum(cornerState)

        #un état est final si la position actuelle est à un corner et que les 3 autres corners ont été mangés
        return (eatenCorners == 3 and pos in self.corners and cornerState[self.corners.index(pos)] == False)

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]
           
            '''
                INSÉREZ VOTRE SOLUTION À LA QUESTION 5 ICI
            '''
            x,y = state[0] 
            cornerState = state[1]

            #mise à jour de l'état des corners
            if (x,y) in self.corners: 
                l = list(cornerState)
                l[self.corners.index((x,y))] = 1 
                cornerState = tuple(l)

            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextPosition = (nextx, nexty)
                cost = 1
                successors.append(((nextPosition, cornerState), action, cost))


        self._expanded += 1 # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)

    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 6 ICI
    '''
    # On propose ici comme heuristique de renvoyer la distance de Manhattan maximale entre la position actuelle de Pacman et les 
    # différents corners qui n'ont pas été encore visités. L'idée étant d'estimer la distance entre la position actuelle et l'arrivée 
    # sur un état final. Cette estimation est donc réalisée en calculant la distance entre pacman et le coin le plus éloigné 
    # (selon la distance de Manhattan)

    pos = state[0]
    cornerState = state[1]
    n_corners = len(corners) # number of corners

    corners_distance = [0]*n_corners # tableau contenant la distance estimée entre la position et chacun des coins.
                                     # Il contient -1 si le coin a déjà été visité
    
    #On parcourt chaque corner 
    for k in range(n_corners):
        if cornerState[k] == 1: ## Le coin a été visité
            corners_distance[k] = -1
        else:
            corners_distance[k] = util.manhattanDistance(pos, corners[k])

    #on retire les valeurs de -1 des coins déjà mangés 
    pos_distance = [x for x in corners_distance if x>=0]
    max_dis = max(pos_distance)

    return  max_dis

class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

def foodHeuristic(state, problem: FoodSearchProblem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']#
    """
    position, foodGrid = state

    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 7 ICI
    '''
    # Pour cette dernière question, nous avons fait le choix de combiner deux heuristiques, et ainsi retourner le maximum des deux heuristiques
    # à chaque appel.

    # La première calcule la distance entre pacman et le rond jaune le plus proche de lui. Elle y ajoute la distance entre ce rond jaune et le
    # rond jaune qui est le plus éloigné de celui-ci. On retourne donc la somme de ces deux distances, afin de donner une estimation du coût pour
    # se rendre à un état final. Étant donné qu'il n'y a plus de points à manger, au lieu de simplement tenir compte du point le plus éloigné de pacman, 
    # nous avons précisé notre heuristique en calculant dans un premier temps la distance entre pacman et le point le plus proche, puis en calculant
    # la distance entre ce point et le point le plus éloigné de ce dernier. 

    # La deuxième heuristique se base plus sur la géométrie du "plateau de jeu". Dans un premier temps, on calcule le rond jaune le plus éloigné de 
    # pacman au sens de la distance de Manhattan, que l'on notera P1. Ensuite, on divise le plateau en 4 cadres, les cadres étant délimités par la position 
    # de pacman. (Comme si on traçait un trait vertical et un trait horizontal là où se situe pacman). On concentre alors la deuxième partie de la recherche 
    # dans le cadre opposé à celui où se situe P1. On calcule alors le point le plus éloigné de pacman dans ce cadre là. On ajoute alors les deux distances
    # calculées pour obtenir le résultat final de cette heuristique. L'idée étant que pour terminer le niveau, pacman va devoir à la fois manger les deux ronds
    # mais les deux ronds étant situés dans des cadres opposés, pacman va devoir au moins parcourir la distance ici calculée pour terminer le niveau.

    import sys 

    foodCoordoList = foodGrid.asList() #récupérer les coordonnées des ronds jaunes
    distance = 0 
    minCoordo = (-1,-1) # coordonnée du rond jaune le plus proche de pacman
    maxCoordo = (-1,-1) # coordonnée du rond jaune le plus éloigné de pacman
    minDist = sys.maxsize #placeholder pour plus petite distance entre un rond jaune et pacman
    maxDist = 0 #placeholder pour plus grand distance entre un rond jaune et pacman
    maxDist_opposite = 0 #placeholder pour plus grand distance entre un rond jaune et pacman dans le cadre opposé


    if len(foodCoordoList) > 0:
        ## Heuristique 1 : dist(pacman, point le plus proche) + dist entre le point le plus proche et point le plus éloigné de lui
        
        for food in foodCoordoList: #permet de trouver le rond jaune le plus proche et le plus éloigné de pacman. Stocke la distance et les coordonnées
            disman = (util.manhattanDistance(position, food))
            if disman < minDist:
                minDist = disman
                minCoordo = food
            if disman > maxDist:
                maxDist = disman
                maxCoordo = food

        #permet de trouver le rond jaune le plus éloigné du rond jaune identifié plus tôt
        for food in foodCoordoList:
            distanceMan = util.manhattanDistance(minCoordo, food)
            if distanceMan > distance:
                distance = distanceMan

        heuristique_1 =  minDist + distance

        ## Heuristique 2 : dist(pacman, point le plus éloigné) + dist(pacman, point le plus éloigné dans le cadre opposé)

        opposite_foodCoordoList = []  ## Tri pour garder seulement les points dans le cadre opposé
        if maxCoordo[0] > position[0] and maxCoordo[1] > position[1]:
            opposite_foodCoordoList = [food for food in foodCoordoList if (food[0] < position[0] or food[1] < position[1])]
        if maxCoordo[0] > position[0] and maxCoordo[1] < position[1]:
            opposite_foodCoordoList = [food for food in foodCoordoList if food[0] < position[0] or food[1] > position[1]]
        if maxCoordo[0] < position[0] and maxCoordo[1] < position[1]:
            opposite_foodCoordoList = [food for food in foodCoordoList if food[0] > position[0] or food[1] > position[1]]
        if maxCoordo[0] < position[0] and maxCoordo[1] > position[1]:
            opposite_foodCoordoList = [food for food in foodCoordoList if food[0] > position[0] or food[1] < position[1]]
            
        ## Recherche de la distance max dans le cadre opposé
        if len(opposite_foodCoordoList) > 0:
            for food in opposite_foodCoordoList:
                    disman = (util.manhattanDistance(position, food))
                    if disman > maxDist_opposite:
                        maxDist_opposite = disman

        heuristique_2 = maxDist_opposite + maxDist ## Addition des deux distances, à la fois celle entre pacman et le point le plus éloigné puis celle
                                                                                    ## entre pacman et le point le plus éloigné dans le cadre opposé.
        r = max(heuristique_1, heuristique_2)
        
        return r
    else:

        return 0
