import intcodeComputerClass as intcodeComputer
from itertools import combinations


PICKABLE_ITEMS = ["space law space brochure", "manifold", "polygon",
        "weather machine", "astrolabe", "prime number", "hologram", "mouse"]
ALL_COMBOS = []
for i in range(2, 8):
    ALL_COMBOS += combinations(PICKABLE_ITEMS, i)

with open("ALL_COMBOS", "w") as f:
    prev = PICKABLE_ITEMS
    for combo in ALL_COMBOS:
        for each in prev:
            f.write("drop " + each + "\n")
        for each in combo:
            f.write("take " + each + "\n")
        f.write("Trying " + str(combo) + "\n")
        f.write("east" + "\n")
        prev = list(combo)

with open("25_instructions", "r") as f:
    # Instructions are a combination of
    # - first - manually typed in commands for exploring
    #       the map and collecting all collectable items
    # - second - the ALL_COMBOS from above, which 
    #       literally brute forces all possible item combinations
    INSTRUCTIONS = f.read().splitlines()

def drawMap(tiles, droid):
    if not tiles:
        return

    minX, maxX = None, None
    minY, maxY = None, None
    for pos, value in tiles.items():
        x, y = pos

        if minX is None or x < minX:
            minX = x
        if maxX is None or x > maxX:
            maxX = x
        if minY is None or y < minY:
            minY = y
        if maxY is None or y > maxY:
            maxY = y
        
    _map = [list(" " for i in range(minX, maxX+1)) for i in range(minY, maxY+1)]
    values = ["#",".","o","O"]
    for pos, value in tiles.items():
        _map[len(_map)-1-pos[1]+minY][pos[0]-minX] = value
    _map[-droid[1]+minY-1][droid[0]-minX] = "X"

    print "\n".join(["".join(g) for g in _map])

if __name__ == "__main__":
    with open("data/25_data", "r") as f:
        _input = f.read()

    code = list(map(int, _input.split(",")))

    outputBuffer = []
    inputBuffer = []
    tiles = {(0,0):"."}
    pos = [0,0]
    def inputCallback():
        global outputBuffer, inputBuffer, tiles, pos

        if not inputBuffer:
            #drawMap(tiles, pos)

            print("".join(outputBuffer))
            outputBuffer = []

            if INSTRUCTIONS:
                strInput = INSTRUCTIONS.pop(0) + "\n"
                if "Trying" in strInput:
                    print(strInput)
                    strInput = INSTRUCTIONS.pop(0) + "\n"
            else:
                strInput = raw_input() + "\n"
            print(strInput)
            inputBuffer = [ord(x) for x in strInput]

            if strInput[:-1] == "north":
                pos[1] += 1
            elif strInput[:-1] == "south":
                pos[1] -= 1
            elif strInput[:-1] == "east":
                pos[0] += 1
            elif strInput[:-1] == "west":
                pos[0] -= 1

            tiles[tuple(pos)] = "."

        return inputBuffer.pop(0)

    ic = intcodeComputer.IntcodeComputer(code,
            inputCallback=inputCallback)

    while not ic.finished:
        out = ic.step()

        if out is not None:
            outputBuffer.append(chr(out))

    if ic.finished:
        print("".join(outputBuffer))
        print("FINISHED")
