from __future__ import print_function


if __name__ == "__main__":
	with open("data/08_data", "r") as f:
		data = f.read().strip()

	width = 25
	height = 6
	numPixelsOnSingleLayer = width * height

	layers = [data[i:i+numPixelsOnSingleLayer] \
			  for i in range(0,len(data)-1,numPixelsOnSingleLayer)]

	least0sLayer = sorted(layers, key=lambda x: x.count("0"))[0]

	num1sMultBy2s = least0sLayer.count("1") * least0sLayer.count("2")
        print("Part 1:", num1sMultBy2s)

	finalValues = []
	for i in range(numPixelsOnSingleLayer):
		finalValues.append("2")
		for l in reversed(layers):
			if l[i] != "2":
				finalValues[i] = l[i]

        print("Part 2: v\n")
	for h in range(height):
		for w in range(width):
			v = finalValues[h*width + w]
			print(v if v == "1" else " ", end='')
		print()
