import random

class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.face_cards = ["J", "Q", "K"]
    def getSuit():
        return self.suit
    def getRank():
        return self.rank
    def __str__(self):
        if self.rank == 1 or self.rank == 14:
            rank = "A"
        elif 2 <= self.rank <= 10:
            rank = str(self.rank)
        elif self.rank >= 11:
            rank = self.face_cards[self.rank - 11]
        return rank + self.suit

class Deck(object):
    def __init__(self):
        self.og_deck = []
        self.suits = ["S", "H", "D", "C"]
        self.ranks = [n for n in range(1, 14)]
        for suit in self.suits:
            for rank in self.ranks:
                card = Card(suit, rank)
                self.og_deck.append(card)
        self.deck = self.og_deck.copy()
        self.shuffleDeck()
    def getSuits(self):
        return self.suits
    def getRanks(self):
        return self.ranks
    def shuffleDeck(self):
        random.shuffle(self.deck)
    def dealCard(self):
        dealt_card = self.deck.pop(0)
        return dealt_card
    def burnCard(self):
        self.deck.append(self.deck.pop(0))
    def reacceptCards(self, pocket_hand):
        hand = pocket_hand.getHand()
        for card in hand:
            self.deck.append(card)
    def resetDeck(self):
        self.deck = self.og_deck.copy()
        self.shuffleDeck()
    def __str__(self):
        return str([str(card) for card in self.deck])

class Hand(object):
    def __init__(self, deck, given_hand=None):
        if given_hand == None:
            given_hand = []
        self.hand = given_hand
        self.deck = deck
        self.potent_hands = ["isRoyalFlush", "isStraightFlush", "isFourOfAKind",
        "isFullHouse", "isFlush", "isStraight", "isThreeOfAKind", "isTwoPair",
        "isPair", "isHighCard"]
    def getHand(self):
        return self.hand
    def getPotentHands(self):
        return self.potent_hands
    def addCards(self, dealt_cards):
        for dealt_card in dealt_cards:
            self.hand.append(dealt_card)
    def dealCards(self, round):
        dealt_cards = [self.deck.dealCard() for c in range(round)]
        self.addCards(dealt_cards)
    def sortHand(self, type):
        #type refers to rank or suit
        hand = self.hand.copy()
        if type == "r":
            hand.sort(key=lambda card: card.rank, reverse=True)
        elif type == "s":
            hand.sort(key=lambda card: card.suit)
        return hand

    def separateSuits(self):
        hand = self.sortHand(type="s")
        suits = self.deck.getSuits()
        suits.sort()
        suits_list, c = [], 0
        for suit in suits:
            if c < len(hand):
                start = c
                while hand[c].suit == suit:
                    c += 1
                    if c >= len(hand):
                        break
                suit_list_hand = Hand(self.deck, hand[start:c])
                suit_list = suit_list_hand.sortHand(type="r")
                suits_list.append(suit_list)
        return suits_list

    def isFlush(self):
        flush, flush_hand = False, Hand(self.deck)
        #create a dummy 0 rank card
        high_card = 0
        #get ranked card lists for each suit
        suits_list = self.separateSuits()
        for suit_list in suits_list:
            if len(suit_list) >= 5:
                flush = True
                flush_hand.hand = suit_list
                high_card = flush_hand.hand[0].rank
                if high_card == 1:
                    high_card = 14 #ace high
                break
        return flush, [high_card, flush_hand]

    def isStraight(self):
        straight, high_card = False, 0
        hand = self.sortHand(type="r")
        #if there's an ace, account for possibility of ace high
        try:
            if hand[-1].rank == 1:
                hand.insert(0, Card(hand[-1].suit, 14))
            previous = hand[0].rank
        except IndexError:
            return straight, high_card
        final_needed = previous - 4
        for c in range(1, len(hand)):
            new = hand[c].rank
            if new == previous - 1:
                if new == final_needed:
                    straight, high_card = True, final_needed + 4
                    return straight, high_card
                elif new > final_needed:
                    previous = new
            elif new < previous - 1:
                if new < 5:
                    return straight, high_card
                else:
                    previous = new
                    final_needed = previous - 4
        return straight, high_card

    def isStraightFlush(self, given_flush_hand=None):
        straight_flush, high_card = False, 0
        if given_flush_hand == None:
            flush, flush_specs = self.isFlush()
            flush_hand = flush_specs[1]
        else:
            #if a flush hand is already passed up from a lower level check
            flush, flush_hand = True, given_flush_hand
        if flush:
            straight, high_card = flush_hand.isStraight()
            if straight:
                straight_flush = True
        return straight_flush, high_card

    def isRoyalFlush(self, given_high_card=None):
        royal_flush, high_card = False, 0
        if given_high_card == None:
            straight_flush, temp_high_card = self.isStraightFlush()
        else:
            straight_flush, temp_high_card = True, given_high_card
        if straight_flush and temp_high_card == 14:
            royal_flush, high_card = True, temp_high_card
        return royal_flush, high_card

    def rerankAces(self, hand):
        reranked_hand = hand.copy()
        while reranked_hand[-1].rank == 1:
            card = reranked_hand.pop(-1)
            reranked_hand.insert(0, Card(card.suit, 14))
        return reranked_hand

    def isNOfAKind(self, n):
        n_of_a_kind, rank = False, 0
        hand = self.sortHand(type="r")
        try:
            hand = self.rerankAces(hand)
            current_rank, rank_counter = hand[0].rank, 1
        except IndexError:
            return n_of_a_kind, rank
        for c in range(1, len(hand)):
            if hand[c].rank == current_rank:
                rank_counter += 1
                if rank_counter >= n:
                    n_of_a_kind, rank = True, current_rank
                    return n_of_a_kind, rank
            else:
                current_rank, rank_counter = hand[c].rank, 1
        return n_of_a_kind, rank

    def isFourOfAKind(self):
        return self.isNOfAKind(4)

    def isThreeOfAKind(self):
        return self.isNOfAKind(3)

    def isPair(self):
        return self.isNOfAKind(2)

    def isExtraPair(self, n, given_rank):
        '''
        given qualifying n (three of a kind (3) or pair (2)), check if there is an extra pair
        '''
        hand = self.sortHand(type="r")
        hand = self.rerankAces(hand)
        c = 0
        while hand[c].rank != given_rank:
            c += 1
        #remove already qualifying cards and retest new_hand to see if there is another pair
        new_hand = Hand(self.deck, hand[:c] + hand[c+n:])
        return new_hand.isPair()

    def isNExtra(self, n):
        #if there's an n_hand, what the n_rank is, and what the pair_rank is
        n_hand, n_rank, pair_rank = False, 0, 0
        n_of_a_kind, given_rank = self.isNOfAKind(n)
        if n_of_a_kind:
            pair, rank = self.isExtraPair(n, given_rank)
            if pair:
                n_hand, n_rank, pair_rank = True, given_rank, rank
        return n_hand, [n_rank, pair_rank]

    def isFullHouse(self):
        return self.isNExtra(3)

    def isTwoPair(self):
        return self.isNExtra(2)

    def isHighCard(self):
        hand = self.sortHand(type="r")
        hand = self.rerankAces(hand)
        try:
            return True, hand[0].rank
        except IndexError:
            return True, 0

    def evalHand(self, stop_ind=9):
        #stop_ind is the index previously stopped on
        high_card = 0 #in case of error in assignment within an if statement
        for i in range(stop_ind + 1):
            potent_hand = self.potent_hands[i]
            potent_hand_status, high_card = getattr(self, potent_hand)()
            if i == 4:
                #isFlush() returns list including high_card & hand, just use the first part
                high_card = high_card[0]
            if potent_hand_status:
                #change stop_ind for future hands and stop evaluating
                stop_ind = i
                break
        return stop_ind, high_card

    def __add__(self, other_hand):
        total_hand = self.hand + other_hand.hand
        return Hand(self.deck, total_hand)
    def __str__(self):
        return str([str(card) for card in self.hand])

class PocketHand(Hand):
    pass

class CommunalHand(Hand):
    pass

class Pot(object):
    def __init__(self, pot=None):
        if pot == None:
            pot = 0
        self.pot = pot
    def getPot(self):
        return self.pot
    def setPot(self, new_pot):
        self.pot = new_pot
    def addToPot(self, bet):
        self.pot += bet
    def awardPot(self, winners):
        pot = self.getPot()
        pot_cut = round( (pot / len(winners)) / 5 ) * 5
        rem = pot - (len(winners) * pot_cut)
        for player in winners[:-1]:
            player.awardChips(pot_cut)
        winners[-1].awardChips(pot_cut + rem)
        self.setPot(0)
    def __str__(self):
        return str(self.pot)

class Player(object):
    def __init__(self, id, chips, deck, pot):
        self.id = id
        self.chips = chips
        self.deck = deck
        self.pot = pot
        self.hand = PocketHand(deck)
        self.total_hand = self.hand
        self.round_bet = 0
    def getId(self):
        return self.id
    def getHand(self):
        return self.hand
    def getTotalHand(self):
        return self.total_hand
    def getChips(self):
        return self.chips
    def dealHand(self, round):
        self.hand.dealCards(round)
    def resetHand(self):
        self.hand = PocketHand(self.deck)
    def bet(self, bet):
        self.chips -= bet
        self.round_bet += bet
    def check(self):
        self.bet(0)
    def call(self, highest_bet):
        call_amt = highest_bet - self.round_bet
        self.bet(call_amt)
    def fold(self):
        self.deck.reacceptCards(self.hand)
        self.resetHand()
    def getRoundBet(self):
        return self.round_bet
    def addRoundBetToPot(self):
        self.pot.addToPot(self.round_bet)
        self.round_bet = 0

    def askBet(self, highest_bet):
        raise_bet, fold = False, False
        if self.chips == 0:
            self.check()
            return raise_bet, fold
        bet_str = input("How much you like to bet, " + self.id + "? ")
        if bet_str == "f":
            fold = True
            return raise_bet, fold
        if bet_str == "k":
            bet_str = 0
        if bet_str == "c":
            bet_str = highest_bet - self.round_bet
        if bet_str == "a":
            if self.round_bet + self.chips <= highest_bet:
                self.bet(self.chips)
                return raise_bet, fold
            else:
                bet_str = self.chips
        try:
            bet = int(bet_str)
            total_bet = self.round_bet + bet
            if bet % 5 != 0:
                print("you must bet at least one whole chip (5 points)")
                raise_bet, fold = self.askBet(highest_bet)
            elif bet > self.chips:
                print("you can't bet more chips than you have")
                raise_bet, fold = self.askBet(highest_bet)
            elif total_bet < highest_bet:
                #if you are all in
                if bet == self.chips:
                    self.bet(self.chips)
                    return raise_bet, fold
                else:
                    print("you need to at least match the highest bet")
                    raise_bet, fold = self.askBet(highest_bet)
            elif total_bet == highest_bet:
                self.bet(bet)
            elif total_bet > highest_bet:
                self.bet(bet)
                raise_bet = True
            return raise_bet, fold
        except ValueError:
            print("please enter a number, 'c' (call), 'k' (check), or 'f' (fold)")
            return self.askBet(highest_bet)

    def updateTotalHand(self, communal_hand):
        self.total_hand = self.hand + communal_hand
    def sortPlayerHand(self, type):
        #type refers to rank or suit
        self.total_hand = self.total_hand.sortHand(type)
    def awardChips(self, chips):
        self.chips += chips
    def evalHand(self, stop_ind=9):
        total_hand = self.getTotalHand()
        return total_hand.evalHand(stop_ind)
    def __eq__(self, other_player):
        return self.id == other_player.id
    def __str__(self):
        return str([("id:", self.id), ("chips:", self.chips),
        ("pocket hand:", str(self.hand)), ("total hand:", str(self.total_hand))])

class Group(object):
    def __init__(self, group, deck, rounds, blinds, pot):
        self.group = group
        self.deck = deck
        self.rounds = rounds
        self.blinds = blinds
        self.pot = pot
        self.highest_bet = 0
        self.auto_check = False
        self.match_group = self.group.copy()
        self.communal_hand = CommunalHand(self.deck)
        self.winner = None
    def getPlayersList(self):
        return self.group
    def getAutoCheck(self):
        return self.auto_check
    def getPot(self):
        return self.pot
    def setAutoCheck(self, auto_check):
        self.auto_check = auto_check
    def setMatchGroup(self, new_group):
        self.match_group = new_group
    def setGroup(self, new_group):
        self.group = new_group
    def dealPocketHands(self):
        pre_flop = self.rounds[0]
        for player in self.group:
            player.dealHand(pre_flop)
    def dealCommunalHand(self, round):
        self.deck.burnCard()
        self.communal_hand.dealCards(round)
        for player in self.group:
            player.updateTotalHand(self.communal_hand)
    def collectBets(self):
        for player in self.group:
            player.addRoundBetToPot()
    def awardPot(self, winners):
        pot = self.getPot()
        pot.awardPot(winners)

    def askBetsHelper(self, group_round, start=0):
        final_player = group_round[-1]
        for player in group_round[start:]:
            #if the player is last and there has been a raise, he was the one
            #who raised last round, so he should auto_check now
            if self.getAutoCheck() and player == final_player:
                player.check()
            else:
                raise_bet, fold = player.askBet(self.highest_bet)
                if fold:
                    player.fold()
                    round_ind, match_ind = group_round.index(player), self.match_group.index(player)
                    group_round.pop(round_ind)
                    self.match_group.pop(match_ind)
                    if len(self.match_group) > 1:
                        #more than one person left in the match
                        self.askBetsHelper(group_round, round_ind)
                    break
                elif raise_bet:
                    #last player (the one who just raised) will auto_check at the end
                    self.setAutoCheck(True)
                    highest_bet = player.getRoundBet()
                    self.setHighestBet(highest_bet)
                    group_round = self.reorganizeSeats(group_round, player)
                    self.askBetsHelper(group_round)
                    break
        self.setAutoCheck(False)

    def askBets(self):
        group_round = self.match_group.copy()
        self.askBetsHelper(group_round)
        self.collectBets()
        self.resetHighestBet()

    def playRound(self, round):
        og_match_starter = self.match_group[0]
        print()
        print("round:", round)
        print("og deck:", self.deck)
        print()
        if round == 2:
            self.dealPocketHands()
        else:
            self.dealCommunalHand(round)
        for player in self.match_group:
            print(player)
            print()
        print("communal hand:", self.communal_hand)
        print()
        self.askBets()
        print("current pot:", self.pot)
        print()
        print("new deck:", self.deck)
        print()
        self.changeStarter(self.match_group, og_match_starter)

    def playMatch(self):
        og_group_starter = self.group[0]
        self.betBlinds()
        for round in self.rounds:
            self.playRound(round)
            if len(self.match_group) == 1:
                break
        self.evalHands()
        for player in self.group:
            print(player)
            print()
        self.resetCommunalHand()
        self.changeStarter(self.group, og_group_starter)
        self.removeBrokePlayers()
        self.setMatchGroup(self.group)

    def removeBrokePlayers(self):
        new_group = []
        for player in self.group:
            if player.getChips() > 0:
                new_group.append(player)
        self.setGroup(new_group)

    def betBlinds(self):
        small_blind_player, big_blind_player = self.match_group[-2], self.match_group[-1]
        small_blind_player.bet(small_blind)
        big_blind_player.bet(big_blind)
        self.highest_bet = big_blind
    def setHighestBet(self, highest_bet):
        self.highest_bet = highest_bet
    def resetHighestBet(self):
        self.setHighestBet(0)
    def changeStarter(self, group, og_starter):
        '''change the starter for the round'''
        #if the og_starter is still in, shift to the right
        if group[0] == og_starter:
            group.append(group.pop(0))
        #else, self.match_group is auto-shifted because the og_starter is gone
    def resetCommunalHand(self):
        self.communal_hand = CommunalHand(self.deck)
    def reorganizeSeats(self, group_round, player):
        try:
            start_seat = group_round.index(player) + 1
            new_group_round = group_round[start_seat:] + group_round[:start_seat]
        except IndexError:
            new_group_round = group_round
        return new_group_round

    def narrowTie(self, win_hands, extra_pair=False, p=2, s=0):
        #extra_pair = True if evaluating full house or two pair
        #p is primary hand index, s is secondary pair index if there is an extra pair
        w = 0
        if extra_pair:
            win_hands.sort(key=lambda win_hand: win_hand[p][s])
            best_rank = win_hands[0][p][s]
            while win_hands[w][p][s] == best_rank:
                w += 1
                if w >= len(win_hands):
                    break
        elif not extra_pair:
            win_hands.sort(key=lambda win_hand: win_hand[p])
            best_rank = win_hands[0][p]
            while win_hands[w][p] == best_rank:
                w += 1
                if w >= len(win_hands):
                    break
        win_hands = win_hands[:w]
        return win_hands

    def decideWinner(self, win_hands, stop_ind):
        if stop_ind == 3 or stop_ind == 7:
            for s in range(2):
                win_hands = self.narrowTie(win_hands, True, 2, s)
        else:
            win_hands = self.narrowTie(win_hands, extra_pair=False, p=2, s=0)
        #return a list of the winning players
        winners = [win_hand[0] for win_hand in win_hands]
        return winners

    def evalHands(self):
        win_hands, stop_ind = [], 9
        for player in self.match_group:
            player_stop_ind, high_card = player.evalHand(stop_ind)
            if high_card != 0 and high_card != [0,0]:
                if player_stop_ind < stop_ind:
                    win_hands = [[player, player_stop_ind, high_card]]
                    stop_ind = player_stop_ind
                elif player_stop_ind == stop_ind:
                    win_hands.append([player, player_stop_ind, high_card])
        winners = self.decideWinner(win_hands, stop_ind)
        self.awardPot(winners)

    def playGame(self):
        while len(self.group) > 1:
            self.playMatch()
        self.winner = self.group[0]
        print(self.winner.getId(), "is the winner of the game!")

    def __str__(self):
        return str([str(player) for player in self.group])


def startGame(chips, rounds, deck, players_list, blinds, pot):
    group_list = []
    for id in players_list:
        player = Player(id, chips, deck, pot)
        group_list.append(player)
    group = Group(group_list, deck, rounds, blinds, pot)
    return group


rounds = [pre_flop, flop, river, turn] = [2, 3, 1, 1]
deck = Deck()
chips = 1000
players_list = ["kishan", "nikhil", "ron", "james"]
blinds = [small_blind, big_blind] = [5, 10]
pot = Pot()

group = startGame(chips, rounds, deck, players_list, blinds, pot)

group.playGame()
