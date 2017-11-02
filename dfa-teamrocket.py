import sys, time

def readDFA(filename):
    f = open(filename, 'r')
    machine = {}
    machine['name'] = f.readline().strip()
    print(machine['name']) # echo machine name
    machine['alphabet'] = f.readline().strip().split(',') # populate machine alphabet
    machine['states'] = f.readline().strip().split(',') # populate states list
    machine['start'] = f.readline().strip() # read in start state
    machine['accept'] = f.readline().strip().split(',') # populate start states list
    machine['transition'] = {key: {} for key in machine['states']}
    machine['rules'] = []
    count = 1
    for line in f:
        # generate data structure for DFA based on rules
        line = line.strip().split(',')
        machine['rules'].append(line)
        print('Rule {}: {},{},{}').format(count, line[0], line[1], line[2])
        machine['transition'][line[0]][line[1]] = line[2]
        count += 1
    f.close()
    return machine

def resetDFA(machine):
    machine['current'] = machine['start']

def readStrings(filename, machine):
    f = open(filename, 'r')
    for line in f:
        resetDFA(machine)
        currentString = line.strip()
        print("String: {}").format(currentString)
        start = time.time()
        output = processString(currentString, machine)
        end = time.time()
        runtime = end - start
        print(output + "\nRuntime: " + str(1000000*runtime) + " microseconds\n")

def processString(string, machine):
    for i,c in enumerate(string):
        if c not in machine['alphabet']:
            return "Rejected"
        elif c not in machine['transition'][machine['current']]:
            return "Rejected"
        else:
            nextState = machine['transition'][machine['current']][c]
            index = machine['rules'].index([machine['current'], c, nextState])
            # print('{},{}=?{}').format(machine['current'],c,nextState)
            print('{},{},{},{},{}').format(i+1, index + 1, machine['current'], c, nextState)
            machine['current'] = nextState
    if machine['current'] in machine['accept']:
        return 'Accepted'
    else:
        return 'Rejected'


args = sys.argv[1:]
dfa = readDFA(args[0])
print('\n')
readStrings(args[1], dfa)
