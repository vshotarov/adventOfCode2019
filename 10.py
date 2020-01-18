import math
#import maya.cmds as mc

THRESHOLD = 1e-5

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def angle(self, other):
        return math.acos((self * other) / (self.mag() * other.mag()))

    def normalized(self):
        mag = self.mag()
        return Vector2(self.x / mag, self.y / mag)

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        return other.x * self.x + other.y * self.y

    def __repr__(self):
        return "Vector2(%f, %f)" % (self.x, self.y)

    def __eq__(self, other):
        if abs(self.x - other.x) < THRESHOLD and abs(self.y - other.y) < THRESHOLD:
            return True
        return False

def angleFromVertical(vector):
    angle = Vector2(0,-1).angle(vector)
    if vector.x < 0:
        return 2*math.pi - angle
    return angle

if __name__ == "__main__":
    with open("data/10_data", "r") as f:
        _input = f.read()

    _input = _input.splitlines()

    width = len(_input[0])
    height = len(_input)

    # Get asteroids
    asteroids = []
    for y in range(height):
        for x in range(width):
            if _input[y][x] == "#":
                asteroids.append(Vector2(x,y))

    # Visible asteroids per asteroid
    rays = [{} for a in asteroids]
    for i in range(len(asteroids)):
        a = asteroids[i]

        for b in asteroids:
            if a == b:
                continue

            ab = b-a

            abNorm = ab.normalized()
            key = str(abNorm)
            if key not in rays[i].keys():
                rays[i][key] = [abNorm]

            rays[i][key].append((b, ab.mag()))

    numVisAsteroids = [len(x.keys()) for x in rays]
    maxVisAsteroids = max(numVisAsteroids)
    maxVisAsteroidsId = numVisAsteroids.index(maxVisAsteroids)
    station = asteroids[maxVisAsteroidsId]

    print("Max visible asteroids (Part 1):", maxVisAsteroids)

    stationData = [v for k,v in rays[maxVisAsteroidsId].items()]

    # Sort station rays by angle
    sortedStationData = sorted(stationData, key=lambda x: angleFromVertical(x[0]))
    for i in range(len(sortedStationData)):
        sortedStationData[i] = [sortedStationData[i][0]] +\
                sorted(sortedStationData[i][1:], key=lambda x:x[1])

    # Visualise in maya #
    #mc.file(new=1,f=1)
    #spheres = {}
    #for y in range(height):
    #    for x in range(width):
    #        if _input[y][x] == "#":
    #            if x == int(station.x) and y == int(station.y):
    #                sp = mc.polySphere(ch=0,r=.55)
    #            else:
    #                sp = mc.polySphere(ch=0,r=.15)
    #            mc.xform(sp, t=[x,-y,0])
    #            spheres[(x,y)] = sp[0]

    #for each in sortedStationData:
    #    mc.curve(p=[[station.x, -station.y, 0], [station.x + each[0].x * 10, -station.y - each[0].y * 10, 0]], d=1)

    class Destroyer:
        def __init__(self):
            self.pointer = 0
            self.cycles = 0
            self.frame = 2
            self.frameStep = 2

        def step(self):
            if len(sortedStationData[self.pointer]) > self.cycles + 1:
                destroyed = sortedStationData[self.pointer][self.cycles+1][0]
                #print("Destroy", destroyed)

                if self.pointer == 199:
                    print("200th destroyed:", "Vec2(%i, %i)" % (destroyed.x, destroyed.y))
                    print("Part 2: ", destroyed.x * 100 + destroyed.y)

                # Visualise in maya #
                #destroyedSp = spheres[(int(destroyed.x), int(destroyed.y))]
                #mc.setKeyframe(destroyedSp + ".v", t=self.frame-self.frameStep, v=1)
                #mc.setKeyframe(destroyedSp + ".v", t=self.frame, v=0)

                self.frame += self.frameStep

            self.pointer += 1

            if self.pointer == len(sortedStationData):
                self.pointer = 0
                self.cycles += 1

    d = Destroyer()
    for i in range(2000):
        d.step()
