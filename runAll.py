if __name__ == "__main__":
    for i in range(1, 26):
        print "#" * 10 + " Day %i" % i
        print "#" * 5 + " Answers:"

        execfile("%s.py" % str(i).zfill(2))

        print
