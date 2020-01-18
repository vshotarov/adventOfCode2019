import intcodeComputerClass as intcodeComputer


if __name__ == "__main__":
    with open("data/21_data", "r") as f:
        _input = f.read()

    code = list(map(int, _input.split(",")))

    # Part 1
    ic = intcodeComputer.IntcodeComputer(code)

    outputs = []
    # If any of A,B,C are missing and D is solid -> JUMP
    program = """
NOT A T
NOT B J
OR T J
NOT C T
OR T J
AND D J
WALK\n"""
    inputs = [ord(x) for x in program[1:]]

    def inputCallback():
        if not inputs:
            print "".join(outputs)
        return inputs.pop(0)

    ic.setInputCallback(inputCallback)

    success = False
    while not ic.finished:
        out = ic.step()

        if out is not None:
            if out > 255:
                print "Part 1:", out
                success = True
                break
            outputs.append(chr(out))

    if not success:
        print "".join(outputs)

    # Part 2
    ic = intcodeComputer.IntcodeComputer(code)

    # # Base is same as part 1, but then we need to make
    # # sure that if we need to make another jumpt immediately
    # # after the first, there is a solid ground at H
    program = """
NOT A T
NOT B J
OR T J
NOT C T
OR T J
AND D J
NOT E T
AND H T
OR E T
AND T J
RUN\n"""
    inputs = [ord(x) for x in program[1:]]

    outputs = []
    def inputCallback():
        return inputs.pop(0)

    ic.setInputCallback(inputCallback)

    success = False
    while not ic.finished:
        out = ic.step()

        if out is not None:
            if out > 255:
                success = True
                print "Part 2:", out
                break
            outputs.append(chr(out))

    if not success:
        print "".join(outputs)
