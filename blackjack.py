import random


class BlackJack:
    balance = 2000
    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    rank = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    def __init__(self, name, players=1):
        self.name = name
        self.players = players
        print(f"\nWELCOME TO BLACKJACK {self.name.upper()}, GOODLUCK!!")

    def start_of_game(self):
        #pop up message welcoming the user wuth name and balance
        print(f"BALANCE: {self.balance}$")
        print("REACH 10000$ TO WIN!\n")

    def game_control(self, user_bet):
        #this method checks if bets is well within the balance limit else request a try again by returning false
        if not is_float(user_bet):
            print(f"\n{user_bet} is not a valid number. TRY AGAIN!!.")
            print(f"BALANCE: {self.balance}$\n")
            return False
        elif float(user_bet) > self.balance:
            print(f"\nBets is greater than Balance. TRY AGAIN!!!")
            print(f"BALANCE: {self.balance}$\n")
            return False
        
        else:
            self.bet = float(user_bet)
            self.balance -= (self.bet)
            return True
        
    def variables_restart(self):
        #restarting temporary variable of the class to make sure the mechanincare continoius
        self.cards = [] #we add all the ranks we got to the list
        self.dealer_display = [] #all the text we will show that belongs to the player
        self.player_display = [] #all the text we will show that belongs to the dealer
        self.player_total = 0 #the total number of combing the ranks of the players cards
        self.dealer_total = 0 #the total number of combing the ranks of the dealers cards
        self.first_display = True #this crucial to tell if its first display or not, to hide the dealer's second card
        self.choice = False #this tell us if the player is still making choices or not, default being no/false
        self.restart = False # this tell us to restart the game cause we have winner or loser
        self.player_ace = False # this tell us if player has ace or not
        self.blackjack = False # checks if player blackjack after first deal or no
        self.dealer_ace = False # tells us if player has ace or not
        self.deck = deck = [(r, s) for r in self.rank for s in self.suits]
    def pick(self):
        
        random.shuffle(self.deck)
        rank_r = random.randrange(len(self.deck))
        return self.deck.pop(rank_r)
     
    def dealing(self):
        #restating here everytime i deal
        self.variables_restart()

        #using random and suits and rank list to distrubute cards between player and dealer and putting them into class variables
        #as well ass updating info that checks if player has ace
        
        
        for i in range((self.players + 1) * 2):
            dealt = self.pick()
            self.cards.append(dealt[0])
            if self.cards[-1] in ['J', 'K', 'Q']:
                self.cards[-1] = 10
            if i % 2 == 0:
                self.player_display.append(f"{dealt[0]} of {dealt[1]}")
                self.player_total += int(self.cards[-1])
                if int(self.cards[-1]) == 1:
                    self.player_ace = True
            else:
                self.dealer_display.append(f"{dealt[0]} of {dealt[1]}")
                self.dealer_total += int(self.cards[-1])
                if int(self.cards[-1]) == 1:
                    self.dealer_ace = True

    def instant_win(self):

        # this method continoiusly check if the player has met the winning requirements by using ace and checking if they have it
        if self.first_display and self.player_ace:
            if self.player_total == 11:
                self.player_total = 21
                self.blackjack = True
        elif not self.first_display and self.player_ace:
            if self.player_total + 10 == 21:
                self.player_total = 21
        if self.restart and self.player_ace:
            if self.player_total > 21 or self.player_total > self.dealer_total:
                return
            if self.player_total + 10 <= 21:
                self.player_total += 10
    
    def instant_lose(self):

        # just like instant win, checks if dealer has meet requiremnts he needs to make player lose by using ace and checking dealer has ace
        if self.first_display and self.dealer_ace:
            if self.dealer_total == 11:
                self.dealer_total = 21
        elif not self.first_display and self.dealer_ace:
            if self.dealer_total + 10 == 21:
                self.dealer_total = 21
        if not self.choice and self.dealer_ace:
            if self.dealer_total > 21 or self.player_total < self.dealer_total:
                return
            if self.dealer_total + 10 <= 21:
                self.dealer_total += 10


    def display(self):  
        #displays the players and dealer cards, but if first display or player still making decisions, it diSplays one card of course
        if self.first_display:
            print(f"\nYour Cards are {self.player_display[0]} and {self.player_display[1]}.")
            print(f"The Dealer's card is {self.dealer_display[0]}.")
            self.first_display = False
        elif self.choice:
            print(f"\nYour Cards are", end=" ")
            for i in self.player_display:
                print(i, end=", ")
            print(f"\nThe Dealer's card is {self.dealer_display[0]}.")
        else:
            print(f"\nYour Cards are", end=" ")
            for i in self.player_display:
                print(i, end=", ")
            print("\n")
            print(f"The Dealer's cards are", end=" ")
            for i in self.dealer_display:
                print(i, end=", ")
            print("\n")

    
    def options(self, decision):
        # this method receives info from user, if he wants to hit or stand, it deals the player another cards if hits
        if decision.lower() not in ["hit", "stand"]:
            print(f"\n{decision} is not a valid option. TRY AGAIN!!.", end="\n")
            return False
        if decision.lower() == "hit":
            dealt = self.pick()
            self.cards.append(dealt[0])
            if self.cards[-1] in ['J', 'K', 'Q']:
                self.cards[-1] = 10
            self.player_display.append(f"{dealt[0]} of {dealt[1]}")
            self.player_total += int(self.cards[-1])
            if int(self.cards[-1]) == 1:
                self.player_ace = True
            self.choice = True
            return False
        self.choice = False
        return True
    
    def last_deal(self):
        #this method makes sure the dealer has higher cards total than 17 in ordeer to go to final caluculation
        self.instant_lose()
        while self.dealer_total < 17:
            dealt = self.pick()
            self.cards.append(dealt[0])
            if self.cards[-1] in ['J', 'K', 'Q']:
                self.cards[-1] = 10
            self.dealer_display.append(f"{dealt[0]} of {dealt[1]}")
            self.dealer_total += int(self.cards[-1])
            self.instant_lose()
        self.restart = True

    def status(self):
        #the final method is for final calculation after all cards are dealt, checks who is winner or loser, also check after the first deal if its blackjack
        winnings = ((self.bet) * 1.5) + (self.bet)
        if self.player_total == 21 and self.blackjack:
            print("\n")
            print(f"Congratulations, You have Won {winnings}$!! BLACKJACK!!!!")
            self.balance += winnings
            self.restart = True
            return
        if not self.first_display and self.choice:
            print("\n")
            if self.player_total > 21:
                print(f"Try Again, You have Lost {self.bet}$!!")
                self.restart = True
            elif self.player_total == 21:
                print(f"Congratulations, You have Won {winnings}$!!")
                self.balance += winnings
                self.restart = True
        elif not self.first_display and self.restart:
            if self.dealer_total > 21:
                print(f"Congratulations, You have Won {winnings}$!!")
                self.balance += winnings
            elif self.dealer_total < self.player_total:
                print(f"Congratulations, You have Won {winnings}$!!")
                self.balance += winnings
            elif self.player_total < self.dealer_total:
                print(f"Try Again, You have Lost {self.bet}$!!")           
            elif self.player_total == self.dealer_total:
                print(f"Oops!! Push Push, Try Again.")
                self.balance += self.bet
            
        





        
    



def play_blackjack():
    # requesting the name of the user for welcoming and ending purposes
    name = input("Your Name: ")

    #creating an instance of blackjack, the game is about to start
    blackjack_1 = BlackJack(name) 
    while True:
        blackjack_1.start_of_game()

        # requesting user's bet compared to balance before dealing and checking if he provides correct value

        user_bets = input(f"Place your bets: ")

        bet_status = blackjack_1.game_control(user_bets)
        while(bet_status != True):
            user_bets = input(f"Place your bets: ")
            bet_status = blackjack_1.game_control(user_bets)
        blackjack_1.dealing()
        blackjack_1.instant_win()
        blackjack_1.instant_lose()
        blackjack_1.display()
        blackjack_1.status()

        if not blackjack_1.restart:
            print("\n")
            decision = input(f"Hit or Stand: ")
            game = blackjack_1.options(decision)
            while game != True:
                blackjack_1.instant_win()
                blackjack_1.display()
                blackjack_1.status()
                if blackjack_1.restart == True:
                    break
                decision = input(f"Hit or Stand: ")
                game = blackjack_1.options(decision)
            if not blackjack_1.restart:
                blackjack_1.last_deal()
                blackjack_1.display()
                blackjack_1.status()

        if blackjack_1.balance <= 0:
            print(f"GAME OVER!!!")
            return
        elif blackjack_1.balance >= 10000:
            print(f"CONGRATULATIONS, YOU WIN!!!")
            return
def is_float(s): 
    try: float(s); return True
    except: return False

play_blackjack()
