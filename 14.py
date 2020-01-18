def getOre(table, minBatches, element, quantity, stock={}):
    #print("getOre", element, quantity, stock)

    if element not in stock.keys():
        stock[element] = 0

    if element == "ORE":
        ore = quantity
        stock["ORE"] -= quantity
        return ore

    if quantity <= stock[element]:
        stock[element] -= quantity
        return 0

    needed = quantity - stock[element]
    stock[element] = 0

    batchesNeeded = needed / minBatches[element]
    batchesNeeded += 1 if (needed % minBatches[element]) else 0

    ore = 0
    for _el, _quant in table[element].items():
        ore += getOre(table, minBatches, _el, _quant * batchesNeeded, stock)

    stock[element] += (batchesNeeded * minBatches[element]) - needed

    return ore

if __name__ == "__main__":
    with open("data/14_data", "r") as f: _input = f.read()

    _input = _input.splitlines()

    # Construct a table of all the reactions available
    table = {}
    minBatches = {}
    for line in _input:
        inputs, output = line.split(" => ")
        outQuantity, outType = output.split(" ")

        minBatches[outType] = int(outQuantity)
        table[outType] = {}

        for element in inputs.split(", "):
            elQuantity, elType = element.split(" ")
            table[outType][elType] = int(elQuantity)

    minBatches["ORE"] = 1

    stock = {}
    print"Ore needed for one unit of fuel (Part 1): %i" %\
            getOre(table, minBatches, "FUEL", 1, stock)

    # Part 2
    startOre = 1000000000000 
    fuel = 0
    stock = {}
    step = int(1e5)
    while True:
        stockCopy = stock.copy()

        getOre(table, minBatches, "FUEL", step, stockCopy)

        if abs(stockCopy["ORE"]) > startOre:
            if step == 1:
                break

            step = int(step/2)
        else:
            fuel += step
            stock = stockCopy

    print("Fuel created by %i ORE (Part 2): %i" % (startOre, fuel))

    #from pprint import pprint
    #pprint(table)
    #pprint(minBatches)
