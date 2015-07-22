from Action import Action
from GameEvent import GameEvent
from Agent import Agent
from Agent import RandomAgent
from Agent import ObviousMoveOrRandomAgent
from AgentState import AgentState
from Rules import Rules
from PublicGameState import PublicGameState
from Card import Card

import random
import copy
import sys

##
# for printing colors to terminal.
#
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class printer:
  verbose = False

##
# INPUT:
#  argv[0]: whether to print all debug game information
#  argv[1]: number of games to play
def main(argv):
  print "args: " + str(argv)
  # params  
  printer.verbose = int(argv[0])
  gamesToPlay = int(argv[1])
  cardsToDraw = 5
  numAgents = 1
  
  # START
  print "WELCOME TO HANABI"

  # params  
  cardsToDraw = 5
  numAgents = 1
 
  # game stats
  totalProgress = 0 
  progressHist = {}
  for gameNumber in range(0,gamesToPlay):
    # agents
    ari = ObviousMoveOrRandomAgent("ari")
    ben = ObviousMoveOrRandomAgent("ben")
    col = ObviousMoveOrRandomAgent("col")
    agents = [ari, ben, col]
    agentStates = {}
    for a in agents:
      a.introducePlayers(agents)
      agentStates[a] = AgentState()

    # init state
    gameState = PublicGameState(agents)   
    deck = makeRandomDeck()
    for i in range(0,cardsToDraw):
      for a in agents:
        drawCard(a, deck, gameState, agentStates)    
    
    # play
    while deck and (gameState.getBombsRemaining() > 0):
      currAgent = gameState.getCurrentPlayer()
      move = currAgent.makeMove()
      executeMove(move, deck, gameState, agentStates)
      gameState.advanceTurn()

    # end
    print str(gameState)
    progress = gameState.getFireworkProgress()
    totalProgress += progress
    if progress not in progressHist:
      progressHist[progress] = 0
    progressHist[progress] = progressHist[progress] + 1

  # GAMES SUMMARY
  print "avg progress:   " + str(totalProgress/float(gamesToPlay))
  print "progress hist:  " + str(progressHist)
  exit()


#############################################################

def executeMove(action, deck, gameState, agentStates):
  subjAgent = action.getSubjectAgent()

  type = action.getType()
  # PLAY
  if type == Action.PLAY:
    cardPos = action.getCardPos()
    cardPlayed = agentStates[subjAgent].removeCard(cardPos)
    colorPileTop = gameState.getFireworks()[cardPlayed.getColor()]
    if colorPileTop + 1 == cardPlayed.getNumber():
      gameState.addToPile(cardPlayed.getColor())
      if printer.verbose: print bcolors.OKGREEN + " ".join([str(subjAgent),"plays",str(cardPlayed)]) + bcolors.ENDC
    else:
      gameState.discardAppend(cardPlayed)
      gameState.bombPlus()
      if printer.verbose: print bcolors.FAIL + "bomb!" + bcolors.ENDC
    for key in agentStates:
      key.observeEvent(GameEvent(action, cardPlayed))
    drawCard(subjAgent, deck, gameState, agentStates)
  # DISCARD
  if type == Action.DISCARD:
    cardPos = action.getCardPos()
    cardDiscarded = agentStates[subjAgent].removeCard(cardPos)
    gameState.discardAppend(cardDiscarded)
    gameState.hintPlus()
    drawCard(subjAgent, deck, gameState, agentStates)
    for key in agentStates:
      key.observeEvent(GameEvent(action, cardDiscarded))
  # HINT
  if type == Action.HINT:
    gameState.hintMinus()
    for key in agentStates:
      key.observeEvent(GameEvent(action))
      
 
def drawCard(agent, deck, gameState, agentStates):
  card = deck.pop()
  agentStates[agent].addCard(card)
  gameState.cardMinus()
  agent.observeEvent(GameEvent(Action.createDrawAction(agent), Card.blank()))
  for key in agentStates:
    if key is agent:
      continue
    key.observeEvent(GameEvent(Action.createDrawAction(agent), card)) 
  if printer.verbose: print str(agent) + " draws " + str(card)

def makeRandomDeck():
  deck = []
  for color in Rules.COLORS():
    for number in [1,1,1,2,2,3,3,4,4,5]:
      deck += [Card(color,number)]
  random.shuffle(deck)
  if printer.verbose: print "shuffling new deck"
  if printer.verbose: print '[%s]' % ', '.join(map(str, deck))
  return deck

if __name__ == "__main__":
    main(sys.argv[1:])
