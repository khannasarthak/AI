# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.QValues =  util.Counter()  # default values are 0 

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # No need to check if state not seen as default value is 0 in QValues
        return self.QValues[(state,action)]



    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        legalActions = self.getLegalActions(state)

        QValues = [] # store all Q values

        for action in legalActions:
            QValues.append(self.getQValue(state,action))

        if QValues == []: # Terminal state with no legal actions
            return 0.0

        return max(QValues) # returns max action

        


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        baseQValue = None    
        bestAction = None
        # pair = dict()
        legalActions = self.getLegalActions(state)

        # Terminal Case
        if len(legalActions)==0:
            return None

        for action in legalActions:
            QValue = self.getQValue(state,action)

            # Find the max Q value and then return the action associated with it.
            if QValue>baseQValue:
                baseQValue = QValue
                bestAction = action

      
        return bestAction

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        legalActions = self.getLegalActions(state)


        # Terminal Case
        if len(legalActions)==0:    
            return None

        # using simple greedy elipson policy, if true, Explore randomly with low prob (p) else act on existing Q values with high prob (1-p)
        if util.flipCoin(self.epsilon)==True:
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(state)       

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # From slides
        QSample = reward + self.discount*self.getValue(nextState)
        
        self.QValues[(state,action)] = (1-self.alpha)*self.QValues[(state,action)] + self.alpha*QSample


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # summation of features * weights

        totalQ = 0

        features = self.featExtractor.getFeatures(state,action)

        for feature in features:
            
            # print ('F---'.features)
            # print ('~~~',features[feature],'W~~~',self.weights[feature])

            totalQ += self.getWeights()[feature]*features[feature]

        # print ('TOTAL_______________________',totalQ)
        return totalQ

     

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        features = self.featExtractor.getFeatures(state,action)
        difference = 0 

        # use getQvalue

        # When difference was calculated in the loop, 3/5 test cases were being passed.
        difference = (reward + self.discount*self.computeValueFromQValues(nextState))-self.getQValue(state,action)

        for feature in features:           

            self.getWeights()[feature]= self.getWeights()[feature]+ self.alpha*difference*features[feature]

            # print self.getWeights()[feature]


        

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass



# python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -lmediumGrid