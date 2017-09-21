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
        # Three main things to consider
        # 1. Nearest Food pellet, total foods
        # 2. Nearest Ghost
        


        score =  successorGameState.getScore()
        fooddistances = []
        ghostdistances = []

        for food in newFood.asList():
            fooddistances.append(manhattanDistance(newPos, food))

        if len(fooddistances)>0:
            minFooddistance = min(fooddistances)
            score = score + (10.0/minFooddistance)  # food weight is taken as 10.0

        for ghost in newGhostStates:
            ghostdistances.append(manhattanDistance(newPos, ghost.getPosition()))
        minghostdistance = min(ghostdistances)
        
        if len(ghostdistances) >0 and minghostdistance !=0:
            score = score - (10.0/minghostdistance)  # ghost weight is taken as 10.0

        return score



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

        
        
        def maxValue(gameState,depth):
            # check if it is a terminal state, if yes then return utility
            if depth == 0 or gameState.isWin()==True or gameState.isLose() == True:
                return self.evaluationFunction(gameState)
            # Get valid moves
            validMoves = gameState.getLegalActions(0) #
            # calculatin v for each successor state for valid moves
            values = []
            for move in validMoves:
                # Next move is of the ghost after pacman
                values.append(minValue(gameState.generateSuccessor(0, move),1,depth))
            # Taking maximum of those values    
            v = max(values)              
            return v


        def minValue(gameState,agent,depth):
            if depth == 0 or gameState.isWin()==True or gameState.isLose() == True:
                return self.evaluationFunction(gameState)

            validMoves = gameState.getLegalActions(agent) 
            values = []

            numOfGhosts = gameState.getNumAgents()-1

            for move in validMoves:
                if(agent==numOfGhosts): # that means last ghost, so next move will be of pacman

                    values.append(maxValue(gameState.generateSuccessor(agent,move),depth-1))                    
                else:   
                # Penultimate ghost, next move of last ghost
                    values.append(minValue(gameState.generateSuccessor(agent,move),agent+1,depth))   # agent+1 =2
                    
                
            v = min(values)
            
            return v


        # Reference : 
        #   https://stackoverflow.com/questions/10188619/alpha-beta-pruning-does-it-need-a-extra-tree-data-structure

        # finding the best action for the corresponding v value
        bestMove = ''
        tmp = -999999
        validMoves = gameState.getLegalActions(0)
        for move in validMoves:
            v = minValue(gameState.generateSuccessor(0, move), 1, self.depth)
            if v>tmp:
                tmp = v
                bestMove = move
        return bestMove       






        
            


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # References:
        #   AI, A modern Approach pg 170
        #   https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
        #   

                   
        

        def maxValue(gameState,a,b,depth): # return utility value,[self.eval], and the move corresponding to the 
        
            if depth == 0 or gameState.isWin()==True or gameState.isLose() == True:
                return self.evaluationFunction(gameState)

            v = float('-inf') # v = -infi
            
            
            validMoves = gameState.getLegalActions(0) # pacman
            for move in validMoves:
                # value = minValue(gameState.generateSuccessor(0,move),a,b,depth,1)
                # v = max(v,value)
                v = max(v, minValue(gameState.generateSuccessor(0,move), a, b, depth, 1))

                if v>b:     # Pruning
                    return v
                a = max(a,v)
            
            
            return v
        
        
        def minValue(gameState, a, b, depth, agent):
            
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            v = float("inf")
            numOfGhosts = gameState.getNumAgents() - 1

            validMoves = gameState.getLegalActions(agent)
            
            for move in validMoves:
                
                if agent == numOfGhosts:    # that means last ghost, so next move will be of pacman
                    # values = 
                    v = min(v, maxValue(gameState.generateSuccessor(agent, move), a, b, depth - 1))
                    
                else:
                        # that means second last ghost, so next move will be of ghost 2
                    v = min(v, minValue(gameState.generateSuccessor(agent, move), a, b, depth,agent + 1))

                if v < a:   # Pruning
                    return v
                b = min(b, v)
            return v
        

        # Reference : 
        #   https://stackoverflow.com/questions/10188619/alpha-beta-pruning-does-it-need-a-extra-tree-data-structure

        # finding the best action for the corresponding v value
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

        # Reference:
        #   Expectimax pseudocode from slide 7

        def maxValue(gameState,depth):  # max value is same as minimax
            # check if it is a terminal state, if yes then return utility
            if depth == 0 or gameState.isWin()==True or gameState.isLose() == True:
                return self.evaluationFunction(gameState)
            # Get valid moves
            validMoves = gameState.getLegalActions(0) #
            # calculatin v for each successor state for valid moves
            values = []
            for move in validMoves:
                # Next move is of the ghost after pacman
                values.append(expValue(gameState.generateSuccessor(0, move),1,depth))
            # Taking maximum of those values    
            v = max(values)              
            return v


        def expValue(gameState,agent,depth):
            if depth == 0 or gameState.isWin()==True or gameState.isLose() == True:
                return self.evaluationFunction(gameState)

            validMoves = gameState.getLegalActions(agent) 
            values = []
            v = 0

            numOfGhosts = gameState.getNumAgents()-1

            for move in validMoves:        

                prob = float(1)/len(validMoves) # Probability = 1/(number of possible actions)

                if(agent==numOfGhosts): # that means last ghost, so next move will be of pacman
                    
                    # v + = p* value(successor)
                    v += prob*maxValue(gameState.generateSuccessor(agent,move),depth-1)                
                else:   
                # Penultimate ghost, next move of last ghost
                    
                    # v + = p* value(successor)
                    v += prob*expValue(gameState.generateSuccessor(agent,move),agent+1,depth)
                
            
           
            
            return v

        

        # Reference : 
        #   https://stackoverflow.com/questions/10188619/alpha-beta-pruning-does-it-need-a-extra-tree-data-structure

        # finding the best action for the corresponding v value
        bestMove = ''
        tmp = -999999
        validMoves = gameState.getLegalActions(0)
        for move in validMoves:        
            v = expValue(gameState.generateSuccessor(0, move), 1, self.depth)
            if v>tmp:
                tmp = v
                bestMove = move
        return bestMove    
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
    """
    "*** YOUR CODE HERE ***"

    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    powerPelletPos = currentGameState.getCapsules()


    # print powerPelletPos[0]
    score =  currentGameState.getScore()
    
    fooddistances = []
    ghostdistances = []
    powerPelletDistance = []



    for food in newFood.asList(): 
        w  =1
        for pellet in powerPelletPos:
            if pellet==food:
                print ('TES')  
                w = 50        # weight of 50 for power pellet
        fooddistances.append(w*manhattanDistance(newPos, food))



    if len(fooddistances)>0:
        minFooddistance = min(fooddistances)
        score = score + (10.0/minFooddistance)  # food weight is taken as 10.0

    for ghost in newGhostStates:
        w = 1
        if ghost.scaredTimer>0: 
            w= 100  # weight 100 for scared ghost, will try to eat it to get max points

        ghostdistances.append(w*manhattanDistance(newPos, ghost.getPosition()))
    minghostdistance = min(ghostdistances)
    
    if len(ghostdistances) >0 and minghostdistance !=0:
        score = score - (10.0/minghostdistance)  # ghost weight is taken as 10.0

    return score
   

# Abbreviation
better = betterEvaluationFunction

