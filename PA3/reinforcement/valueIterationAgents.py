# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # print mdp.getStates()
      

         
        for i in range(iterations):
            op = util.Counter() # keeping track of values in this , temporary, initialised with all 0

            possibleStates = mdp.getStates()
            
            for state in possibleStates:
                maxQ = None # set initial Q value to find max

                possibleActions = mdp.getPossibleActions(state)

                for action in possibleActions:
                    # Calculate Q value for the state action pair
                    QValue = self.computeQValueFromValues(state, action)
                    # Find max Q value
                    if QValue>maxQ:
                        maxQ = QValue
                    # update with state and max Q value
                    op[state] = maxQ           
                
            # Replace values with the temporary storage.    
            self.values = op            



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        Qvalue = 0
        # print self.mdp.getTransitionStatesAndProbs(state,action)
        # nextState is S'
        for nextState,prob in self.mdp.getTransitionStatesAndProbs(state,action):

            # Q = prob*(reward(state,prob,nextState) + discount*value(nextState))
            Qvalue += prob*(self.mdp.getReward(state,prob,nextState)+self.discount*self.values[nextState])

        return Qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # Best action is the one with the highest Q value

        baseQValue = None    
        bestAction = None   # Also takes care of terminal States
        # pair = dict()
        possibleActions = self.mdp.getPossibleActions(state)
        for action in possibleActions:
            QValue = self.computeQValueFromValues(state,action)

            # Find the max Q value and then return the action associated with it.
            if QValue>baseQValue:
                baseQValue = QValue
                bestAction = action
      
        return bestAction
        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
