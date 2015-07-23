from Action import Action

##
# Fully or partially observed advancement of the game. Composed of an Action
# and optionally a card that is the outcome of a play, discard, or draw.
# The attributes of the card contained by the GameEvent can be either fully
# or partially specified.
#
class GameEvent(object):

  def __init__(self, action, card = None):
    self.action = action
    self.card = card

  def getAction(self):
    return self.action

  def getCard(self):
    return self.card

  def __str__(self):
    return " ".join(map(str,[self.action,self.card]))
