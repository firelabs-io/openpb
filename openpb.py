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
            parts.append(line[start:i+1])
            i += 1
            continue
        elif line[i] in '+-*/':
            parts.append(line[i])
            i += 1
        else:
            start = i
            while i < n and line[i] not in (' ', ''):
                i += 1
            parts.append(line[start:i].upper())

    return parts[0], parts[1:]

def runpb(numlist, codelist):
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

    varibles = {}
    loops = []
    i = 0
    LAST_IF = True
    while i < len(numlist):
        time.sleep(0.03)
        line_num = numlist[i]
        current = codelist[i]

        opcode = current[0]
        args = current[1:]

        if opcode == "FOR":
            var_name, rest = args[0].split("=")[0], args[0].split("=")[1]
            start_val = int(ev([rest], varibles))
            to_index = args.index("TO")
            T = args[to_index+1]
            if T in varibles:
                T = varibles[T]
            end_val = int(ev([T], varibles))
            varibles[var_name] = start_val
            loops.append({"var": var_name, "end": end_val, "line": i})

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
            cond = ev(args[0], varibles)
            try:
                cond_val = int(cond)
            except:
                cond_val = cond in ["True", "true"]
            if cond_val:
                LAST_IF = True
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
                i += 1
                if i < len(numlist):
                    next_line = codelist[i]
                    if next_line[0] == "ELSE":
                        opcode = next_line[0]
                        args = next_line[1:]
                    else:
                        i -= 1

        elif opcode == "ELSE":
            if not LAST_IF:
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
            if args[0] in varibles:
                target = varibles[args[0]]
                i = numlist.index(target)
            else:
                target = int(args[0])
                i = numlist.index(target)
            continue
        if opcode == "LET":
            l = split(args[0])
            if l[2] in varibles:
                varibles[l[0]] = varibles[l[2]]
            else:
                varibles[l[0]] = l[2]
        if opcode == "PRINT":
            if len(args) == 1:
                if args[0] in varibles:
                    print(varibles[args[0]])
                else:
                    print(args[0])
            else:
                print(ev(args, varibles).replace('"', ''))
        if opcode == "INPUT":
            l = split(args[0])
            varibles[l[0]] = input('')
        if opcode == "CLS":
            print("\033[2J\033[H", end="")

        i += 1

def ev(exp, varibles):
    def split_tokens(s):
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

    pass1 = []
    for k in split_tokens(exp[0]):
        if k in varibles:
            pass1.append(str(varibles[k]))
        else:
            pass1.append(k)

    if len(pass1) == 1:
        return pass1[0]

    j = 0
    temp = [0]
    if pass1[0].isdigit():
        temp = [pass1[0]]
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
            temp[0] = str(math.sin(math.radians(int(ev(pass1[j+2:], varibles)))))
        elif op == 'COS':
            temp[0] = str(math.cos(math.radians(int(ev(pass1[j+2:], varibles)))))
        elif op == 'TAN':
            temp[0] = str(math.tan(math.radians(int(ev(pass1[j+2:], varibles)))))            
        elif op == 'RND':
            temp[0] = str(random.randint(1, int(ev(pass1[j+2:], varibles))))
        j += 2
    return temp[0]

def load(file):
    numlist = []
    codelist = []
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            num, parts = parseline(line)
            numlist.append(int(num))
            codelist.append(parts)
    return numlist, codelist

if __name__ == '__main__':
    numlist = []
    codelist = []
    print("\n**** open progressbasic v1 ****\nREADY\n")
    while True:
        inp = input()
        p, j = parseline(inp)
        if p == 'RUN':
            runpb(numlist, codelist)
            print("="*30)
            print("THE PROGRAM HAS BEEN COMPLETED")
        elif p == 'HOME':
            print("\033[2J\033[H", end="")
        elif p == 'LIST':
            for n, stmt in sorted(zip(numlist, codelist), key=lambda x: x[0]):
                print(n, " ".join(stmt))
        elif p == 'DELETE':
            target = int(j[0])
            pairs = list(zip(numlist, codelist))
            pairs = [p for p in pairs if p[0] != target]
            numlist = [p[0] for p in pairs]
            codelist = [p[1] for p in pairs]
        elif p == 'CLEAR':
            numlist = []
            codelist = []
        elif p == 'SAVE':
            with open(j[0]+'.txt', 'w') as f:
                for n, stmt in zip(numlist, codelist):
                    f.write(f"{n} {' '.join(stmt)}\n")
            print('-'*3 + 'SAVED PROGRAM ' + '-'*3)
        elif p == 'LOAD':
            numlist, codelist = load(j[0]+'.txt')
        elif p.isdigit():
            numlist.append(int(p))
            codelist.append(j)
