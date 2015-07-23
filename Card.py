##
# Immutable collection of card attributes, which may be independently specified.
#
class Card(object):

  ##
  # Create a card without specifying any attributes.
  #
  @classmethod
  def blank(cls):
    return cls(None, None)

  ##
  # INPUT
  #   color: char
  #   number: integer
  #
  def __init__(self,color,number):
    self.color = color
    self.number = number

  def getColor(self):
    return self.color

  def getNumber(self):
    return self.number

  def setColor(self, color):
    self.color = color

  def setNumber(self, number):
    self.number = number

  def __str__(self):
    colorStr = "?"
    if self.color:
      colorStr = self.color
    numberStr = "?"
    if self.number:
      numberStr = str(self.number)
    return "[" + colorStr + " " + numberStr + "]"
