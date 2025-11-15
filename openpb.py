def parseline(line):
    parts = []
    i = 0
    n = len(line)

    while i < n:
        if line[i] == ' ':
            i += 1
            continue

        if line[i] == '"':
            start = i + 1
            i += 1
            while i < n and line[i] != '"':
                i += 1
            parts.append(line[start:i])   # clean string
            i += 1
            continue

        start = i
        while i < n and line[i] not in (' ', '"'):
            i += 1
        parts.append(line[start:i].upper())

    return parts[0], parts[1:]

def runpb(lines):
    numlist = sorted(lines.keys())
    i = 0

    while i < len(numlist):
        line_num = numlist[i]
        current = lines[line_num]

        opcode = current[0]
        args   = current[1:]

        if opcode == "GOTO":
            target = int(args[0])
            i = numlist.index(target)
            continue

        if opcode == "PRINT":
            print(args[0])

        i += 1

if __name__ == '__main__':
    lines = {}
    varibles = {}
    print("\n**** open progressbasic v1 ****\nREADY\n")
    while True:
        inp = input()
        p, j = parseline(inp)
        if p == 'RUN':
            runpb(lines)
        elif p.isdigit():
            lines[int(p)] = j
