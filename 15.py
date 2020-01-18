import intcodeComputerClass as intcodeComputer
import json


class Droid:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, direction):
        if direction == 1:
            self.y += 1
        elif direction == 2:
            self.y -= 1
        elif direction == 3:
            self.x += 1
        elif direction == 4:
            self.x -= 1

def drawMap(tiles, droid):
    if not tiles:
        return

    minX, maxX = None, None
    minY, maxY = None, None
    for pos, value in tiles.items():
        x, y = pos

        if not minX or x < minX:
            minX = x
        if not maxX or x > maxX:
            maxX = x
        if not minY or y < minY:
            minY = y
        if not maxY or y > maxY:
            maxY = y
        
    _map = [list(" " for i in range(minX, maxX+1)) for i in range(minY, maxY+1)]
    values = ["#",".","o","O"]
    for pos, value in tiles.items():
        _map[len(_map)-1-pos[1]+minY][pos[0]-minX] = values[value]
    _map[-droid.y+minY-1][droid.x-minX] = "D"

    print "\n".join(["".join(g) for g in _map])

if __name__ == "__main__":
    with open("data/15_data", "r") as f:
        _input = f.read()

    code = list(map(int, _input.split(",")))

    # Part 1
    ic = intcodeComputer.IntcodeComputer(code)
    droid = Droid()
    tile = (0,0)
    tiles = {tile:1}
    oppositeDir = [0,2,1,4,3]

    def step(_input):
        out = ic.step(_input)
        while out is None:
            out = ic.step(_input)

        return out

    explorationList = [(0, tile, ic.getState())]

    while explorationList:
        steps, tile, icState = explorationList.pop(0)

        x,y = tile
        ic.setState(*icState)

        tilePotentialNeighbours = [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
        neighboursToExplore = [(n,i+1) for i, n in enumerate(
            tilePotentialNeighbours) if n not in tiles.keys()]

        if tiles[x,y] == 2:
            print("Part 1:", steps)

        for n, _dir in neighboursToExplore:
            out = step(_dir)

            tiles[n] = out
                
            if out != 0:
                explorationList.append((steps+1, n, ic.getState()))
                ic.setState(*icState)

    # Part 2
    tile = [k for k,v in tiles.items() if v == 2][0]  # Oxygen system
    oxygenTiles = tiles.copy()
    oxygenTiles[tile] = 3

    tilesToFill = [(tile, 0)]
    distances = []
    while 1 in tiles.values():
        tile, thisDistance = tilesToFill.pop(0)
        x,y = tile

        tilePotentialNeighbours = [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
        noOxygenNeighbours = [n for n in tilePotentialNeighbours\
                if n in tiles.keys() and tiles[n] == 1]

        for n in noOxygenNeighbours:
            tilesToFill.append((n, thisDistance+1))

        tiles[(x,y)] = 3

        distances.append(thisDistance)

    print("Part 2:", max(distances))
