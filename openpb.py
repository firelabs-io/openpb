import time
import math
import random

def parseline(line):
    parts = []
    i = 0
    n = len(line)

    while i < n:
        if line[i] == ' ':
            i += 1
            continue

        elif line[i] == '"':
            start = i
            i += 1
            while i < n and line[i] != '"':
                i += 1
            parts.append(line[start:i+1])   # clean string
            i += 1
            continue
        elif line[i] in '+-*/':
            parts.append(line[i])
        else:
            start = i
            while i < n and line[i] not in (' ', ''):
                i += 1
            parts.append(line[start:i].upper())

    return parts[0], parts[1:]

def runpb(lines):
    def split(s):
        tokens = []
        temp = ''
        for c in s:
            if c in '+-*/=()<>':
                if temp:
                    tokens.append(temp)
                    temp = ''
                tokens.append(c)
            else:
                temp += c
        if temp:
            tokens.append(temp)
        return tokens
    numlist = sorted(lines.keys())
    varibles = {}
    def ev(exp):
        # Step 1: split first token and replace variables
        pass1 = []
        for k in split(exp[0]):
            if k in varibles:
                pass1.append(str(varibles[k]))
            else:
                pass1.append(k)

        if len(pass1) == 1:
            return pass1[0]

        # Step 2: compute arithmetic left-to-right
        j = 0
        temp = [0]
        if pass1[0].isdigit():
            temp = [pass1[0]]  # start with first number
            j = 1
        while j < len(pass1):
            op = pass1[j]
            num = pass1[j+1]
            if op == '+':
                temp[0] = str(int(temp[0]) + int(num))
            elif op == '-':
                temp[0] = str(int(temp[0]) - int(num))
            elif op == '*':
                temp[0] = str(int(temp[0]) * int(num))
            elif op == '/':
                temp[0] = str(int(temp[0]) // int(num))
            elif op == '>':
                temp[0] = str(int(temp[0]) > int(num))
            elif op == '<':
                temp[0] = str(int(temp[0]) < int(num))
            elif op == 'SIN':
                temp[0] = str(math.sin(math.radians(int(ev(pass1[j+2:])))))
            elif op == 'COS':
                temp[0] = str(math.cos(math.radians(int(ev(pass1[j+2:])))))
            elif op == 'TAN':
                temp[0] = str(math.tan(math.radians(int(ev(pass1[j+2:])))))            
            elif op == 'RND':
                temp[0] = str(random.randint(1, int(ev(pass1[j+2:]))))
            j += 2

        return temp[0]
    loops = []
    i = 0
    LAST_IF = True
    while i < len(numlist):
        time.sleep(0.03) # mandetory lol
        line_num = numlist[i]
        current = lines[line_num]

        opcode = current[0]
        args   = current[1:]
        if opcode == "FOR":
            var_name, rest = args[0].split("=")[0], args[0].split("=")[1]
            start_val = int(ev([rest]))
            to_index = args.index("TO")
            end_val = int(ev([args[to_index+1]]))
            varibles[var_name] = start_val
            loops.append({
                "var": var_name,
                "end": end_val,
                "line": i
            })

        elif opcode == "NEXT":
            var_name = args[0]
            for loop in reversed(loops):
                if loop["var"] == var_name:
                    varibles[var_name] += 1
                    if varibles[var_name] <= loop["end"]:
                        i = loop["line"]
                    else:
                        loops.remove(loop)
                    break
        elif opcode == "IF":
            cond = ev(args[0])
            try:
                cond_val = int(cond)
            except:
                cond_val = cond in ["True", "true"]
            if cond_val:
                LAST_IF = True
                # Execute THEN part
                if args[1].upper() == "THEN":
                    then_code = args[2:]
                    if then_code[0] == "GOTO":
                        target = int(then_code[1])
                        i = numlist.index(target)
                        continue
                    else:
                        opcode = then_code[0]
                        args = then_code[1:]
            else:
                LAST_IF = False
                # Check for ELSE on next line
                i += 1
                if i < len(numlist):
                    next_line = lines[numlist[i]]
                    if next_line[0] == "ELSE":
                        opcode = next_line[0]
                        args = next_line[1:]
                    else:
                        i -= 1  # no ELSE, continue normally

        elif opcode == "ELSE":
            if not LAST_IF:
                # Execute ELSE block
                if args[0] == "GOTO":
                    target = int(args[1])
                    i = numlist.index(target)
                    continue
                else:
                    opcode = args[0]
                    args = args[1:]
            else:
                i += 1
                continue

        if opcode == "REM":
            i += 1
            continue
        if opcode == "GOTO":
            target = int(args[0])
            i = numlist.index(target)
            continue
        if opcode == "LET":
            l = split(args[0])
            varibles[l[0]] = l[2]
        if opcode == "PRINT":
            print(ev(args))
        if opcode == "INPUT":
            l = split(args[0])
            varibles[l[0]] = input('')
        if opcode == 'CLS':
            print("\033[2J\033[H", end="")
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
            with open(j[0]+'.txt', 'w') as f:
                for num in lines:
                    f.write(f'{num} {" ".join(lines[num])}\n')
            print('-'*3 + 'SAVED PROGRAM ' + '-'*3)
        elif p == 'LOAD':
            lines = load(j[0]+'.txt')
        elif p.isdigit():
            lines[int(p)] = j
