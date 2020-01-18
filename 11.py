# In the beginning of AoC 2019 I didn't expect to reuse the intcode
# computer as much, so I whipped it up as a bunch of functions,
# with the actual main loop in in the if __name__ == "__main__" bit
#
# After probably the 3rd time i did that i wrote and started using
# the intcodeComputerClass, but I am leaving this implementation here as well

def getArg(intcode, pointer, relativeBase, argNum):
    op = str(intcode[pointer]).zfill(5)

    if op[-2-argNum] == "1":
        return intcode[pointer+argNum]
    elif op[-2-argNum] == "2":
        return intcode[relativeBase + intcode[pointer+argNum]]
    else:
        return intcode[intcode[pointer+argNum]]

def get(ic, p, rb, a):
    return getArg(ic, p, rb, a)

def draw(tiles):
    minX, maxX, minY, maxY = None, None, None, None

    for t in tiles.keys():
        x, y = [int(_) for _ in t[1:-1].split(",")]

        if x < minX or not minX:
            minX = x
        if x > maxX or not maxX:
            maxX = x
        if y < minY or not minY:
            minY = y
        if y > maxY or not maxY:
            maxY = y

    _map = [[" " for x in range(maxX - minX + 1)] for y in range(maxY - minY + 2)]

    for t,v in tiles.items():
        x, y = [int(_) for _ in t[1:-1].split(",")]
        if v:
            _map[len(_map)-(y-minY+1)][x-minX] = "#"

    print "\n".join(["".join(x) for x in _map])

def _compute(code, inputStack):
    # Code is taken as a string with comma separated operations
    ic = list(map(int, code.split(","))) + [0] * 1000
    cl = len(ic)  # Length of data
    p = 0  # Pointer
    rb = 0  # Relative base
    ist = inputStack
    outputs = []
    paint = []
    rotate = []
    outputsCounter = 0

    pos = [0,0]
    _dir = [0,1]
    allPositions = {}
    allPos = []
    allDirs = []

    while p < cl:
        op = ic[p] % 100
        if op == 1:
            ic[ic[p+3] + (0 if (ic[p] / 10000) != 2 else rb)] = get(ic,p,rb,1) + get(ic,p,rb,2)
            p += 4
        elif op == 2:
            ic[ic[p+3] + (0 if (ic[p] / 10000) != 2 else rb)] = get(ic,p,rb,1) * get(ic,p,rb,2)
            p += 4
        elif op == 3:
            if inputStack:
                ic[ic[p+1] + 0 if ic[p] != 203 else rb] = inputStack.pop(0)
            else:
                #ic[ic[p+1] + 0 if ic[p] != 203 else rb] = int(input("Input: "))
                ic[ic[p+1] + 0 if ic[p] != 203 else rb] = int(allPositions.get(str(pos), 0))
            p += 2
        elif op == 4:
            output = get(ic,p,rb,1)
            if outputsCounter % 2 == 0:
                allPositions[str(pos)] = output
                allPos.append(pos)
                paint.append(output)
            else:
                if output == 0:
                    _dir = [-_dir[1], _dir[0]]
                else:
                    _dir = [_dir[1], -_dir[0]]
                pos = [pos[0]+_dir[0], pos[1]+_dir[1]]
                rotate.append(output)
            outputsCounter += 1
            outputs.append(output)
            #print("Output: ", outputs[-1])
            p += 2
        elif op == 5:
            # Jump if true
            if get(ic,p,rb,1) != 0:
                p = get(ic,p,rb,2)
            else:
                p += 3
        elif op == 6:
            # Jump if false
            if get(ic,p,rb,1) == 0:
                p = get(ic,p,rb,2)
            else:
                p += 3
        elif op == 7:
            # Less than
            ic[ic[p+3] + (0 if (ic[p] / 10000) != 2 else rb)] = 1 if get(ic,p,rb,1) < get(ic,p,rb,2) else 0
            p += 4
        elif op == 8:
            # Equals
            ic[ic[p+3] + (0 if (ic[p] / 10000) != 2 else rb)] = 1 if get(ic,p,rb,1) == get(ic,p,rb,2) else 0
            p += 4
        elif op == 9:
            # Offset relative base
            rb += get(ic,p,rb,1)
            p += 2
        elif ic[p] % 100 == 99:
            break
        else:
            print("Unrecognized code", ic[p])
            break

    draw(allPositions)

    return ic, outputs, allPositions

if __name__ == "__main__":
    with open("data/11_data", "r") as f:
        _input = f.read()

    print "Part 1:"
    _, _, allPos = _compute(_input, [0])
    print("Num panels painted at least once", len(allPos.keys()))

    print "Part 2:"
    _, _, allPos = _compute(_input, [1])
