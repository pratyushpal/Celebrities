import random, time

from threading import Timer
  
## CONSTANTS

FULL = 0
DECKS = 1
SCORES = 2
T1 = 3
T2 = 4
MAXTIME = 60
DEBUG = True

def getWord():
  print('\n' * 30)
  return raw_input("Word: ")
  
def showWord(word):
  print "NEW WORD: {}".format(word)

## CLASSES

class Deck:
  
  def __init__(self):
    self.items = []

  def isEmpty(self):
    return self.items == []

  def push(self, item):
    self.items.append(item)

  def pop(self):
    return self.items.pop()

  def peek(self):
    return self.items[len(self.items)-1]

  def size(self):
    return len(self.items)
    
  def shuffle(self):
    for i in range(self.size() - 1, 0, -1):
      j = random.randint(0,i)
      temp = self.items[j]
      self.items[j] = self.items[i]
      self.items[i] = temp
    
  def draw(self):
    card = self.peek()
    self.pop()
    return card
  
  def insert_deck(self, deck2):
    while not deck2.isEmpty():
      self.push(deck2.draw())

class Team:
  
  def __init__(self, players):
    self.players = players
    self.active = 0
    self.points = 0
    self.score = 0
    self.yes = Deck()
    self.no = Deck()
  
  def clearPoints(self):
    self.points = 0
  
  def getPoints(self):
    return self.points
  
  def clearNo(self):
    self.no = Deck()
  
  def clearYes(self):
    self.yes = Deck()
  
  def remNo(self):
    retval = self.no
    self.clearNo()
    return retval
  
  def remYes(self):
    self.points += self.score
    self.score = 0
    retval = self.yes
    self.clearYes()
    return retval
  
  def add(self, item, correct):
    if correct:
      self.yes.push(item)
      self.score += 1
    else:
      self.no.push(item)

class Game:
  
  # Initialize game
  def __init__(self, players, rounds, cards):
    self.setup(players, rounds, cards)
  
  # Assign player count
  def setTeams(self, players):
    self.players = players
    p1 = players / 2
    p2 = players - p1
    self.team1 = Team(p1)
    self.team2 = Team(p2)
    if p1 == p2: self.active = random.randint(T1, T2)
    else: self.active = T1
  
  # Assign number of rounds
  def setMaxRound(self, rounds):
    self.maxRound = rounds
  
  # Set game data
  def setup(self, players, rounds, cards):
    self.round = 0
    self.time = MAXTIME
    self.setMaxRound(rounds)
    self.setTeams(players)
    self.fill(cards)
    self.shuffle()
    
  # Fill draw_pile with words
  def fill(self, cards):
    self.draw_pile = Deck()
    for i in range(0, self.players * cards):
      self.draw_pile.push(getWord())
    
  # Returns round #
  def getRound(self):
    return self.round
  
  # Returns relevant team scores in a tuple
  def score(self):
    self.round += 1
    return [self.team1.getPoints(), self.team2.getPoints(), self.round]
  
  # Shuffles words in draw_pile
  def shuffle(self):
    self.draw_pile.shuffle()
    
  # Switch active team
  def switch(self):
    if self.active == T1: self.active = T2
    else: self.active = T1
    
  # Move active no pile back into draw_pile amd shuffle
  def turnUpdate(self):
    self.timer.cancel()
    self.draw_pile.insert_deck(self.team1.remNo())
    self.draw_pile.insert_deck(self.team2.remNo())
    self.switch()  
  
  # Does something during tick
  def tickAction(self):
    if self.time > 0:
      if DEBUG: print(self.time)
      self.time -= 1
      self.timer.cancel()
      if not self.roundOver():
        self.tick()
    else:
      self.turnUpdate()
      self.timer.cancel()
      if not self.roundOver():
        print "Team {}, pass the phone".format({self.active - 2})
        self.time = MAXTIME
        self.show()
  
  # Ticks the timer
  def tick(self):
    self.timer = Timer(1, self.tickAction)
    self.timer.start()
  
  # Displays a drawn word, adds to team's collection
  def newWord(self):
    self.card = self.draw_pile.peek()
    self.show()
    x = raw_input()
    if not self.roundOver():
      if self.active == T1:
        self.team1.add(self.draw_pile.draw(), x == "Y")
      else:
        self.team2.add(self.draw_pile.draw(), x == "Y")
  
  def show(self):
    showWord(self.card)
    self.tick()
  
  # Returns true if active no pile is empty
  def activeEmpty(self):
    if self.active == T1: self.team1.no.isEmpty()
    else: return self.team2.no.isEmpty()
  
  # Returns true if draw_pile is empty
  def drawEmpty(self):
    return self.draw_pile.isEmpty()
  
  # Returns true if there are no more cards to draw from
  def roundOver(self):
    return (self.drawEmpty() and (self.activeEmpty() == None))
  
  # Reset some data to start new round
  def roundUpdate(self):
    if DEBUG: print "ROUND UPDATE"
    self.draw_pile.insert_deck(self.team1.remYes())
    self.draw_pile.insert_deck(self.team2.remYes())
  
  # Plays through a single round of the game
  def roundPlay(self):
    
    if DEBUG: print "ROUND START"
    
    while not self.roundOver():
      if self.roundOver(): break
      
      if self.drawEmpty():
        if self.active == T1: self.draw_pile.insert_deck(self.team1.remNo())
        else: self.draw_pile.insert_deck(self.team2.remNo())
      
      if not self.drawEmpty(): self.newWord()
    
    self.roundUpdate()
    self.timer.cancel()
    
    return self.score()

## TESTING

def test():
  p = input("How many players? ")
  r = input("How many rounds? ")
  c = input("How many cards per player? ")

  game = Game(p, r, c)

  score = game.roundPlay()
  while(score[2] + 1 < r):
    print 'ROUND {} END'.format(game.getRound())
    if score[0] > score[1]:
      print 'TEAM 1 LEADS {} : {}'.format(score[0], score[1])
    elif score[0] == score[1]:
      print 'TIED {} : {}'.format(score[0], score[0])
    else:
      print 'TEAM 2 LEADS {} : {}'.format(score[1], score[2])
    if (game.getRound()):
      score = game.roundPlay()
