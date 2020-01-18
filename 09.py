import intcodeComputerClass as intcodeComputer

if __name__ == "__main__":
    with open("data/09_data", "r") as f:
        _input = f.read()

    print("Part 1: (Input 1)")
    code = list(map(int, _input.split(",")))
    ic = intcodeComputer.IntcodeComputer(code)
    ic.inputs = [1]
    ic.compute()

    print("Part 2: (Input 2)")
    code = list(map(int, _input.split(",")))
    ic = intcodeComputer.IntcodeComputer(code)
    ic.inputs = [2]
    ic.compute()
