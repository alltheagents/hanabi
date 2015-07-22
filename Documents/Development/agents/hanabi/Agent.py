from Rules import Rules
from Action import Action
from PublicGameState import PublicGameState
from Hint import Hint
from AgentState import AgentState

import random

##
# Abstract cooperative player with limited game state information.
#
class Agent(object):
  def makeMove(self):
    pass
  
  ##
  # Update this agent with a message that describes how the game has
  # advanced, from this agent's (limited) perspective.
  #
  def observeEvent(self, gameEvent):
    self.events.append(gameEvent)
    action = gameEvent.getAction()
    actionType = action.getType()

    subjAgent = gameEvent.getAction().getSubjectAgent()
    if actionType == Action.DRAW:
      self.agentStates[subjAgent].addCard(gameEvent.getCard())
      self.gameState.cardMinus()
    elif actionType == Action.PLAY:
      cardPlayed = gameEvent.getCard()  
      self.agentStates[subjAgent].removeCard(gameEvent.getAction().getCardPos())
      colorPileTop = self.gameState.getFireworks()[cardPlayed.getColor()]
      if colorPileTop + 1 == cardPlayed.getNumber():
	self.gameState.addToPile(cardPlayed.getColor())
      else:
	self.gameState.discardAppend(cardPlayed)
	self.gameState.bombPlus()
      self.gameState.advanceTurn()
    elif actionType == Action.DISCARD:
      cardPlayed = gameEvent.getCard()
      self.agentStates[subjAgent].removeCard(gameEvent.getAction().getCardPos())
      self.gameState.discardAppend(cardPlayed)
      self.gameState.hintPlus() 
      self.gameState.advanceTurn()
    elif actionType == Action.HINT:
      hint = action.getHint()
      cardPositions = hint.getCardPositions()
      objAgent = action.getObjectAgent()
      objAgentCards = self.agentStates[objAgent].getCards()
      if hint.getColor():
        for cardPos in cardPositions:
          objAgentCards[cardPos].setColor(hint.getColor())
      if hint.getNumber():
        for cardPos in cardPositions:
          objAgentCards[cardPos].setNumber(hint.getNumber())
      self.gameState.advanceTurn()
      self.gameState.hintMinus()

  ##
  # Create new Agent with no game context and no prior knowledge. This agent is not
  # ready to play a new game until its other cooperative agents have been introduced
  # to it.
  def __init__(self,name):
    self.name = name
    self.gameState = None
    self.agentStates = {}
    self.events = []

  ##
  # Players must be introduced before the game starts.
  #
  def introducePlayers(self, agents):
    self.gameState = PublicGameState(agents)
    for agent in agents:
      self.agentStates[agent] = AgentState()
  
  def __str__(self):
    return self.name

##
# Agent that choices every possible action available to it with equal probability.
#
class RandomAgent(Agent):
  
  def makeMove(self):
    possibleActions = []
    # add possible PLAYs, DISCARDs
    for cardPos in range(0, len(self.agentStates[self].getCards())):
      possibleActions.append(Action.createPlayAction(self,cardPos))
      possibleActions.append(Action.createDiscardAction(self,cardPos))
    # add possible HINTs
    if self.gameState.getHintsRemaining():
      for key in self.agentStates:
        # can't hint myself
        if self is key:
          continue
        else:
          objectAgent = key
          colors = {}
          numbers = {}
          for cardPos in range(0, self.agentStates[key].getNumCards()):
            card = self.agentStates[key].getCard(cardPos)
            color = card.getColor()
            if not color in colors:
              colors[color] = []
            colors[color].append(cardPos)
            number = card.getNumber()
            if not number in numbers:
              numbers[number] = []
            numbers[number].append(cardPos)
          for key in colors:
            possibleActions.append(Action.createHintAction(self,objectAgent,Hint.createColorHint(colors[key],key)))
          for key in numbers:
            possibleActions.append(Action.createHintAction(self,objectAgent,Hint.createNumberHint(numbers[key],key)))

    move = random.choice(possibleActions)
    return move

class ObviousMoveOrRandomAgent(RandomAgent):

  def makeMove(self):
     productiveActions = []
     for cardPos in range(0, len(self.agentStates[self].getCards())):
       card = self.agentStates[self].getCards()[cardPos]
       if self.isProductivePlay(card):
         productiveActions.append(Action.createPlayAction(self,cardPos))
     
     if productiveActions:
       return random.choice(productiveActions)
     else:
       return super(ObviousMoveOrRandomAgent, self).makeMove()

  def isProductivePlay(self, card):
    if card.getNumber() and card.getColor():
      colorPileTop = self.gameState.getFireworks()[card.getColor()]
      return colorPileTop + 1 == card.getNumber()
    elif card.getNumber():
      toReturn = True
      for color in Rules.COLORS():
        colorPileTop = self.gameState.getFireworks()[color]
        toReturn = toReturn and colorPileTop + 1 == card.getNumber()
      return toReturn
    else:
      return False
