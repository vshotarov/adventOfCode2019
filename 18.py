import collections
import itertools
import fileinput
import heapq


def reachable_keys(sx, sy, keys, grid):
    q = collections.deque([(sx, sy, 0)])
    seen = set()
    d = ( (-1, 0), (1, 0), (0, -1), (0, 1) )
    while q:
        cx, cy, l = q.popleft()
        if grid[cy][cx].islower() and grid[cy][cx] not in keys:
            yield l, cx, cy, grid[cy][cx]
            continue
        for dx, dy in d:
            nx, ny = cx + dx, cy + dy
            if ((nx, ny)) in seen:
                continue
            seen.add((nx, ny))

            c = grid[ny][nx]
            if c != '#' and (not c.isupper() or c.lower() in keys):
                q.append((nx, ny, l + 1))

def getVisibleKeys(tiles, pos, collectedKeys):
    exploreList = [(pos, 0)]
    explored = []
    pickedKeys = []

    while exploreList:
        thisPos, thisDist = exploreList.pop(0)
        thisValue = tiles[thisPos]

        if thisPos in explored:
            continue

        x,y = thisPos
        possibleNeighbours = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

        if thisValue.islower() and thisValue not in collectedKeys:
            pickedKeys.append((thisValue, thisDist, thisPos))

        for n in possibleNeighbours:
            value = tiles[n]

            if value.islower() or value.lower() in collectedKeys or value in ["@","."]:
                exploreList.append((n, thisDist+1))

        explored.append(thisPos)

    return pickedKeys


if __name__ == "__main__":
    with open("data/18_data", "r") as f:
        _input = f.read().splitlines()

    tiles = {}
    keys = {}
    doors = {}
    height, width = len(_input), len(_input[0])
    _map = [[_input[y][x] for x in range(width-1)] for y in range(height)]

    part1 = True

    # Part 1
    for y in range(height):
        for x in range(width):
            data = _input[y][x]

            tiles[(x,y)] = data

            if data.isupper():
                doors[data] = (x,y)
            elif data.islower():
                keys[data] = (x,y)
            elif data == "@":
                startPos = (x,y)

    exploreList = [(0, startPos, frozenset([]))]
    explored = set([])
    numSeen = 0
    while exploreList:
        thisDist, thisPos, thisKeys = heapq.heappop(exploreList)
        x,y = thisPos

        if numSeen < len(thisKeys):
            #print "Exploring", thisPos, thisDist, thisKeys
            numSeen = len(thisKeys)

        if len(thisKeys) == len(keys.keys()):
            print "Part 1:", thisDist
            break

        if (tuple(thisPos),thisKeys) in explored:
            continue
        for dist, posX, posY, key in reachable_keys(x,y,thisKeys,_input):
            pos = (posX, posY)
            newKeys = set(thisKeys)
            newKeys.add(key)
            heapq.heappush(exploreList, (thisDist+dist,pos,frozenset(newKeys)))

        explored.add((tuple(thisPos), thisKeys))

    # Part 2
    _input = [list(x) for x in _input]

    _input[40][40] = "#"
    _input[39][40] = "#"
    _input[41][40] = "#"
    _input[40][39] = "#"
    _input[40][41] = "#"
    _input[39][39] = _input[41][39] = _input[41][41] = _input[39][41] = "@"

    _input = ["".join(x) for x in _input]

    pos = []
    for y in range(height):
        for x in range(width):
            data = _input[y][x]

            tiles[(x,y)] = data

            if data.isupper():
                doors[data] = (x,y)
            elif data.islower():
                keys[data] = (x,y)
            elif data == "@":
                pos.append((x,y))

    exploreList = [(0, pos, frozenset([]))]
    explored = set([])
    numSeen = 0
    while exploreList:
        thisDist, thisPos, thisKeys = heapq.heappop(exploreList)

        if numSeen < len(thisKeys):
            #print "Exploring", thisPos, thisDist, thisKeys
            numSeen = len(thisKeys)

        if len(thisKeys) == len(keys.keys()):
            print "Part 2:", thisDist
            break

        if (tuple(thisPos),thisKeys) in explored:
            continue

        for i, p in enumerate(thisPos):
            for dist, posX, posY, key in reachable_keys(p[0],p[1],thisKeys,_input):
                newPos = list(thisPos)
                newPos[i] = (posX, posY)
                newKeys = set(thisKeys)
                newKeys.add(key)
                heapq.heappush(exploreList, (thisDist+dist,newPos,frozenset(newKeys)))

        explored.add((tuple(thisPos), thisKeys))
