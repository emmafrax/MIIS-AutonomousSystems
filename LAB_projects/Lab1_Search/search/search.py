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

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
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
    "*** YOUR CODE HERE ***"
    
    start = (problem.getStartState(), [None])

    #Creating the list where we keep the visited nodes
    visited = []
    
    #where_to_go next, it is a stack so it uses a FIFO order
    w_t_g = util.Stack()

    #Adding start to the first where to go node
    w_t_g.push(start)

    
    #While there are still nodes to go to
    while w_t_g.isEmpty() != True:
        
    #Take last node that was pushed into stack and the trajectory to that path
        (parent,traj) = w_t_g.pop()
        #print(parent)
        #print(traj)

    #Check if it is goal
        if problem.isGoalState(parent) == True:
            path=traj
            break
        
    #If this node has already been visited we skip the other orders
        if parent in visited:
            continue
            
    #If we haven't visited the node we add it to visited list
    #  and we add the successors and updating the trakectories in the w_t_g stack
        else:

            #Add to visited
            visited.append(parent)
            
            #keep track of path and add non-visited nodes to w_t_g
            for successor in problem.getSuccessors(parent): 
                if successor[0] not in visited:
                    traj_suc = list(traj)
                    traj_suc.append(successor[1])
                    w_t_g.push((successor[0],traj_suc))

    
    #Removing the first action 
    path.remove(None)

    return path

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    start = (problem.getStartState(), [None])

    #Creating the list where we keep the visited nodes
    visited = []
    
    #where_to_go next, it is a stack so it uses a FIFO order
    w_t_g = util.Queue()

    #Adding start to the first where to go node
    w_t_g.push(start)

    
    #While there are still nodes to go to
    while w_t_g.isEmpty() != True:
        
    #Take last node that was pushed into stack and the trajectory to that path
        (parent,traj) = w_t_g.pop()
        #print(parent)
        #print(traj)

    #Check if it is goal
        if problem.isGoalState(parent) == True:
            path=traj
            break
        
    #If this node has already been visited we skip the other orders
        if parent in visited:
            continue
            
    #If we haven't visited the node we add it to visited list
    #  and we add the successors and updating the trakectories in the w_t_g stack
        else:

            #Add to visited
            visited.append(parent)
            
            #keep track of path and add non-visited nodes to w_t_g
            for successor in problem.getSuccessors(parent): 
                if successor[0] not in visited:
                    traj_suc = list(traj)
                    traj_suc.append(successor[1])
                    w_t_g.push((successor[0],traj_suc))

    
    #Removing the first action 
    path.remove(None)

    return path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    start = (problem.getStartState(), [None],0)

    #Creating the list where we keep the visited nodes
    visited = []
    
    #where_to_go next, it is a stack so it uses a FIFO order
    w_t_g = util.PriorityQueue()

    #Adding start to the first where to go node
    w_t_g.push(start,0)

    
    #While there are still nodes to go to
    while w_t_g.isEmpty() != True:
        
    #Take last node that was pushed into stack and the trajectory to that path
        (parent,traj,cost) = w_t_g.pop()


    #Check if it is goal
        if problem.isGoalState(parent) == True:
            path=traj
            break
        
    #If this node has already been visited we skip the other orders
        if parent in visited:
            continue
            
    #If we haven't visited the node we add it to visited list
    #  and we add the successors and updating the trakectories in the w_t_g stack
        else:

            #Add to visited
            visited.append(parent)
            
            #keep track of path and add non-visited nodes to w_t_g
            for successor in problem.getSuccessors(parent): 
                if successor[0] not in visited:
                    traj_suc = list(traj)
                    traj_suc.append(successor[1])
                    cost_s = cost + successor[2]
                    w_t_g.push((successor[0],traj_suc,cost_s),cost_s)

    
    #Removing the first action 
    path.remove(None)

    return path
    util.raiseNotDefined()
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ##python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

    start = problem.getStartState()
    #If you already are in the goal:
    if problem.isGoalState(start):
        return 

    # G is the distace from start to node n 
    # H heuristic distance from node to end
    # F total cost H+G

    #open list nodes to be visited
    open_l = util.PriorityQueue()
    # g is zero for start node
    g = 0
    h = heuristic(start,problem)
    #Define start state with all the variables + the path
    start_state = (start,g,h,[])
    f = g+h
    open_l.update(start_state,f)

    #closed list nodes visited
    visited = []


    while open_l.isEmpty() != True:
        (curr, g, h, path) = open_l.pop()
        #Return path when goal reached
        if problem.isGoalState(curr):
            return path

        if curr in visited:
            continue
            
        visited.append(curr)
        #For each succesor compute its cost and heuristic and addid to the open queue. 
        for successor, action, cost in problem.getSuccessors(curr):
            if successor in visited:
                continue                
            next_cost = g + cost
            h = heuristic(successor, problem)
            open_l.update((successor, next_cost, h, path + [action]), next_cost + h)



    util.raiseNotDefined()




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
