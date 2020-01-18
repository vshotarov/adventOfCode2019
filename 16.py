VERBOSE = 0

def part1(_input):
    if VERBOSE:
        print "-------------- Part 1 start"
    pattern = [0,1,0,-1]

    for i in range(100):
        if VERBOSE:
            print "iter", i, _input
        newInput = []

        for j, x in enumerate(_input):
            if VERBOSE:
                print "    generating repeating pattern at j", j
            # Generate repeating pattern
            currentPattern = [x for patterns in zip(*([pattern]*(j+1)))\
                    for x in patterns]
            lenCurrentPattern = len(currentPattern)

            newInput.append(0)
            if VERBOSE:
                print "    ",
            for k, element in enumerate(_input):
                if VERBOSE:
                    print "%i * %i + " % (element, currentPattern[(k+1)%lenCurrentPattern]),
                newInput[-1] += element * currentPattern[(k+1) % lenCurrentPattern]
            if VERBOSE:
                print "= ", newInput[-1]

            # Take rightmost digit
            a = newInput[-1]
            newInput[-1] = abs(newInput[-1]) % 10 if abs(newInput[-1]) >= 10 else abs(newInput[-1])
            if VERBOSE:
                print "    taking rightmost of", a, "which is", newInput[-1]

        _input = newInput

    return "".join([str(each) for each in _input[:8]])

def part2(_input):
    firstSevenDigits = _input[:7]
    offset = sum([x*(10**i) for i,x in enumerate(firstSevenDigits[::-1])])
    size = len(_input) * 10000 - offset

    sliced = []
    for i in range(size):
        sliced.append(_input[(offset+i) % len(_input)])

    for i in range(100):
        thisSum = 0
        for k in reversed(range(size)):
            thisSum += sliced[k]
            sliced[k] = abs(thisSum) % 10

    return "".join([str(each) for each in sliced[:8]])

if __name__ == "__main__":
    with open("data/16_data", "r") as f:
        _input = f.read()

    _input = [int(x) for x in _input.splitlines()[0]]

    print "Part 1:", part1(list(_input))
    print "Part 2:", part2(list(_input))
