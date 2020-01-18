import intcodeComputerClass as intcodeComputer


def getTilesAffectedByRayInRadius50(code):
    ic = intcodeComputer.IntcodeComputer(code)
    inputs = []
    size = 50
    for x in range(size):
        for y in range(size):
            inputs += [x,y]

    icState = ic.getState()
    outputs = [["." for _ in range(size)] for _ in range(size)]
    totalAffected = 0
    for i in range(0,len(inputs),2):
        ic.setState(*icState)
        ic.setInputs(inputs[i:i+2])
        x,y = ic.inputs

        while not ic.finished:
            out = ic.step()

            if out is not None:
                outputs[y][x] = "#" if out else "."
                totalAffected += out

    print "\n".join([str(i) + "".join(x) for i, x in enumerate(outputs)])
    print "Total affected (Part 1): ", totalAffected
    return outputs

def computeSingleRun(ic):
    while True:
        out = ic.step()

        if out is not None:
            return out

def findFirstAffectedOnRow(ic, resetState, startX, row):
    # Find where the ray starts affecting tiles on the current row
    ic.setState(*resetState)

    # Check if the tile on the rough slope is affected
    x, y = startX, row
    ic.setInputs([x,y])
    affected = computeSingleRun(ic)

    # If it's not affected, then it starts affecting after that tile,
    # so let's find where exactly
    if not affected:
        while not affected:
            x += 1
            ic.setState(*resetState)
            ic.setInputs([x,y])
            affected = computeSingleRun(ic)
        return x,y
    else:
        # If it's affected, we need to go backwards to find where
        # they start being affected
        while affected:
            x -= 1
            ic.setState(*resetState)
            ic.setInputs([x,y])
            affected = computeSingleRun(ic)
        return x+1,y

def getNumberAffectedOnRow(ic, resetState, firstAffected, row):
    ic.setState(*resetState)
    x = firstAffected[0] + 1
    ic.setInputs([x,row])
    affected = computeSingleRun(ic)
    while affected:
            x += 1
            ic.setState(*resetState)
            ic.setInputs([x,row])
            affected = computeSingleRun(ic)
    return x - firstAffected[0]

if __name__ == "__main__":
    with open("data/19_data", "r") as f:
        _input = f.read()

    code = list(map(int, _input.split(",")))

    # Part 1
    outputs50 = getTilesAffectedByRayInRadius50(code)

    # Part 2
    # # Find an approximation of the slope of the ray
    # # # Find the affected tiles at Y 50
    affectedAtY50 = [x for x in range(50) if outputs50[-1][x] == "#"]
    # # # Find the one to the left
    firstOneAtY50 = [affectedAtY50[0], 50]
    slope = firstOneAtY50[1] / float(firstOneAtY50[0])

    ic = intcodeComputer.IntcodeComputer(code)

    icState = ic.getState()
    currentRow = 100  # Start at row 100, as it's obvious the solution is not before that
    step = 50
    lastComboWorks = False
    squareSize = 100

    while True:
        firstAffectedOnThisRow = findFirstAffectedOnRow(
                ic, icState, int(currentRow/slope), currentRow)
        numAffectedOnThisRow = getNumberAffectedOnRow(
                ic, icState, firstAffectedOnThisRow, currentRow)

        if numAffectedOnThisRow < squareSize:
            currentRow += step
            continue

        remainder = numAffectedOnThisRow - squareSize

        firstAffectedAfter100Rows = findFirstAffectedOnRow(
                ic, icState, int((currentRow+squareSize-1)/slope), currentRow+squareSize-1)

        diff = firstAffectedAfter100Rows[0] - firstAffectedOnThisRow[0]

        if diff == remainder:
            if step == 1:
                print "Part 2: ", firstAffectedAfter100Rows[0] * 10000 + currentRow
                break
            currentRow -= step
            lastComboWorks = True
        else:
            if diff > remainder:
                currentRow += step
            else:
                currentRow -= step
                lastComboWorks = True

        if step > 1 and lastComboWorks:
            step = int(step / 2)

        lastComboWorks = False
