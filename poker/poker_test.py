import poker

pocket_hand = [Card('S', 2), Card('H', 5)]
suits = ['H', 'C', 'S', 'D']

given_reg_hand = [Card('H', 7), Card('S', 2), Card('D', 9), Card('C', 11), Card('S', 4), Card('D', 13), Card('H', 1)]
reg_hand = Hand(deck, given_reg_hand)

def genFlushHand():
    suit = random.choice(suits)
    given_flush_hand = [Card(suit, random.randint(1, 13)) for i in range(5)] + pocket_hand
    random.shuffle(given_flush_hand)
    flush_hand = Hand(deck, given_flush_hand)
    return flush_hand

def genStraightHand():
    start = random.randint(1, 10)
    given_straight_hand = [Card(random.choice(suits), r) for r in range(start, start+5)] + pocket_hand
    random.shuffle(given_straight_hand)
    straight_hand = Hand(deck, given_straight_hand)
    return straight_hand

def genStraightFlushHand():
    start = random.randint(1, 10)
    suit = random.choice(suits)
    given_straight_flush_hand = [Card(suit, r) for r in range(start, start+5)] + pocket_hand
    random.shuffle(given_straight_flush_hand)
    straight_flush_hand = Hand(deck, given_straight_flush_hand)
    return straight_flush_hand

def genRoyalFlushHand():
    start = 10
    suit = random.choice(suits)
    given_royal_flush_hand = [Card(suit, r) for r in range(start, start+5)] + pocket_hand
    random.shuffle(given_royal_flush_hand)
    royal_flush_hand = Hand(deck, given_royal_flush_hand)
    return royal_flush_hand

def genNOfAKindHand(n):
    rank = random.randint(1, 13)
    given_n_of_a_kind_hand = [Card(random.choice(suits), rank) for c in range(n)] + pocket_hand + [Card(random.choice(suits), random.randint(1, 13))]
    random.shuffle(given_n_of_a_kind_hand)
    n_of_a_kind_hand = Hand(deck, given_n_of_a_kind_hand)
    return n_of_a_kind_hand

def genNExtraHand(n):
    rank1, rank2 = random.randint(1, 13), random.randint(1, 13)
    given_n_extra_hand = [Card(random.choice(suits), rank1) for c in range(n)] + [Card(random.choice(suits), rank2) for c in range(2)] + pocket_hand
    random.shuffle(given_n_extra_hand)
    n_extra_hand = Hand(deck, given_n_extra_hand)
    return n_extra_hand

stop_ind = len(reg_hand.getPotentHands()) - 1
print()
print("regular hand:", reg_hand)
print("regular hand status?", reg_hand.evalHand(stop_ind))
print()

special_hand = genNExtraHand(2)
print("special hand:", special_hand)
print("special hand status?", special_hand.evalHand(stop_ind))
print()


#original isStraight code
def isStraight(self):
    straight, high_card = False, 0
    hand = self.sortHand(type="r")
    print([str(card) for card in hand])
    #if there's an ace, account for possibility of ace high
    try:
        if hand[-1].rank == 1:
            hand.insert(0, Card(hand[-1].suit, 14))
        previous = hand[0].rank
        print("original start:", previous)
    except IndexError:
        return straight, high_card
    final_needed = previous - 4
    print("final needed:", final_needed)
    for c in range(1, len(hand)):
        new = hand[c].rank
        if new == previous - 1:
            print("previous:", previous)
            print("new:", new)
            if new == final_needed:
                straight, high_card = True, final_needed + 4
                return straight, high_card
            elif new > final_needed:
                previous = new
                print("new previous:", previous)
        elif new < previous - 1:
            if new < 5:
                return straight, high_card
            else:
                previous = new
                print("new startover:", previous)
                final_needed = previous - 4
                print("new final needed:", final_needed)
    return straight, high_card
