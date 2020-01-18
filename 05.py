# In the beginning of AoC 2019 I didn't expect to reuse the intcode
# computer as much, so I whipped it up as a bunch of functions,
# with the actual main loop in in the if __name__ == "__main__" bit
#
# After probably the 3rd time i did that i wrote and started using
# the intcodeComputerClass, but I am leaving this implementation here as well

def getArgument(data, pointer, index, address=False):
    instruction = data[pointer].zfill(5)

    if instruction[-2-index] == "1" or address:
        return int(data[pointer+index])
    else:
        return int(data[int(data[pointer+index])])

def addition(data, pointer):
    a = getArgument(data, pointer, 1)
    b = getArgument(data, pointer, 2)
    destination = getArgument(data, pointer, 3, True)

    data[destination] = str(a + b)

    return pointer + 4

def multiplication(data, pointer):
    a = getArgument(data, pointer, 1)
    b = getArgument(data, pointer, 2)
    destination = getArgument(data, pointer, 3, True)
    
    data[destination] = str(a * b)

    return pointer + 4

def _input(data, pointer, val=None):
    if not val:
        val = input("Input: ")

    data[int(data[pointer+1])] = str(val)
    
    return pointer + 2

def output(data, pointer):
    print "Output: %i" % getArgument(data, pointer, 1)

    return pointer + 2

def jumpIfTrue(data, pointer):
    if getArgument(data, pointer, 1) != 0:
        return getArgument(data, pointer, 2)
    return pointer + 3

def jumpIfFalse(data, pointer):
    if getArgument(data, pointer, 1) == 0:
        return getArgument(data, pointer, 2)
    return pointer + 3

def lessThan(data, pointer):
    if getArgument(data, pointer, 1) < getArgument(data, pointer, 2):
        data[getArgument(data, pointer, 3, True)] = "1"
    else:
        data[getArgument(data, pointer, 3, True)] = "0"

    return pointer + 4

def equals(data, pointer):
    if getArgument(data, pointer, 1) == getArgument(data, pointer, 2):
        data[getArgument(data, pointer, 3, True)] = "1"
    else:
        data[getArgument(data, pointer, 3, True)] = "0"

    return pointer + 4

def getOpcode(instruction):
    return int(instruction[-2:])

def compute(code, diagnosticCode):
    data = code.split(",")

    pointer = 0
    iters = 0

    while pointer < len(data) - 1:
        opcode = getOpcode(data[pointer])

        if opcode == 1:
            pointer = addition(data, pointer)
        elif opcode == 2:
            pointer = multiplication(data, pointer)
        elif opcode == 3:
            pointer = _input(data, pointer, diagnosticCode)
        elif opcode == 4:
            pointer = output(data, pointer)
        elif opcode == 5:
            pointer = jumpIfTrue(data, pointer)
        elif opcode == 6:
            pointer = jumpIfFalse(data, pointer)
        elif opcode == 7:
            pointer = lessThan(data, pointer)
        elif opcode == 8:
            pointer = equals(data, pointer)
        elif opcode == 99:
            break
        else:
            raise RuntimeError("Unrecognized opcode %i" % opcode)

        iters += 1

if __name__ == "__main__":
    with open("data/05_data", "r") as f:
        data = f.read()

    # Part 1
    print "Part 1:"
    compute(data, 1)

    # Part 2
    print "Part 2:"
    compute(data, 5)
