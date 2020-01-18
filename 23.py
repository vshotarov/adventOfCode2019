import intcodeComputerClass as intcodeComputer
from functools import partial


if __name__ == "__main__":
    with open("data/23_data", "r") as f:
        _input = f.read()

    code = list(map(int, _input.split(",")))

    numComputers = 50

    inputs = []
    def inputCallback(_id):
        if _id < 50:
            if inputs[_id]:
                return inputs[_id].pop(0)
            return -1


    outputBuffers = []
    NATpacket = [None, None]
    sentFromNAT = []
    firstNAT = False
    alive = True
    def outputCallback(_id, output):
        #print("Output %i:" % _id, output)
        global NAToutputBuffer, firstNAT, sentFromNAT, alive
        if _id < 50:
            outputBuffers[_id].append(output)

            if len(outputBuffers[_id]) > 2 and outputBuffers[_id][-3] == 255:
                if not firstNAT:
                    print("First Y value sent to 255", output)
                    firstNAT = True

                NATpacket = outputBuffers[_id][-2:]
                outputBuffers[_id] = []

                # Check if idle
                idle = True
                for i in range(numComputers):
                    if inputs[i]:
                        idle = False

                if idle:
                    print "Restart after idle"
                    inputs[0] = list(NATpacket)

                    sentFromNAT += NATpacket

                    if len(sentFromNAT) > 2 and sentFromNAT[-1] == sentFromNAT[-3]:
                        print("First repeated Y value sent to 0 from NAT", sentFromNAT[-1])
                        alive = False

                return

            if len(outputBuffers[_id]) == 3:
                address, x, y = outputBuffers[_id]
                inputs[address] += [x,y]
                outputBuffers[_id] = []

    ic = []
    for i in range(numComputers):
        ic.append(intcodeComputer.IntcodeComputer(code))
        ic[-1].setInputCallback(partial(inputCallback, i))
        ic[-1].setOutputCallback(partial(outputCallback, i))
        inputs.append([i])
        outputBuffers.append([])

    while alive:
        for computer in ic:
            computer.step()
