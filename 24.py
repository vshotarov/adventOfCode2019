LEN_FRAME = 30
MID_NEIGHBOURS = [8,13,15,20]
RECURSIVE_IN_NEIGHBOURS = [[24, 25, 26, 27, 28],
                        [0, 1, 2, 3, 4],
                        [4, 10, 16, 22, 28],
                        [0, 6, 12, 18, 24]]
RECURSIVE_OUT_NEIGHBOURS = [8, 20, 13, 15]
OUTER_TILES = [x for y in RECURSIVE_IN_NEIGHBOURS for x in y]


def emptyFrame():
    return list("\n".join(["."*5 for _ in range(5)])) + ["\n"]

def getNeighbours(thisElement, currentFrame, currentLevel=0, levels={}, recursive=False):
    above = thisElement-6
    below = thisElement+6
    left = thisElement-1
    right = thisElement+1

    _left = currentFrame[left] if left >= 0 else "."
    _right = currentFrame[right] if right < LEN_FRAME else "."

    if left > 0 and currentFrame[left] == "\n":
        _left = "."
    if right < LEN_FRAME and currentFrame[right] == "\n":
        _right = "."
    
    _above = currentFrame[above] if above >= 0 else "."
    _below = currentFrame[below] if below < LEN_FRAME else "."

    neighbours = [above, below, left, right]
    neighbourValues = [_above, _below, _left, _right]

    if recursive:
        lowerLevel = currentLevel + 1
        upperLevel = currentLevel - 1 
        if lowerLevel not in levels.keys():
            levels[lowerLevel] = emptyFrame()
        if upperLevel not in levels.keys():
            levels[upperLevel] = emptyFrame()

        toAppend = []
        for i in range(4):
            if neighbours[i] == 14:
                neighbourValues.remove(neighbourValues[i])
                neighbourValues += [levels[lowerLevel][x] for x in RECURSIVE_IN_NEIGHBOURS[i]]
                toAppend += [100+x for x in RECURSIVE_IN_NEIGHBOURS[i]]
        if toAppend:
            neighbours.remove(14)
            neighbours += toAppend

        if thisElement in RECURSIVE_IN_NEIGHBOURS[1]:
            neighbourValues[0] = levels[upperLevel][8]
            neighbours[0] = -108
        if thisElement in RECURSIVE_IN_NEIGHBOURS[0]:
            neighbourValues[1] = levels[upperLevel][20]
            neighbours[1] = -120
        if thisElement in RECURSIVE_IN_NEIGHBOURS[3]:
            neighbourValues[2] = levels[upperLevel][13]
            neighbours[2] = -113
        if thisElement in RECURSIVE_IN_NEIGHBOURS[2]:
            neighbourValues[3] = levels[upperLevel][15]
            neighbours[3] = -115

    return neighbours, neighbourValues

def part1(_input):
    frames = [list(_input)]
    currentFrame = frames[0]
    iters = 0
    while True:
        iters += 1
        currentFrame = frames[-1]
        nextFrame = list(currentFrame)

        #print("".join(currentFrame))

        for i, x in enumerate(currentFrame):
            if x == "\n":
                continue

            _, neighbours = getNeighbours(i, currentFrame, False)
            numBugNeighbours = neighbours.count("#")

            if currentFrame[i] == "#" and numBugNeighbours != 1:
                nextFrame[i] = "."

            if currentFrame[i] == "." and numBugNeighbours in [1,2]:
                nextFrame[i] = "#"

        if nextFrame in frames:
            frames.append(nextFrame)
            print("Repeated", iters)
            print("".join(nextFrame))
            break

        frames.append(nextFrame)

    # Calculate biodiversity
    biodiversity = 0
    power = 0
    for x in nextFrame:
        if x == "\n":
            continue

        biodiversity += 0 if x == "." else (2**(power))
        power += 1

    print("Biodiversity (Part 1):", biodiversity)

if __name__ == "__main__":
    with open("data/24_data", "r") as f:
        _input = f.read()
    _input = _input.replace("\r\n","\n")

    # Part 1
    part1(list(_input))

    # Part 2
    levels = {0:list(_input)}

    print("".join(levels[0]))
    levels[-1] = emptyFrame()
    levels[1] = emptyFrame()
    levels[-2] = emptyFrame()
    levels[2] = emptyFrame()
    lowBound = 0
    highBound = 0
    for i in range(200):
        depths, grids = list(levels.keys()), list(levels.values())
        nextFrames = {k:list(v) for k,v in levels.items()}
        lowBound -= 1
        highBound += 1
        for depth, grid in zip(depths, grids):
            if depth < lowBound or depth > highBound:
                continue

            for j, x in enumerate(grid):
                # Get neighbours
                if x == "\n" or j == 14:
                    continue

                _, neighbours = getNeighbours(j, grid, depth, levels, True)

                numBugNeighbours = neighbours.count("#")

                if grid[j] == "#" and numBugNeighbours != 1:
                    nextFrames[depth][j] = "."
                elif grid[j] == "." and numBugNeighbours in [1,2]:
                    nextFrames[depth][j] = "#"

        for k,v in nextFrames.items():
            levels[k] = list(v)

    # Count bugs after 200 minutes
    bugs = 0
    for k,v in levels.items():
        bugs += v.count("#")

    print("Bugs after 200 minutes (recursive):", bugs)
