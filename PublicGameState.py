from Rules import Rules

##
# "On the table" attributes of the current state of a game of Hanabi. Includes
# progress of fireworks, counters for bombs and bombs, discard pile, deck size,
# whose turn it is, and who is playing the game.
#
# Incrementally mutable.
#
class PublicGameState(object):
  def __init__(self,agents):
    self.turn = 0
    self.agents = agents
    self.discardPile = []
    self.bombsRemaining = 4
    self.hintsRemaining = 8
    self.cardsInDeckRemaining = 50
    self.fireworks = {}
    for color in Rules.COLORS():
      self.fireworks[color] = 0

  ## GET STATE METHODS

  def getCurrentPlayer(self):
     return self.agents[self.turn % len(self.agents)]

  def getDiscardPile(self):
    return self.discardPile

  def getFireworkProgress(self):
    return sum(self.fireworks.values())

  def getFireworks(self):
    return self.fireworks

  def getBombsRemaining(self):
    return self.bombsRemaining

  def getHintsRemaining(self):
    return self.hintsRemaining

  def getCardsInDeckRemaining(self):
    return self.cardsInDeckRemaining

  ## MODIFY STATE METHODS
 
  def advanceTurn(self):
    self.turn += 1

  def cardMinus(self):
    self.cardsInDeckRemaining -= 1
   
  def addToPile(self, color):
    self.fireworks[color] = self.fireworks[color] + 1

  def hintMinus(self):
    self.hintsRemaining -= 1

  def hintPlus(self):
    self.hintsRemaining += 1

  def discardAppend(self, card):
    self.discardPile.append(card)

  def bombPlus(self):
    self.bombsRemaining -= 1

  def __str__(self):
    return " ".join(map(str,
        ["state=",
         "turn", self.turn,
         "deck", self.cardsInDeckRemaining,
         "bombs", self.bombsRemaining,
         "hints", self.hintsRemaining,
         "discard", ", ".join(map(str, self.discardPile)), 
         ", ".join(map(str, [self.fireworks]))
        ]))
         
