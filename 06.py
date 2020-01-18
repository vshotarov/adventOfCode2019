def getAllOrbits(d, a):
	allOrbits = []

	if a in d.keys():
		allOrbits.append(d[a])
		allOrbits += getAllOrbits(d, d[a])

	return allOrbits

def buildMap(dr):
	_map = {}

	for k,v in dr.items():
		pass
		

if __name__ == "__main__":
	with open("data/06_data", "r") as f:
		_input = f.read()

	direct, indirect = 0, 0
	d = {} # key orbits value
	dr = {} # values orbit key

	for line in _input.splitlines():
		a,b = line.split(")")
		
		d[b] = a

		if a not in dr.keys():
			dr[a] = []

		dr[a].append(b)

		direct += 1

	totalOrbits = 0

	for k in d.keys():
		totalOrbits += len(getAllOrbits(d, k))

		if k == "YOU":
			myPathToCOM = getAllOrbits(d,k)
		elif k == "SAN":
			santaPathToCOM = getAllOrbits(d,k)

        print("Total orbits (Part 1):", totalOrbits)

	common = None
	for item in myPathToCOM:
		if item in santaPathToCOM:
			common = item
			break

        print("Num orbitral transfers between me and Santa (Part 2):",
                myPathToCOM.index(common) + santaPathToCOM.index(common))
