# Initially i wrote a very stupid but obvious solver, which
# iterates over the range and checks whether a password is valid
#
# I've left it in here for posterity, but really, Matt's solution
# at the bottom (getAllValidPasswords(min, max)) is much better

def isPasswordValidA(password):
    prev = None
    hasDuplicates = False

    for strDigit in str(password):
        digit = int(strDigit)

        if prev:
            if digit < prev:
                return False

            if digit == prev and not hasDuplicates:
                hasDuplicates = True

        prev = digit

    if not hasDuplicates:
        return False

    return True

def isPasswordValidB(password):
    prev = None
    members = {}

    for strDigit in str(password):
        digit = int(strDigit)

        if prev:
            if digit < prev:
                return False

        if digit not in members.keys():
            members[digit] = 0
        members[digit] += 1

        prev = digit

    return 2 in members.values()

def combine(digits):
    return sum([x*(10**(len(digits)-1-i)) for i,x in enumerate(digits)])

def getAllValidPasswords(_min, _max):
    bottomBound = _min / 10**5

    valid1 = 0
    valid2 = 0

    for a in range(bottomBound, 10):
        for b in range(a, 10):
            for c in range(b, 10):
                for d in range(c, 10):
                    for e in range(d, 10):
                        for f in range(e, 10):
                            asList = [a,b,c,d,e,f]
                            combined = combine(asList)

                            if combined < _max and combined > _min:
                                if len(set(asList)) < 6:
                                    valid1 += 1
                                    
                                    counts = [asList.count(x) for x in asList]

                                    if 2 in counts:
                                        valid2 += 1
    return valid1, valid2

if __name__ == "__main__":
    _input = "147981-691423"
    inputRange = [int(each) for each in _input.split("-")]

    password = inputRange[1]

    numValidPasswordPart1 = 0
    numValidPasswordPart2 = 0
    while password > inputRange[0]:
        numValidPasswordPart2 += int(isPasswordValidB(password))
        numValidPasswordPart1 += int(isPasswordValidA(password))

        password -= 1

    import time
    start = time.time()
    print "Inefficient looping through each number in range, which was my initial solution"
    print "Part 1:", numValidPasswordPart1, "(%.3f s)" % (time.time() - start)
    start = time.time()
    print "Part 2:", numValidPasswordPart2, "(%.3f s)" % (time.time() - start)

    print "Matt Jenkins' much nicer solution for generating the numbers"
    start = time.time()
    print "Part 1: %i, Part 2: %i (%.3f s)" % (getAllValidPasswords(*inputRange) +\
            (time.time() - start, ))

