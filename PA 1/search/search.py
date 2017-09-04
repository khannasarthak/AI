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


# def bdfs(problem,algoType,dataStructure):

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()   

    # References: 
    #   https://docs.python.org/2.7/tutorial/classes.html   
    #   https://stackoverflow.com/questions/21508765/how-to-implement-depth-first-search-for-graph-with-non-recursive-aprroach    
    #   https://www.reddit.com/r/artificial/comments/6rwbf1/ai_teaching_pacman_to_search_with_depth_first/
    #   AI a modern approach, pg 86,87 
    #   https://stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search

    class node():   # Class to initialise nodes.
        def __init__(self,parent,state,action):
            self.parent = parent
            self.state = state
            self.action = action
          
    root = node(None, problem.getStartState(),None)  # Setting root node  

    fringe = util.Stack() # generate fringe stack or frontier   
    explored = set() # set to store visited nodes, set to prevent duplicates  
    
    fringe.push(root)   # Push root onto the stack
    actions = []    # list of actions to return

    while fringe.isEmpty()==False:  # while loop to check while the stack is not empty
        currentNode = fringe.pop()  # pop the node         
        currentState = currentNode.state 

        if problem.isGoalState(currentState):   # Checking if goal state is reached. Then currentNode is the solution
            break

        if currentState in explored:    # adding node.state to explored and marking it as visited
            continue
        else:
            explored.add(currentState)

        
        for successor in problem.getSuccessors(currentState):   # Get successors of the current node
            # print ('+++', successor,'STATE-',successor[0],'Action-',successor[1]) # successor[0] gives the state of the child node
            if successor[0] not in explored:  # If succesors not already visited, we push the successsor onto the stack  
                    
                successorNode = node(currentNode,successor[0],successor[1])  # assign successorNode with its parent, state and action 
                # upon inspection of successor, it was of the form [state,action,path cost]. Path cost has no use in DFS, thus ignored. 

                fringe.push(successorNode) # push the successor node onto the stack

  
    while currentNode.parent:     # tracing the path going back up to the parent.
        actions.append(currentNode.action)  # adding the action of each node going up to the root.
        currentNode = currentNode.parent    # updating currentNode with its parent node
    
    return actions[::-1]    # Reversing the output, since it is stack.





def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # Basically, BFS is the same as DFS, all we have to do is change the LIFO Stack to a FIFO Queue. Thus, using the same code and
    # just change the util.Stack() to util.Queue() passed the test cases.
    # Reference:
    #   AI a modern approach, pg 81,82
    

    class node():   # Class to initialise nodes.
        def __init__(self,parent,state,action):
            self.parent = parent
            self.state = state
            self.action = action
          
    root = node(None, problem.getStartState(),None)  # Setting root node  

    fringe = util.Queue() # generate fringe queue or frontier   
    explored = set() # set to store visited nodes, set to prevent duplicates  
    
    fringe.push(root)   # Push root onto the queue
    actions = []    # list of actions to return

    while fringe.isEmpty()==False:  # while loop to check while the queue is not empty
        currentNode = fringe.pop()  # pop the node         
        currentState = currentNode.state 

        if problem.isGoalState(currentState):   # Checking if goal state is reached. Then currentNode is the solution
            break

        if currentState in explored:    # adding node.state to explored and marking it as visited
            continue
        else:
            explored.add(currentState)

        
        for successor in problem.getSuccessors(currentState):   # Get successors of the current node
            # print ('+++', successor,'STATE-',successor[0]) # successor[0] gives the state of the child node
            if successor[0] not in explored:  # If succesors not already visited, we push the successsor onto the queue  
                    
                successorNode = node(currentNode,successor[0],successor[1])  # assign successorNode with its parent, state and action  

                fringe.push(successorNode) # push the successor node onto the queue

  
    while currentNode.parent:     # tracing the path going back up to the parent.
        actions.append(currentNode.action)  # adding the action of each node going up to the root.
        currentNode = currentNode.parent    # updating currentNode with its parent node
    
    return actions[::-1]    # Reversing the output as we are appending at the end of the actions list
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # References:
    #   https://www.youtube.com/watch?v=dRMvK76xQJI
    #   AI a modern approach, pg 84
    #   https://cyluun.github.io/blog/uninformed-search-algorithms-in-python


    

    class node():   # Class to initialise nodes.
        def __init__(self,parent,state,action,cost):
            self.parent = parent
            self.state = state
            self.action = action
            self.cost = cost

          
    root = node(None, problem.getStartState(),None,0)
    fringe = util.PriorityQueue() 
    fringe.push(root,root.cost) 
    explored = set()
    actions = []

    while fringe.isEmpty()==False:
        currentNode = fringe.pop()
        currentState = currentNode.state
        currentCost = currentNode.cost

        if problem.isGoalState(currentState):
            break

        if currentState in explored:
            continue
        else:
            explored.add(currentState)

        for successor in problem.getSuccessors(currentState):
            if successor[0] not in explored:
                successorNode = node(currentNode,successor[0],successor[1],currentCost+successor[2])    # Cost has to be calculated for 
                # each successor, and thus it has the cost of the parent added to it. 
                fringe.push(successorNode,successorNode.cost)

    #print ('PATH COST---',currentNode.cost)
    while currentNode.parent:
        actions.append(currentNode.action)
        currentNode=currentNode.parent

    return actions[::-1]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    # References:
    #   http://www.redblobgames.com/pathfinding/a-star/introduction.html
    #   http://www.growingwiththeweb.com/2012/06/a-pathfinding-algorithm.html
    #   http://www.redblobgames.com/pathfinding/a-star/implementation.html
    #   

    class node():   # Class to initialise nodes.
        def __init__(self,parent,state,action,gcost,hcost):
            self.parent = parent
            self.state = state
            self.action = action
            self.gcost = gcost # g(n)
            self.hcost = hcost # h(n)          
            self.fcost = gcost+hcost  #f(n) = g(n) + h(n)  
            

    # Initializing root with g(n) = 0, h(n) = heauristic(startState)
    root = node(None,problem.getStartState(),None,0,heuristic(problem.getStartState(),problem)) 

    fringe = util.PriorityQueue()
    fringe.push(root,root.fcost)

    # print ('ROOT COST', root.fcost)
    explored = set()
    actions = []


    while fringe.isEmpty()==False:
        currentNode = fringe.pop()
        currentState = currentNode.state
        currentGCost = currentNode.gcost # current g(n), to calculate total cost for each successor node, like UCS
        currentFCost = currentNode.fcost # f(n) for each node, also calculated for each successor

        if problem.isGoalState(currentState):
            break

        if currentState in explored:
            continue
        else:
            explored.add(currentState)

        for successor in problem.getSuccessors(currentState):
            if successor[0] not in explored:
            # If successor not visited, we initialize the succesor Node with (Parent, State, Action, updated g(n) like UCS, h(n) using the heuristic)

                successorNode = node(currentNode,successor[0],successor[1],currentGCost+successor[2],heuristic(successor[0],problem))  
                # It is then pushed onto the priority Queue           
                fringe.push(successorNode,successorNode.fcost)


    while currentNode.parent:
        actions.append(currentNode.action)
        currentNode=currentNode.parent

    return actions[::-1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


