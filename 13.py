import intcodeComputerClass as intcodeComputer


def drawScreen(tiles, maxX, maxY):
    _map = []
    symbols = [" ", "|", "#", "_", "o"]
    for y in range(maxY):
        _map.append([])
        for x in range(maxX):
            _map[-1].append(symbols[tiles[(x,y)]])

    print "\n".join(["".join(x) for x in _map])

if __name__ == "__main__":
    with open("data/13_data", "r") as f:
        _input = f.read()

    code = list(map(int, _input.split(",")))
    ic = intcodeComputer.IntcodeComputer(code)

    ## Part 1
    maxX, maxY = 0, 0
    tiles = {}
    outputBuffer = []
    iters = 0
    while not ic.finished:
        out = ic.step()

        if out == None:
            continue

        outputBuffer.append(out)

        if len(outputBuffer) == 3:
            tiles[(outputBuffer[0], outputBuffer[1])] = outputBuffer[2]
            
            if outputBuffer[0] > maxX:
                maxX = outputBuffer[0]
            if outputBuffer[1] > maxY:
                maxY = outputBuffer[1]

            outputBuffer = []

        iters += 1

    drawScreen(tiles,maxX,maxY)

    print("Num block tiles (Part 1):", len([v for v in tiles.values() if v == 2]))

    ## Part 2
    code = list(map(int, _input.split(",")))
    ic = intcodeComputer.IntcodeComputer(code)

    ic.code[0] = 2
    tiles = {}
    paddlePos, ballPos = None, None
    frames = 0

    scores = []
    def inputCallback():
        global frames, tiles
        #drawScreen(tiles, 37, 20)

        scores.append(tiles[(-1,0)])

        frames += 1

        diffX = ballPos[0] - paddlePos[0]

        if diffX:
            return diffX / abs(diffX)

        return 0

    ic.setInputCallback(inputCallback)

    outputBuffer = []
    iters = 0
    while not ic.finished:
        out = ic.step()

        if out == None:
            continue

        outputBuffer.append(out)

        if len(outputBuffer) == 3:
            tiles[(outputBuffer[0], outputBuffer[1])] = outputBuffer[2]

            if outputBuffer[2] == 4:
                ballPos = [outputBuffer[0], outputBuffer[1]]
            if outputBuffer[2] == 3:
                paddlePos = [outputBuffer[0], outputBuffer[1]]

            outputBuffer = []

        iters += 1

    print("Final score (Part 2):", tiles[(-1,0)])
