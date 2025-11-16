import time
def parseline(line):
    parts = []
    i = 0
    n = len(line)

    while i < n:
        if line[i] == ' ':
            i += 1
            continue

        if line[i] == '"':
            start = i
            i += 1
            while i < n and line[i] != '"':
                i += 1
            parts.append(line[start:i+1])   # clean string
            i += 1
            continue

        start = i
        while i < n and line[i] not in (' ', '"'):
            i += 1
        parts.append(line[start:i].upper())

    return parts[0], parts[1:]

def runpb(lines):
    numlist = sorted(lines.keys())
    varibles = {}
    i = 0

    while i < len(numlist):
        time.sleep(0.03)
        line_num = numlist[i]
        current = lines[line_num]

        opcode = current[0]
        args   = current[1:]
        if opcode == "REM":
            i += 1
            continue
        if opcode == "GOTO":
            target = int(args[0])
            i = numlist.index(target)
            continue
        if opcode == "PRINT":
            if args[0] in varibles:
                print(varibles[args[0]])
            else:
                print(args[0].replace('"', ''))
        if opcode == "INPUT":
            varibles[args[0]] = input('')
            
        i += 1

def load(file):
    program = []
    lines = {}
    with open(file, 'r') as f:
        program = f.read().split('\n')
        del program[-1]
    for e in program:
        ind, parts = parseline(e)
        lines[int(ind)] = parts
        print(lines)
    return lines

if __name__ == '__main__':
    lines = {}
    print("\n**** open progressbasic v1 ****\nREADY\n")
    while True:
        inp = input()
        p, j = parseline(inp)
        if p == 'RUN':
            runpb(lines)
            print("="*30)
            print("THE PROGRAM HAS BEEN COMPLETED")
        elif p == 'HOME':
            print("\033[2J\033[H", end="")
        elif p == 'LIST':
            for num in sorted(lines):
                print(f"{num} {" ".join(lines[num])}")
        elif p == 'DELETE':
            if int(j[0]) in lines:
                del lines[int(j[0])]
        elif p == 'CLEAR':
            lines = {}
        elif p == 'SAVE':
            with open(j[0]+'.pb', 'w') as f:
                for num in lines:
                    f.write(f'{num} {" ".join(lines[num])}\n')
            print('-'*3 + 'SAVED PROGRAM ' + '-'*3)
        elif p == 'LOAD':
            lines = load(j[0]+'.pb')
        elif p.isdigit():
            lines[int(p)] = j
