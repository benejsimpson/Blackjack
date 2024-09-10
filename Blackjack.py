values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank}'

    def ace_value(self, value):
        """
        sets value of ace to specified value
        """
        self.value = value


class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def __str__(self):
        return 'Deck: ' + ('/' * len(self.all_cards))

    def shuffle_cards(self):
        import random
        print('shuffling cards...')
        random.shuffle(self.all_cards)

    def deal_one(self, print_turn=True):
        card = self.all_cards.pop()
        if print_turn:
            print(f'Dealer turns over a {str(card)}')
        return card


class Player:

    def __init__(self, name, balance, is_dealer=False):
        self.options = None
        self.name = name
        self.balance = balance
        self.is_dealer = is_dealer
        self.card_list = []
        self.split_hands = None

    def __str__(self):
        return f'Name: {self.name}\nBalance: £{self.balance}'

    def add_balance(self, num):
        self.balance += num

    def reduce_balance(self, num):
        self.balance -= num

    def get_bet(self):
        """
        returns player bet for hand
        """
        while True:
            try:
                player_bet = int(input(f'Current Balance: {self.balance}\n\nHow much would you like to bet: £'))

            except TypeError:
                print('Please enter a whole number')

            else:
                if player_bet > self.balance:
                    print('INSUFFICIENT FUNDS!')
                    continue

                else:
                    self.balance -= player_bet
                    return player_bet

    def card_add(self, card):
        return self.card_list.append(card)

    def print_cards(self, all_cards=True):
        """
        prints all hands for player and dealer. enter (False) to only show top card
        """
        if self.is_dealer:
            if not all_cards:
                print(f'Dealer cards: {str(self.card_list[0])}, ?')
            else:
                print(f'Dealer cards: {[str(card) for card in self.card_list]} = {self.card_sum()}')
        elif type(self.card_list[0]) == type([]):
            print('Your hands:')
            for i in range(len(self.card_list)):
                print(
                    f'Hand {i + 1}:'
                    f'{[str(card) for card in self.card_list[i]]} = {sum([card.value for card in self.card_list[i]])}')
        else:
            print(f'Your cards: {[str(card) for card in self.card_list]} = {self.card_sum()}')

    def choice_options(self):
        """
        available options for split/stand/double/hit returned
        """
        self.options = []
        if self.card_list[0].value == self.card_list[1].value:
            self.options.append('SPLIT')
        if sum([card.value for card in self.card_list]) < 21:
            self.options.extend(['HIT', 'STAND', 'DOUBLE'])
        if sum([card.value for card in self.card_list]) == 21:
            self.options = ['STAND']

    def check_bust(self):
        """
        returns true if player is bust
        """
        if self.card_sum() <= 21:
            return False
        else:
            return True

    def check_blackjack(self):
        return self.card_sum() == 21 and len(self.card_list) == 2

    def player_choice(self):
        """
        player chooses from options and valid choice returned. auto-stand on 21
        """
        self.choice_options()
        if len(self.options) == 4:
            while True:
                player_choice = input('Please enter Hit / Stand / Double / Split: ').upper()
                if player_choice in ['HIT', 'STAND', 'DOUBLE', 'SPLIT']:
                    return player_choice
        elif 'HIT' not in self.options and self.card_sum() == 21:
            print('Standing on 21!')
            return 'STAND'
        elif 'SPLIT' not in self.options:
            while True:
                player_choice = input('Please enter Hit / Stand / Double: ').upper()
                if player_choice in ['HIT', 'STAND', 'DOUBLE']:
                    return player_choice

    def split_hand(self):
        """
        returns hand split into 2 hands [[hand1],[hand2]]
        """
        self.split_hands = True
        print(f'Split {str(self.card_list[0])}s')
        self.card_list = [[self.card_list[0]], [self.card_list[1]]]

    def card_sum(self):
        if sum([card.value for card in self.card_list]) > 21:
            for i in range(len(self.card_list)):
                if self.card_list[i].rank == 'A':
                    self.card_list[i].ace_value(1)
        return sum([card.value for card in self.card_list])

    def clear_cards(self):
        self.card_list = []


def get_player_balance():
    """
    returns players input(deposit to balance)
    """
    while True:
        try:
            balance = int(input('Deposit to your balance: £'))
        except TypeError:
            print('ERROR: You can only add whole numbers to your balance.')
            continue
        else:
            print(f'Deposited: £{balance}')
            return balance


def replay():
    """
    returns True to play again
    """
    return input('Press Enter to play again or type anything and Enter to quit!') == ''


# SETUP GAME

player = Player(input('Enter your name: '), get_player_balance())
dealer = Player('Dealer', 0, True)
deck = Deck()
print()
deck.shuffle_cards()
print()

# GAME LOGIC

game_on = True
while game_on:
    print(deck)
    bet = player.get_bet()

    print(('\n' * 2) + 'Dealing cards...\n')
    player.card_add(deck.deal_one(False))
    dealer.card_add(deck.deal_one(False))
    player.card_add(deck.deal_one(False))
    dealer.card_add(deck.deal_one(False))

    player.print_cards()
    dealer.print_cards(False)

    if player.check_blackjack():
        print('\n------- BLACKJACK! -------\n')
        player.add_balance(bet * 2.5)
        print(f'You won: £{bet * 2.5}')
        continue

    while True:

        if player.check_bust():
            print('--- BUST! ---\n')
            break
        print('\n' * 2)
        choice = player.player_choice()

        if choice == 'HIT':
            player.card_add(deck.deal_one())
            player.print_cards()
            print()
            continue

        elif choice == 'STAND':
            print(f'Standing on {player.card_sum()}\n')
            break

        elif choice == 'DOUBLE':
            player.reduce_balance(bet)
            bet *= 2
            new_card = deck.deal_one()
            player.card_add(new_card)
            player.print_cards()

            if player.balance < 0:
                print(f'\n\nINSUFFICIENT FUNDS!\nDEBT: £{player.balance * -1}\n\n')
            continue

        elif choice == 'SPLIT':
            player.split_hand()
            continue

    dealer.print_cards()

    if dealer.check_blackjack():
        print('\n------- BLACKJACK! -------\n')
        print(f'You lost £{bet}')

    if not player.check_bust() and not player.check_blackjack():

        while dealer.card_sum() < 17:
            print()
            print(f'Dealer hits on {dealer.card_sum()}!')
            dealer.card_add(deck.deal_one())
            dealer.print_cards()

        print()
        if dealer.check_bust():
            print(f'Dealer busts on {dealer.card_sum()}')
            print(f'You win £{bet}')
            player.add_balance(bet * 2)

        elif dealer.card_sum() > player.card_sum():
            print(f'Dealer wins with {dealer.card_sum()} compared to your {player.card_sum()}')

        elif dealer.card_sum() == player.card_sum():
            print(f'Push on {dealer.card_sum()}!')

        else:
            print('--- CONGRATULATIONS! ---')
            print(f'You win with {player.card_sum()} compared to dealer {dealer.card_sum()}')
            player.add_balance(bet * 2)

    if not replay():
        print('\nThank you for playing!')
        print(f'\nYour final balance is: £{player.balance}')
        break
    else:
        player.clear_cards()
        dealer.clear_cards()
        print('\n'*100)
