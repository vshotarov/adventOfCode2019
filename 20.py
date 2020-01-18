import heapq


DEBUG = False
if DEBUG:
    from pprint import pprint

class Data(list):
    def set(self, xy, val):
        self[xy[1]][xy[0]] = val

    def get(self, xy):
        try:
            return self[xy[1]][xy[0]]
        except IndexError as e:
            # Soft constraint on size of grid, so
            # i don't have to validate each time
            return None

def printMap(data):
    print "\n".join(["".join(x) for x in data])

def getPortals(data):
    outerPortals = {}
    innerPortals = {}
    toIgnore = []

    for i, row in enumerate(data):
        for j, x in enumerate(row):
            if (j, i) in toIgnore:
                continue

            if x not in [" ","#","."]:
                # Possible locations of the second letter are
                #   - to the right
                direction = None
                otherCharacter = data.get((j+1,i))
                if otherCharacter not in [" ","#","."]:
                    direction = [1, 0]
                    toIgnore.append((j+1, i))
                else:
                    otherCharacter = None

                if not otherCharacter:
                    otherCharacter = data.get((j,i+1))
                    direction = [0, 1]
                    toIgnore.append((j, i+1))

                assert direction, "Could not find 2nd char for portal name" + str((j, i))

                # Find portal tile
                portalTile = (j+direction[0]*2, i+direction[1]*2)
                try:
                    portalTileVal = data.get(portalTile)
                    if portalTileVal != ".":
                        portalTile = (j-direction[0], i-direction[1])
                except IndexError as e:
                    portalTile = (j-direction[0], i-direction[1])

                # Identify if inner or outer
                if portalTile[0] < 3 or portalTile[0] > (len(data[2]) - 4) or\
                        portalTile[1] < 3 or portalTile[1] > (len(data) - 4):
                    outerPortals[x+otherCharacter] = portalTile
                else:
                    innerPortals[x+otherCharacter] = portalTile

    if DEBUG:
        print("Inner:")
        pprint(innerPortals)
        print("Outer:")
        pprint(outerPortals)

    return innerPortals, outerPortals

def bfs(data, startPos, targetPos, innerPortals, outerPortals, recursive=False):
    exploreList = [(0, startPos, 0)]
    visited = set([startPos[0], startPos[1], 0])

    prevMaxSteps = 0

    while exploreList:
        steps, (x,y), depth = exploreList.pop(0)

        if steps > prevMaxSteps:
            #print("Max steps", steps, len(exploreList))
            prevMaxSteps = steps

        if depth < -(len(outerPortals) + len(innerPortals)):
            # Depth can't be larger than amount of portals
            continue

        if (x,y) == targetPos and depth == 0:
            break

        visited.add((x,y,depth))

        # Find neighbours
        potentialNeighbours = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        validNeighbours = [(n,0) for n in potentialNeighbours if data.get(n) == "."]
        
        if (x,y) in innerPortals.values():
            # Inner portals available on all levels
            validNeighbours.append((
                    outerPortals[[k for k,v in innerPortals.items() if v == (x,y)][0]],
                    -1 if recursive else 0))

        elif (x,y) in outerPortals.values() and depth != 0:
            # Outer portals available on all levels except 0
            validNeighbours.append((
                    innerPortals[[k for k,v in outerPortals.items() if v == (x,y)][0]],
                    +1 if recursive else 0))

        for n,d in validNeighbours:
            if (n[0], n[1], depth+d) in visited:
                continue
            exploreList.append((steps+1, n, depth+d))

    return steps

def getVisiblePortals(data, startPos, portals):
    exploreList = [(startPos, 0)]
    visited = set([])
    visible = {}

    while exploreList:
        (x,y), steps = exploreList.pop(0)

        if (x,y) in visited:
            continue

        visited.add((x,y))

        potentialNeighbours = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        validNeighbours = [n for n in potentialNeighbours if data.get(n) == "."]

        for n in potentialNeighbours:
            if n in portals.keys() and n != startPos:
                visible[n] = (portals[n], steps+1)

        exploreList += [(n, steps+1) for n in validNeighbours]

    if portals[startPos] not in ["AA", "ZZ"]:
        visible[[k for k,v in portals.items()\
                if v == portals[startPos] and k != startPos][0]] = (portals[startPos], 1)

    return visible

def buildGraph(data, startPos, targetPos, innerPortals, outerPortals):
    portals = {v:k for d in [innerPortals, outerPortals] for k,v in d.items()}
    portals[startPos] = "AA"
    portals[targetPos] = "ZZ"

    graph = {}

    for k,v in portals.items():
        graph[k] = getVisiblePortals(data, k, portals)

    return graph

def bfsGraph(graph, startPos, targetPos, recursive=False, innerPortals={}, outerPortals={}):
    thisGraph = {k:v for k,v in graph.items()}
    exploreList = [(0, startPos, 0)]
    visited = set([])

    maxSteps = 0

    while exploreList:
        steps, (x,y), depth = heapq.heappop(exploreList)

        if steps > maxSteps:
            #print("Max steps", steps, len(exploreList))
            maxSteps = steps

        if (x,y) == targetPos and depth == 0:
            return steps

        if (x,y,depth) in visited:
            continue

        visited.add((x,y,depth))

        neighbours = thisGraph[(x,y)]

        for n, (name, stepsTo) in neighbours.items():
            if n == startPos:
                continue

            if recursive:
                if n == targetPos:
                    # If we can go to the target position
                    if depth == 0:
                        # and we are on level 0
                        depthDirection = 0
                    else:
                        # target position is only accessible on level 0
                        continue
                else:
                    # any tile that is not the target position
                    if stepsTo == 1:
                        # if we are making a portal jump
                        # we check whether it's an inner or an outer portal
                        if (x,y) in innerPortals.values():
                            # Inner portal goes down a level
                            depthDirection = -1
                        else:
                            # Outer portal goes up a level
                            # but only if we are not on level 0
                            if depth == 0:
                                continue
                            depthDirection = 1
                    else:
                        # not making a portal jump, so we treat it the same
                        # way as if it was a non recursive maze
                        depthDirection = 0
                heapq.heappush(exploreList, (steps+stepsTo, n, depth+depthDirection))
            else:
                heapq.heappush(exploreList, (steps+stepsTo, n, 0))

    return steps

if __name__ == "__main__":
    with open("data/20_data", "r") as f:
        _input = Data([list(x) for x in f.read().splitlines()])

    innerPortals, outerPortals = getPortals(_input)
    startPos = outerPortals.pop("AA")
    targetPos = outerPortals.pop("ZZ")


    import time
    start = time.time()
    print("Part 1: ", bfs(_input, startPos, targetPos, innerPortals, outerPortals),
        "(%.3f s)" % (time.time() - start))
    start = time.time()
    print("Part 2: ", bfs(_input, startPos, targetPos, innerPortals, outerPortals, True),
        "(%.3f s)" % (time.time() - start))

    graph = buildGraph(
            _input, startPos, targetPos, innerPortals, outerPortals)
    start = time.time()
    print("Part 2 using portals instead of tiles as nodes: ",
          bfsGraph(graph, startPos, targetPos, True, innerPortals, outerPortals),
          "(%.3f s)" % (time.time() - start))

