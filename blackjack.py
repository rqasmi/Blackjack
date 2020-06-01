"""
@author: Ragheed


This program implements a simple 1-player interactive blackjack game who plays against the house (bot). The game rules are as follows:

The player is dealt two cards, face up. The house is dealt two cards, one up (exposed) and one down (hidden). 
The value of cards two through ten is their pip value (2 through 10). Face cards (Jack, Queen, and King) are all worth ten. 
Aces can be worth one or eleven. A hand's value is the sum of the card values. Players are allowed to draw additional 
cards ('hit') to improve their hands. A hand with an ace valued as 11 is called "soft", meaning that the hand will not bust 
by taking an additional card. The value of the ace will become one to prevent the hand from exceeding 21. 
Otherwise, the hand is called "hard".

Once the player has completed his hand, it is the house's turn. The house hand will not be completed if the player 
has received a blackjack or busted. The house then reveals the hidden card and must hit until the cards total up to 17 points. 
At 17 points or higher the house must stay. The house also hits on a "soft" 17, i.e. a hand containing an ace and one or 
more other cards totaling six.) You are betting that you have a better hand than the house. The better hand is the hand 
where the sum of the card values is closer to 21 without exceeding 21. The detailed outcome of the hand follows:

- If the player is dealt an Ace and a ten-value card (called a "blackjack"), and the house does not, the player 
wins receives a bonus.
- If the player exceeds a sum of 21 ("busts"); the player loses, even if the house also exceeds 21.
- If the house exceeds 21 ("busts") and the player does not; the player wins.
- If the player attains a final sum higher than the house and does not bust; the player wins.
- If both house and player receive a blackjack or any other hands with the same sum, called a "push", no one wins.

"""

from random import shuffle
from model import Card, Player, RegularPlayer, House

blackjack = 21
house_limit= 17

def createDeck():
  """ Create and return shuffled deck as array of cards."""
  Deck = []
  face_values = ["A", "J", "Q", "K"]
  suit_list = ["Hearts", "Diamonds", "Spades", "Clubs"]
  for suit in suit_list:
    for num_val in range (2, 11):
      Deck.append(Card(str(num_val), num_val))
    for face_val in face_values:
      Deck.append(Card(face_val, Card.face_card_dict.get(face_val)))

  shuffle(Deck)
  return Deck


def gameTeardown(house, player):
  print(Player.__str__(house))
  print(player, end="\n\n")


def getBet(player):
  "Reads in and returns bet amount of input player."
  get_bet = False
  while(not get_bet):
    bet = input("Please enter your bet amount:\n>")
    try:
      if float(bet) < 0:
        print("Your bet should be greater than 0\n")
        continue
      elif float(bet) > player.money:
        print("Your don't have enough money to bet an amount of $", bet, "\n")
        continue
    except ValueError:
      print("Bet amount must be a numerical value.\n")
      continue
    get_bet = True

  return float(bet)

def play(player, house, deck):
  """ Play function logic for one round."""
  bet = getBet(player)
  print("You bet an amount of", bet, "\n")
  player.betMoney(bet)
  print(house)
  print(player, end="\n\n")

  if player.hasBlackjack():
    if house.hasBlackjack():
      player.draw()
      gameTeardown(house, player)
      print("You both have a blackjack. The round ended in a draw.")
      print(f"Your money is now: {player.money}")
      return
    else:
      player.win(True)
      gameTeardown(house, player)
      print("Congrats!! You attained a blackjack and won 1.5 times your bet!")
      print(f"Your money is now: {player.money}\n")
      return

  while(player.score < blackjack):
    action = input("Do you want another card?(y/n): ")
    if action.upper() == 'Y':
      player.hit(deck.pop())
      if player.bust():
        player.win(False)
        gameTeardown(house, player)
        print("You busted and lost your bet!!")
        print(f"Your money : {player.money}\n")
        return
      print(house)
      print(player, end= "\n\n")    
    elif action.upper() == 'N':
      break
    else:
      print("Please enter 'y' or 'n'.")
    
  while(house.score < house_limit):
    house.hit(deck.pop())

  gameTeardown(house, player)

  if house.bust() or player.score > house.score:
    player.win(True)
    print("Congrats!! You won your bet!")
    print(f"Your money is now: {player.money}\n")
  elif player.score < house.score:
    player.win(False)
    print("You lost your bet!")
    print(f"Your money is now: {player.money}\n")
  else:
    player.draw()
    print("The round ended in a draw.")
    print(f"Your money is now: {player.money}\n")

def main():
  """ Main function to play continuously."""
  name = input("Please enter your name: ")
  cardDeck = createDeck()
  if not name.isalpha():
    player = RegularPlayer([cardDeck.pop(), cardDeck.pop()])
  else:
    player = RegularPlayer([cardDeck.pop(), cardDeck.pop()], name+"'s")
  house = House([cardDeck.pop(), cardDeck.pop()])
  play(player, house, cardDeck)
  while(True):
    if not player.isBroke():
      action = input("Do you want to play another time?(y/n):\n>")
      if action.upper() == 'Y':
        cardDeck = createDeck()
        player.play([cardDeck.pop(), cardDeck.pop()])
        house.play([cardDeck.pop(), cardDeck.pop()])
        play(player, house, cardDeck)
      else:
        print("See you soon again!")
        return
    else:
      print("You're out of money! Maybe next time!")
      return

main()



