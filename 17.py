import intcodeComputerClass as intcodeComputer


def compress(path, offset=0, ignoreList=[]):
    path = list(path)
    letter = "ABC"[len(ignoreList)]

    # Find the chunk starting at 0 that you can repeat to get rid of the
    # largest possible number of characters
    pointer = 10  # Max length to put in a function
    maxRemovedCharacters = 0
    maxRemovedCharactersPointer = None
    maxRemovedCharactersIds = []
    maxRemovedCharactersChunk = None
    while pointer > 2:
        chunk = path[offset:offset+pointer]

        # Check if it's repeatable
        numRepeats = 0
        removedIds = []
        i = pointer + offset
        while i < len(path) - pointer + 1:
            skip = False
            for each in ignoreList:
                if each in path[i:i+pointer]:
                    skip = True
                    break
            if skip:
                i+=1
                continue

            if path[i:i+pointer] == chunk:
                numRepeats += 1
                removedIds.append(i)
                i += pointer
            else:
                i += 1

        if numRepeats * pointer > maxRemovedCharacters:
            maxRemovedCharacters = numRepeats * pointer
            maxRemovedCharactersPointer = pointer
            maxRemovedCharactersIds = removedIds
            maxRemovedCharactersChunk = chunk

        pointer -= 1

    # Perform replacement
    for i, _id in enumerate([offset] + maxRemovedCharactersIds):
        modifiedId = _id-(i*(maxRemovedCharactersPointer-1))
        path[modifiedId:modifiedId+maxRemovedCharactersPointer] = [letter]

    chunks = [maxRemovedCharactersChunk]

    if len(ignoreList) <= 1:
        for offset, x in enumerate(path):
            if x not in ignoreList + [letter]:
                break
        path, newChunks = compress(path, offset, ignoreList + [letter])
        chunks += newChunks

    return path, chunks

if __name__ == "__main__":
    with open("data/17_data", "r") as f:
        _input = f.read()

    code = list(map(int, _input.split(",")))

    ic = intcodeComputer.IntcodeComputer(list(code))

    chars = {10:"\n",35:"#",46:".",94:"^",60:"<",62:">",118:"v"}

    _map = [[]]
    mapStr = ""
    while not ic.finished:
        out = ic.step()

        if out is not None:
            mapStr += chars[out]

            if out == 10:
                _map.append([])
            else:
                _map[-1].append(chars[out])

    _map = _map[:-2]

    intersections = []
    for y in range(1,len(_map)-1):
        for x in range(1,len(_map[0])-1):
            if _map[y][x] == "#" and _map[y+1][x] == "#"\
                    and _map[y-1][x] == "#" and _map[y][x+1] == "#"\
                    and _map[y][x-1] == "#":
                intersections.append((x,y))

    alignmentSum = 0
    for intersection in intersections:
        alignmentSum += intersection[0] * intersection[1]

    print("Part 1:", alignmentSum)

    #print "\n".join(["".join(g) for g in _map])

    tiles = {}
    for y in range(len(_map)):
        for x in range(len(_map[0])):
            tiles[(x,y,)] = _map[y][x]
            if _map[y][x] == "^":
                pos = x,y

    width, height = len(_map[0]), len(_map)

    # Find way along scaffolding
    # Current strategy, just keep going along without taking any crossings
    _dir = [1,0]
    steps = ["R",0]
    while True:
        # Check if making a step will push us off the scaffold
        proposedPos = [pos[0] + _dir[0], pos[1] + _dir[1]]
        outOfRange = False
        if proposedPos[0] < 0 or proposedPos[0] >= width:
            outOfRange = True
        if proposedPos[1] < 0 or proposedPos[1] >= height:
            outOfRange = True
        if outOfRange or _map[proposedPos[1]][proposedPos[0]] == ".":
            # We need to change direction
            # Since this will never happen at a crossing we just find
            # the only direction
            x,y = pos
            possibleDirs = [[-_dir[1], _dir[0]], [_dir[1],-_dir[0]]]
            possibleTurns = ["R","L"]
            validNeighbour = False
            for pd, pt in zip(possibleDirs, possibleTurns):
                n = [pos[0]+pd[0], pos[1]+pd[1]]
                if n[0] < 0 or n[0] >= width or n[1] < 0 or n[1] >= height:
                    continue
                if _map[n[1]][n[0]] == "#":
                    _dir = [n[0]-x,n[1]-y]
                    steps += [pt,0]
                    validNeighbour = True
                    break

            if not validNeighbour:
                break

        # Take a step
        pos = [pos[0] + _dir[0], pos[1] + _dir[1]]
        _map[pos[1]][pos[0]] = "q"
        steps[-1] += 1

    mainRoutine, functions = compress(steps)

    print(mainRoutine)

    # Convert to string
    mainRoutine = ",".join(mainRoutine) + "\n"
    for i in range(3):
        functions[i] = ",".join([str(x) for x in functions[i]]) + "\n"

    asciiMap = {"A":65,"B":66,"C":67,"L":76,"R":82,"\n":10,",":44,"1":49,"2":50,"0":48,"8":56}

    # Convert to ascii
    mainRoutine = [asciiMap[x] for x in mainRoutine]

    for i in range(3):
        functions[i] = [asciiMap[x] for x in functions[i]]

    # Put through the intcode computer
    inputs = mainRoutine + functions[0] + functions[1] + functions[2]

    # Append an "n" to inputs to say no video feed
    inputs.append(110)
    inputs.append(10)

    def inputCallback():
        global inputs
        if not inputs:
            print "Ran out of inputs"

        return inputs.pop(0)

    outputs = []
    def outputCallback(out):
        global outputs
        outputs.append(out)

    newCode = list(code)
    newCode[0] = 2

    ic = intcodeComputer.IntcodeComputer(newCode)
    ic.setInputCallback(inputCallback)
    ic.setOutputCallback(outputCallback)

    ic.compute()

    print("Part 2: ", outputs[-1])
