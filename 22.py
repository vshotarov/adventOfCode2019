# Following the comments on reddit, it seems like the correct
# approach is to try to abstract the deck into just two numbers
# that fully describe it - offset and increment.
#
# each card is      offset + increment * n
#
# Each of the 4 operations just modify those numbers, where
# the deal with increment operation uses an inverse modulus
#
# Here's the reddit comment i followed
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/?context=3

class Deck:
    def __init__(self, n):
        self.n = n
        self.offset = 0
        self.increment = 1

    def card(self, n):
        return (self.offset + self.increment * n) % self.n

    def __repr__(self):
        return str([self.card(x) for x in range(10)])

def dealIntoNewStack(deck):
    # Just reverse
    deck.increment *= -1
    deck.offset += deck.increment
    deck.increment %= deck.n
    deck.offset %= deck.n

def cut(deck, n):
    deck.offset += n * deck.increment
    deck.offset %= deck.n

def dealWithIncrement(deck, n):
    deck.increment *= pow(n, deck.n-2, deck.n)
    deck.increment %= deck.n

def shuffle(deck, instructions):
    for instruction in instructions:
        splitInst = instruction.split(" ")
        
        if splitInst[1] == "into":
            dealIntoNewStack(deck)
        elif splitInst[1] == "with":
            dealWithIncrement(deck, int(splitInst[-1]))
        else:
            cut(deck, int(splitInst[-1]))

if __name__ == "__main__":
    with open("data/22_data", "r") as f:
        _input = f.read().splitlines()

    # Part 1
    deck = Deck(10007)

    shuffle(deck, _input)

    for i in range(10007):
        if deck.card(i) == 2019:
            print("Part 1: ", i)
            break

    # Part 2
    deck = Deck(119315717514047)
    iterations = 101741582076661

    # # Do instructions once
    shuffle(deck, _input)

    # # Using the logic of a geometric progression we can apply
    # # that same set of instructions a large number of times
    finalDeck = Deck(119315717514047)
    finalDeck.increment = pow(deck.increment, iterations, deck.n)
    finalDeck.offset = deck.offset * (1 - finalDeck.increment) *\
        pow((1 - deck.increment) % deck.n, deck.n - 2, deck.n)
    finalDeck.offset = finalDeck.offset % deck.n

    print("Part 2: ", finalDeck.card(2020))
