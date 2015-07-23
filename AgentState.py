##
# Mutable card container, backed by list. Note that card representation allows
# attributes to not be completely specified.
#
class AgentState(object):

  def __init__(self):
    self.cards = []

  def addCard(self,card):
    self.cards += [card]

  # returns card at given integer position
  def removeCard(self, position):
    return self.cards.pop(position)

  def getNumCards(self):
    return len(self.cards)

  def getCards(self):
    return self.cards

  def getCard(self, cardPos):
    return self.cards[cardPos]

  def __str__(self):
    return '[%s]' % ', '.join(map(str, self.cards))
