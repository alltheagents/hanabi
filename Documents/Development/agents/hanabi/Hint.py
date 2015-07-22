##
# Immutable, publically observable message to indicate an attribute of one or more cards
# in a particular players hand. A HINT type Action would contain a Hint plus a hinter
# Agent and an Agent who receives the Hint.
#
class Hint(object):

  @classmethod
  def createColorHint(cls, cardPositions, color):
    return cls(cardPositions,color,None)

  @classmethod
  def createNumberHint(cls, cardPositions, number):
    return cls(cardPositions,None,number)

  def __init__(self, cardPositions, color = None, number = None):
    self.cardPositions = cardPositions
    self.color = color
    self.number = number

  def getCardPositions(self):
    return self.cardPositions

  def getColor(self):
    return self.color

  def getNumber(self):
    return self.number

  def __str__(self):
    colorOrNumber = None
    if self.color:
      colorOrNumber = self.color
    elif self.number:
      colorOrNumber = self.number
    return " ".join([", ".join(map(str,self.cardPositions)), "are", str(colorOrNumber)])
