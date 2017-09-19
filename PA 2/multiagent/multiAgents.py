# multiAgents.py
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # Function to run classic search: python pacman.py --frameTime 0 -p ReflexAgent -l testClassic

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        print newFood
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # References:
        #   http://giocc.com/concise-implementation-of-minimax-through-higher-order-functions.html
        #   https://athena.ecs.csus.edu/~gordonvs/Beijing/Minimax.pdf
        #   AI, A modern Approach pg 166
        
        # Agents = 0 : Pacman
        # Agent = 1 : Ghost
        # Agent = 2 : Ghost     

        def miniMax(gameState,depth):
            return (maxPlay(gameState,self.depth)[1])   # returns the optimal move
        
        def maxPlay(gameState,depth):
            # check if it is a terminal state, if yes then return utility
            if depth == 0 or gameState.isWin()==True or gameState.isLose() == True:
                return self.evaluationFunction(gameState)
            # Get valid moves
            validMoves = gameState.getLegalActions(0) #
            # calculatin v for each successor state for valid moves
            values = []
            for move in validMoves:
                # Next move is of the ghost after pacman
                values.append(minPlay(gameState.generateSuccessor(0, move),1,depth))
            # Taking maximum of those values    
            maxValues = max(values)
            
            # Findin the best move, i.e, the one with the maximum valued utility, this was easier
            # to implement as compared to the minimax decision funtion in the book.
            bestMove = validMoves[values.index(maxValues)]          
            return maxValues,bestMove


        def minPlay(gameState,agent,depth):
            if depth == 0 or gameState.isWin()==True or gameState.isLose() == True:
                return self.evaluationFunction(gameState)

            validMoves = gameState.getLegalActions(agent) 
            values = []

            numOfGhosts = gameState.getNumAgents()-1

            for move in validMoves:
                if(agent==numOfGhosts): # that means last ghost, so next move will be of pacman

                    values.append(maxPlay(gameState.generateSuccessor(agent,move),depth-1))                    
                else:   # Penultimate ghost, next move of last ghost
                    values.append(minPlay(gameState.generateSuccessor(agent,move),agent+1,depth))   # agent+1 =2
                    
                
            minValues = min(values)
            
            return minValues

        return miniMax(gameState,self.depth)





        
            


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # DO THIS AGAIN

        # def absearch(gameState,depth): # returns a move
            
            
        #     validMoves = gameState.getLegalActions(0) # pacman
        #     values = []
        #     for move in validMoves:
        #         # values = [(value),(move)]
        #         values.append((minValue(gameState.generateSuccessor(0, move), float('-inf'), float('inf'), 1,gameState.getNumAgents() - 1), move))
           
        #     # return max(values, key=values.get)

        #     bestMove = max(values)
        #     print (bestMove)
        #     return bestMove[1]



            # return validMoves[values.index(v)]  # move which has max value v

        def maxValue(gameState,a,b,depth): # return utility value,[self.eval], and the move corresponding to the 
        
            if depth == 0 or gameState.isWin()==True or gameState.isLose() == True:
                return self.evaluationFunction(gameState)

            v = float('-inf') # v = -infi
            
            # depth += 1
            validMoves = gameState.getLegalActions(0) # pacman
            for move in validMoves:
                # value = minValue(gameState.generateSuccessor(0,move),a,b,depth,1)
                # v = max(v,value)
                v = max(v, minValue(gameState.generateSuccessor(0,move), a, b, depth, 1))

                if v>b:
                    return v
                a = max(a,v)
            
            # print ('MAX',v)
            return v
        
        
        def minValue(gameState, a, b, depth, agent):
            
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            v = float("inf")
            numOfGhosts = gameState.getNumAgents() - 1

            validMoves = gameState.getLegalActions(agent)
            
            for move in validMoves:
                # nextState = gameState.generateSuccessor(agentindex, action)
                if agent == numOfGhosts:
                    # values = 
                    v = min(v, maxValue(gameState.generateSuccessor(agent, move), a, b, depth - 1))
                    
                else:

                    v = min(v, minValue(gameState.generateSuccessor(agent, move), a, b, depth,agent + 1))

                if v < a:
                    return v
                b = min(b, v)
            return v
        

        # Reference : 
        #   https://stackoverflow.com/questions/10188619/alpha-beta-pruning-does-it-need-a-extra-tree-data-structure
        bestMove = ''
        a = float("-inf")
        b = float("inf")
        validMoves = gameState.getLegalActions(0)
        for move in validMoves:
            v = minValue(gameState.generateSuccessor(0, move), a, b, self.depth,1)
            if v>a:
                a = v
                bestMove = move
        return bestMove       








        # def minValue(gameState,a,b):

        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

