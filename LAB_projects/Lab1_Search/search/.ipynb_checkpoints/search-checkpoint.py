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


    from game import Directions
    
    start = problem.getStartState()
#If you already are in the goal:
    if problem.isGoalState(start):
        return 


#Creating the list where we keep the visited nodes
    visited = []
#where_to_go next, it is a stack so it uses a LIFO order
    w_t_g = util.Stack()
#Initialize dictionary to draw the path backwards
    parent_list = {}
    parent_list[start] = (None,None)

#Adding start to the first where to go node
    w_t_g.push(start)
    #print('start', start)

#Initialize list for the backwards path
    path=[]

    
#While there are still nodes to go to
    while w_t_g.isEmpty != True:
        
    #Take last node that was pushed into stack
        parent = w_t_g.pop()
        
        
    #If this node has already been visited we skip the other orders
        if parent in visited:
            continue
            
    #If we haven't visited the node we check if it is a goal, we add it to visited list
    #  and we add the successors in the w_t_g stack, keeping track of the path with 
    #  the dictionary
        else:
            #Check if it is goal
            if problem.isGoalState(parent) == True:
                goal = parent
                #print('goal!')
                #path.append(goal)
                while goal != None:
#                     print('iter',parent_list)
                    (prev_state,act) = parent_list[goal]
                    path.append(act)
                    goal= prev_state
                break
            
            #Add to visited
            #print('visiting', parent)
            visited.append(parent)
            
            #keep track of path and add nodes to w_t_g
            for successor in problem.getSuccessors(parent):
                w_t_g.push(successor[0])
                
                if successor[0] not in parent_list.keys():
                    action = successor[1]
                    parent_list[successor[0]] = (parent,action)
                    #print(parent_list)

     
    #Finding the real path (inverse of found path)
    #print('inverse path',path)
    path.reverse()
    path.remove(None)
    #print('path', path)
    
    
    #Describe directions
    #s = Directions.SOUTH
    #w = Directions.WEST
    #n = Directions.NORTH
    #e = Directions.EAST
    
    #actions=[]
    
    #Check what are the actions to do that path
    #for i in range(len(path)-1):
    #    a=path[i]
    #    b=path[i+1]
    #    c= (b[0]-a[0],b[1]-a[1])
    #    print(c)
    #    if c[1]>0:
    #        print('n')
    #        actions.append(n)
    #    if c[1]<0:
    #        print('s')
    #        actions.append(s)
    #    if c[0]>0:
    #        print('e')
    #        actions.append(e)
    #    if c[0]<0:
    #        print('w')
    #        actions.append(w)
    #print(actions)
    
    return path

#So it moves slowly
# python pacman.py -l tinyMaze -p SearchAgent --frameTime=2
        
# what is this?? nomes un print no?
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    from game import Directions
    
    start = problem.getStartState()
#If you already are in the goal:
    if problem.isGoalState(start):
        return 


#Creating the list where we keep the visited nodes
    visited = []
#where_to_go next, it is a stack so it uses a FIFO order
    w_t_g = util.Queue()
#Initialize dictionary to draw the path backwards
    parent_list = {}
    parent_list[start] = (None,None)

#Adding start to the first where to go node
    w_t_g.push(start)
    #print('start', start)

#Initialize list for the backwards path
    path=[]

    
#While there are still nodes to go to
    while w_t_g.isEmpty != True:
        
    #Take last node that was pushed into stack
        parent = w_t_g.pop()
        
        
    #If this node has already been visited we skip the other orders
        if parent in visited:
            continue
            
    #If we haven't visited the node we check if it is a goal, we add it to visited list
    #  and we add the successors in the w_t_g stack, keeping track of the path with 
    #  the dictionary
        else:
            #Check if it is goal
            if problem.isGoalState(parent) == True:
                goal = parent
                #print('goal!')
                #path.append(goal)
                while goal != None:
#                     print('iter',parent_list)
                    (prev_state,act) = parent_list[goal]
                    path.append(act)
                    goal= prev_state
                break
            
            #Add to visited
            #print('visiting', parent)
            visited.append(parent)
            
            #keep track of path and add nodes to w_t_g
            for successor in problem.getSuccessors(parent):
                w_t_g.push(successor[0])
                
                if successor[0] not in parent_list.keys():
                    action = successor[1]
                    parent_list[successor[0]] = (parent,action)
                    #print(parent_list)

     
    #Finding the real path (inverse of found path)
    #print('inverse path',path)
    path.reverse()
    path.remove(None)

    return path

        
# what is this?? nomes un print no?
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    from game import Directions
    
    start = (problem.getStartState(),0)
#If you already are in the goal:
    if problem.isGoalState(start[0]):
        return 


#Creating the list where we keep the visited nodes
    visited = []
#where_to_go next, it is a priority queue so it uses a cost order
    w_t_g = util.PriorityQueue()
#Initialize dictionary to draw the path backwards
    parent_list = {}
    parent_list[start[0]] = (None,None)

#Adding start to the first where to go node
    w_t_g.update(start,0)
    #print('start', start)

#Initialize list for the backwards path
    path=[]

    
#While there are still nodes to go to
    while w_t_g.isEmpty != True:
        
    #Take last node that was pushed into stack
        (parent,cost) = w_t_g.pop()

    #Check if it is goal
        if problem.isGoalState(parent) == True:
            goal = parent
            #print('goal!')
            #path.append(goal)
            while goal != None:
#               print('iter',parent_list)
                (prev_state,act) = parent_list[goal]
                path.append(act)
                goal= prev_state
            break

    #If this node has already been visited we skip the other orders
        if parent in visited:
            continue
            
    #If we haven't visited the node we check if it is a goal, we add it to visited list
    #  and we add the successors in the w_t_g stack, keeping track of the path with 
    #  the dictionary
        else:
            
            #Add to visited
            #print('visiting', parent)
            visited.append(parent)
            
            #keep track of path and add nodes to w_t_g
            for successor in problem.getSuccessors(parent):
                cost_s = cost + successor[2]
                successor_state = (successor[0],cost_s)
                w_t_g.update(successor_state ,cost_s)
                
                if successor[0] not in parent_list.keys():
                    action = successor[1]
                    parent_list[successor[0]] = (parent,action)
                    #print(parent_list)

    #Finding the real path (inverse of found path)
    #print('inverse path',path)
    path.reverse()
    path.remove(None)
    
    return path

        
# what is this?? nomes un print no?
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
    g = 0
    h = heuristic(start,problem)
    start_state = (start, g,h,[])
    f = g+h
    open_l.update(start_state,f)

    #closed list nodes visited
    closed_l = []

    while(not open_l.isEmpty()):
        (curr, g, h, path) = open_l.pop()

        if problem.isGoalState(curr):
            return path

        if curr in closed_l:
            continue
        closed_l.append(curr)
        for suc, action, c in problem.getSuccessors(curr):
            if suc in closed_l:
                continue                
            next_cost = g + c
            h = heuristic(suc, problem)
            open_l.update((suc, next_cost, h, path + [action]), next_cost + h)



    util.raiseNotDefined()




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
