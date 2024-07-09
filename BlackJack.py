# Gordon Andric
# Programming
# 24 June 7
# BlackJackBonus
# Enhance your Blackjack game

# Blackjack
# From 1 to 7 players compete against a dealer

import cards, games     

class BJ_Card(cards.Card):
    """ A Blackjack Card. """
    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v

class BJ_Deck(cards.Deck):
    """ A Blackjack Deck. """
    def populate(self):
        for suit in BJ_Card.SUITS: 
            for rank in BJ_Card.RANKS: 
                self.cards.append(BJ_Card(rank, suit))
    

class BJ_Hand(cards.Hand):
    """ A Blackjack Hand. """
    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()  
        if self.total:
            rep += " (" + str(self.total) + ")"        
        return rep

    @property     
    def total(self):
        # if a card in the hand has value of None, then total is None
        for card in self.cards:
            if not card.value:
                return None
        
        # add up card values, treat each Ace as 1
        t = 0
        for card in self.cards:
              t += card.value

        # determine if hand contains an Ace
        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True
                
        # if hand contains Ace and total is low enough, treat Ace as 11
        if contains_ace and t <= 11:
            # add only 10 since we've already added 1 for the Ace
            t += 10   
                
        return t

    def is_busted(self):
        return self.total > 21


class BJ_Player(BJ_Hand):
    """ A Blackjack Player. """
    def __init__(self, name, bankroll=100): # Bankroll keeps track of how much money
        super(BJ_Player, self).__init__(name)
        self.bankroll = bankroll
        # How much player bets
        self.bet = 0

    def is_hitting(self):
        response = self.ask_yes_no("\n" + self.name + ", do you want a hit? (y/n): ")
        return response == "y"

    def bust(self):
        print("\n" + self.name, "busts.")
        self.lose()

    def lose(self):
        print("\n" + self.name, "loses.")
        # If player loses remove amount of money betted from their total
        self.bankroll -= self.bet
        # if player does not run out of money, display their new balance else display that they ran out
        if self.bankroll != 0:
            print("\n" + self.name + "'s new balance is: $" + str(self.bankroll))
        else:
            print("\n" + self.name, "ran out of money!")
    
    def win(self):
        print("\n" + self.name, "wins.")
        # If player wins add amount of money they betted to their total 
        self.bankroll += self.bet
        print("\n" + self.name + "'s new balance is: $" + str(self.bankroll))

    def push(self):
        print("\n" + self.name, "pushes.")
        # If someone pushes keep the balance the same
        print("\n" + self.name + "'s balance stays the same at: $" + str(self.bankroll))

    # Ask user how much they would like to bet
    def make_bet(self):
        bet = self.ask_number(f"\n{self.name}, you have ${self.bankroll}. How much would you like to bet? ", 1, self.bankroll + 1)
        self.bet = bet

    @staticmethod
    def ask_yes_no(question):
        """Ask a yes or no question."""
        response = None
        while response not in ("y", "n"):
            response = input(question).lower()
            if response not in ("y", "n"):
                print("\nInvalid input. Please enter 'y' or 'n'.") # If user enters invalid input tell them and reprompt
      
        return response
                

    @staticmethod
    def ask_number(question, low, high):
        """Ask for a number within a range."""
        response = 0
        while not low <= response < high:
            try:
                # check if response is a integer
                response = int(input(question))
                if not low <= response < high:
                    # If user inputs a number within the range display to them invalid input and reprompt
                    print(f"\nInvalid input. Please enter a number between {low} and {high - 1}.")
            # If user does not enter a number for input
            except ValueError:
                # Display invalid input and reprompt
                print("\nInvalid input. Please enter a valid number.")
                
        return response


class BJ_Dealer(BJ_Hand):
    """ A Blackjack Dealer. """
    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "busts.")

    def flip_first_card(self):
        first_card = self.cards[0]  
        first_card.flip()


class BJ_Game(object):
    """ A Blackjack Game. """
    def __init__(self, names):      
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Dealer")
        
        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()
            
    def play(self):
        # Allow players to make their bets
        for player in self.players:
            player.make_bet() # prompt each player to make a bet
            
        print()

        # deal initial 2 cards to everyone
        self.deck.deal(self.players + [self.dealer], per_hand = 2)
        self.dealer.flip_first_card()    # hide dealer's first card
        for player in self.players:
            print(player)
        print(self.dealer)

        # deal additional cards to players
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()    # reveal dealer's first

        if not self.still_playing:
            # since all players have busted, show the dealer's hand
            print(self.dealer)
        else:
            # deal additional cards to dealer
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # everyone still playing wins
                for player in self.still_playing:
                    player.win()                    
            else:
                # compare each player still playing to dealer
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        # Remove players who have run out of money
        self.players = [player for player in self.players if player.bankroll > 0]

        if not self.players:
            print("All players are out of money! Game over.")
            return False  # End the game if all players are out of money

        # remove everyone's cards
        for player in self.players:
            player.clear()
        self.dealer.clear()
        
                
        # Clear deck, populate, and shuffle the deck every new round
        self.deck.clear()
        self.deck.populate()
        self.deck.shuffle()
        
        return True  # Continue the game

def main():
    print("\t\tWelcome to Blackjack!\n")
    
    names = []
    number = BJ_Player.ask_number("\nHow many players? (1 - 7): ", low = 1, high = 8)
    for i in range(number):
        name = input("\nEnter player name: ")
        names.append(name)
    print()
        
    game = BJ_Game(names)

    again = None
    while again != "n":
        if not game.play():
            break
        again = BJ_Player.ask_yes_no("\nDo you want to play again?(y/n): ")

main()
input("\n\nPress the enter key to exit.")
