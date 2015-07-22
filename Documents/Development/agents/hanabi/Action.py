## 
# Immutable message. Fields completely describe move intention, as it can be publicly observed
# by any agent. For example, play and discard indicate card position only, instead of card
# attributes. Draw is also represented in this message- again attributes of drawn card not
# contained.
# 
# SubjectAgent: agent declaring action, making the move
# ObjectAgent: in case of hint only, receives the hint
#
class Action(object):

  DRAW = 'draw'
  PLAY = 'play'
  DISCARD = 'dcrd'
  HINT = 'hint'

  @classmethod
  def createDrawAction(cls,subjectAgent):
    return cls(Action.DRAW,subjectAgent,None,None,None)

  @classmethod
  def createHintAction(cls,subjectAgent,objectAgent,hint):
    return cls(Action.HINT,subjectAgent,objectAgent,hint,None)

  @classmethod
  def createPlayAction(cls,subjectAgent,cardPos):
    return cls(Action.PLAY,subjectAgent,None,None,cardPos)

  @classmethod
  def createDiscardAction(cls,subjectAgent,cardPos):
    return cls(Action.DISCARD,subjectAgent,None,None,cardPos)

  def __init__(self,actionType,subjectAgent,objectAgent = None, hint = None, cardPos = None):
    self.actionType = actionType
    self.subjectAgent = subjectAgent 
    self.objectAgent = objectAgent
    self.hint = hint
    self.cardPos = cardPos

  def getType(self):
    return self.actionType

  def getSubjectAgent(self):
    return self.subjectAgent
 
  # None iff Action is not HINT
  def getObjectAgent(self):
    return self.objectAgent

  # None iff Action is not HINT
  def getHint(self):
    return self.hint

  # None iff Action is HINT or DRAW
  def getCardPos(self):
    return self.cardPos

  def __str__(self):
    if self.actionType == Action.HINT:
      return str(self.subjectAgent) + " tells " + str(self.objectAgent) + " " + str(self.hint)
    elif self.actionType == Action.DRAW:
      return str(self.subjectAgent) + " draws"
    else:
      return str(self.actionType) + ": " + str(self.subjectAgent) + ", " + str(self.cardPos)
