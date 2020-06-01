""" This model.py file contains the classes used to implement the game. It defines a main player class with two classes: regular
player and house (dealer) that inherit from the player class. There is also a Card class that models a card in the game.
"""

blackjack = 21

class Player:
  def __init__(self, name, hand = []):
    self.name = name
    self.hand = hand
    self.setScore()

  def __str__(self):
    return self.name + " cards: "  + " ".join(card.str_val for card in self.hand) + " , score: " + str(self.score)

  def setScore(self):
    aceCounter = 0
    self.score = 0
    for card in self.hand:
      self.score += card.score_val
      if card.str_val == "A":
        aceCounter += 1
      if self.score > blackjack and aceCounter != 0:
        self.score -= 10
        aceCounter -= 1

  def hit(self, card):
    self.hand.append(card)
    self.setScore()

  def play(self, new_hand):
    self.hand = new_hand
    self.setScore()

  def hasBlackjack(self):
    return self.score == blackjack and len(self.hand) == 2

  def bust(self):
    return self.score > blackjack


class House(Player):
  def __init__(self, hand, name="House"):
    Player.__init__(self, name, hand)
  
  def __str__(self):
    result = self.name + "'s cards: "
    for card in range(len(self.hand)):    
      if card == 0:
        result += "X "
      else:
        result += self.hand[card].str_val + " "
    return result


class RegularPlayer(Player):
  def __init__(self, hand, name="Your", money = 100):
    Player.__init__(self, name, hand)
    self.money = money
    self.bet = 0

  def betMoney(self, amount):
    self.money -= amount
    self.bet += amount

  def win(self, result):
    if result == True:
      if self.hasBlackjack():
        self.money += 2.5 * self.bet
      else:
        self.money += 2* self.bet
      self.bet = 0
    else: 
      self.bet = 0

  def draw(self):
    self.money += self.bet
    self.bet = 0

  def isBroke(self):
    return self.money == 0

class Card:
  face_card_dict = {"A": 11, "J": 10, "Q": 10, "K": 10}

  def __init__(self, str_val, score_val):
    self.str_val = str_val
    self.score_val = score_val

  def __repr__(self):
    return self.str_val
