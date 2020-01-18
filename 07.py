# Similar to 5
#
# In the beginning of AoC 2019 I didn't expect to reuse the intcode
# computer as much, so I whipped it up as a bunch of functions,
# with the actual main loop in in the if __name__ == "__main__" bit
#
# After probably the 3rd time i did that i wrote and started using
# the intcodeComputerClass, but I am leaving this implementation here as well

from functools import partial

states = [0] * 5
pointers = [0] * 5
initialized = [0] * 5
currentCombo = [0] * 5
ampOutputs = [[], [], [], [], [0]]

def reset():
	global states, pointers, initialized, currentCombo, ampOutputs
        states = [0] * 5
        pointers = [0] * 5
        initialized = [0] * 5
        currentCombo = [0] * 5
        ampOutputs = [[], [], [], [], [0]]

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

def _compute(i, topLevel=False):
	global states, pointers, initialized, currentCombo, ampOutputs
	# Code is taken as a string with comma separated operations
	code = states[i%5]
	ic = list(map(int, code.split(",")))
	cl = len(ic)  # Length of data
	p = pointers[i%5]  # Pointer
	rb = 0  # Relative base
	outputs = []

	while p < cl:
		op = ic[p] % 100
		if op == 1:
			ic[ic[p+3]] = get(ic,p,rb,1) + get(ic,p,rb,2)
			p += 4
		elif op == 2:
			ic[ic[p+3]] = get(ic,p,rb,1) * get(ic,p,rb,2)
			p += 4
		elif op == 3:
			#ic[ic[p+1]] = int(input("Input: "))
			if ampOutputs[(i-1)%5]:
				ic[ic[p+1]] = ampOutputs[(i-1)%5].pop(0)
			else:
				prevIc, prevOut, prevP = _compute((i-1)%5)
				states[(i-1)%5] = ",".join(map(str, prevIc))
				pointers[(i-1)%5] = prevP
				ic[ic[p+1]] = ampOutputs[(i-1)%5].pop(0)
			p += 2
		elif op == 4:
			outputs.append(get(ic,p,rb,1))
			states[i%5] = ",".join(map(str, ic))
			pointers[i%5] = p+2
			ampOutputs[i%5].append(outputs[-1])
			if not topLevel:
				return ic, outputs[-1], p+2
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
			ic[ic[p+3]] = 1 if get(ic,p,rb,1) < get(ic,p,rb,2) else 0
			p += 4
		elif op == 8:
			# Equals
			ic[ic[p+3]] = 1 if get(ic,p,rb,1) == get(ic,p,rb,2) else 0
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

	return ic, outputs, p

def part1(code):
	global states, pointers, initialized, currentCombo, ampOutputs
        states = [str(code) for i in range(5)]
	possibleCombinations = []
	for i in range(5):
		for j in range(5):
			for k in range(5):
				for l in range(5):
					for m in range(5):
							if len(set([i,j,k,l,m])) < 5:
								continue
							possibleCombinations.append([i,j,k,l,m])

	maxOut = float("-inf") 
	maxOutCombo = None
	for combo in possibleCombinations:
                reset()
                states = [str(code) for i in range(5)]

                currentCombo = combo
		for i in range(5):
                        ampOutputs[(i-1)%5].insert(0, combo[i])

                        if i == 0:
                            ampOutputs[-1].append(0)

			_, out, _ = _compute(i, True if i < 4 else False)

		if out > maxOut:
			maxOut = out
			maxOutCombo = list(combo)

        print("Part 1:", maxOut, maxOutCombo)

def part2(code):
	possibleCombinations = []
	for i in range(5):
		for j in range(5):
			for k in range(5):
				for l in range(5):
					for m in range(5):
							if len(set([i,j,k,l,m])) < 5:
								continue
							possibleCombinations.append([i+5,j+5,k+5,l+5,m+5])

	maxOut = float("-inf")
	maxCombo = []
	for combo in possibleCombinations:
		i = 0
		out = 0

		global states, currentCombo, pointers
		currentCombo = list(combo)
		states = [str(code) for _ in range(5)]
		pointers = [0] * 5
		ampOutputs[0] = [currentCombo[1]]
		ampOutputs[1] = [currentCombo[2]]
		ampOutputs[2] = [currentCombo[3]]
		ampOutputs[3] = [currentCombo[4]]
		ampOutputs[4] = [currentCombo[0], 0]

		_, out, _ = _compute(0, True)
		_, out, _ = _compute(1, True)
		_, out, _ = _compute(2, True)
		_, out, _ = _compute(3, True)
		_, out, _ = _compute(4, True)

		if out[-1] > maxOut:
			maxOut = out[-1]
			maxCombo = list(combo)

        print("Part 2:", maxOut, maxCombo)

if __name__ == "__main__":
	code = "3,8,1001,8,10,8,105,1,0,0,21,42,67,88,105,114,195,276,357,438,99999,3,9,101,4,9,9,102,3,9,9,1001,9,2,9,102,4,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,101,2,9,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,1001,9,4,9,1002,9,4,9,101,2,9,9,1002,9,2,9,4,9,99,3,9,101,4,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99"
	part1(code)
	part2(code)
