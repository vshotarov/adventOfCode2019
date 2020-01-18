def compute_gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

def compute_lcm3(x,y,z):
    # Copied from https://stackoverflow.com/a/42517664
    # Find the 2-number and 3-number GCDs
    gcd2 = compute_gcd(y, z)
    gcd3 = compute_gcd(x, gcd2)

    # Find the 2-number and 3-number LCMs
    lcm2 = y*z // gcd2
    lcm3 = x*lcm2 // compute_gcd(x, lcm2)

    return lcm3

if __name__ == "__main__":
    with open("data/12_data", "r") as f:
        _input = f.read()

    # Gather all moon initial positions
    positions = []
    for line in _input.splitlines():
        positions.append(
                [int(each.split("=")[1]) for each in line[1:-1].split(",")])

    numMoons = len(positions)

    # Storage for position and velocity pairs for each axis
    pvx = set([])
    pvy = set([])
    pvz = set([])

    foundXCycle = False
    foundYCycle = False
    foundZCycle = False

    # Main loop
    gravity = [[0,0,0] for _ in range(numMoons)]
    for i in range(10000000):
        thisPvx = tuple([(positions[j][0], gravity[j][0]) for j in range(numMoons)])
        thisPvy = tuple([(positions[j][1], gravity[j][1]) for j in range(numMoons)])
        thisPvz = tuple([(positions[j][2], gravity[j][2]) for j in range(numMoons)])

        if thisPvx in pvx and not foundXCycle:
            print("X cycle is", i)
            foundXCycle = i
        if thisPvy in pvy and not foundYCycle:
            print("Y cycle is", i)
            foundYCycle = i
        if thisPvz in pvz and not foundZCycle:
            print("Z cycle is", i)
            foundZCycle = i

        if foundXCycle and foundYCycle and foundZCycle and i > 1000:
            break

        pvx.add(thisPvx)
        pvy.add(thisPvy)
        pvz.add(thisPvz)

        # Calculate gravity
        for j in range(numMoons):
            for k in range(j+1, numMoons):
                for x in range(3):
                    distance = positions[k][x] - positions[j][x]
                    if distance:
                        gravity[j][x] += distance / abs(distance)
                        gravity[k][x] -= distance / abs(distance)

        #print("############# After step %i" % (i+1))

        totalEnergy = 0
        for j in range(numMoons):
            # Apply velocity
            positions[j] = [positions[j][x] + gravity[j][x] for x in range(3)]

            #print("# pos=(% 2d, % 2d, % 2d) vel=(% 2d, % 2d, % 2d)" % tuple(positions[j]+gravity[j]))

            # Get energy
            potential = sum([abs(x) for x in positions[j]])
            kinetic = sum([abs(x) for x in gravity[j]])

            totalEnergy += potential * kinetic

        if i == 999:
            print("Total energy (Part 1):", totalEnergy)

    print("The first repeating state is at the step that's the LCD of the inverse of",
            foundXCycle, foundYCycle, foundZCycle)
    print("Part 2 answer:", compute_lcm3(foundXCycle, foundYCycle, foundZCycle))
