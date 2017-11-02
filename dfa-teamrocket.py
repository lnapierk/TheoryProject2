import sys, time

def readDFA(filename):
    f = open(filename, 'r')
    machine = {} # dictionary to represent the entire DFA
    machine['name'] = f.readline().strip()
    print(machine['name']) # echo machine name
    machine['alphabet'] = f.readline().strip().split(',') # populate machine alphabet
    machine['states'] = f.readline().strip().split(',') # populate states list
    machine['start'] = f.readline().strip() # read in start state
    machine['accept'] = f.readline().strip().split(',') # populate start states list
    machine['transition'] = {key: {} for key in machine['states']} # create blank transition function
    machine['rules'] = [] # create list of rules
    count = 1 # use to keep track of rule number
    for line in f:
        # generate data structure for DFA based on rules
        line = line.strip().split(',')
        machine['rules'].append(line) # add rule to rule list
        print('Rule {}: {},{},{}').format(count, line[0], line[1], line[2])
        machine['transition'][line[0]][line[1]] = line[2] # add transitions to transition function as they are read in
        count += 1
    f.close()
    return machine

def resetDFA(machine):
    # simple function just used to reset machine after each string
    machine['current'] = machine['start']

def readStrings(filename, machine):
    f = open(filename, 'r')
    for line in f: # read input strings one at a time
        resetDFA(machine)
        currentString = line.strip()
        print("String: {}").format(currentString)
        start = time.time() # start time
        output = processString(currentString, machine) # check if machine rejects or accepts string
        end = time.time() # end time
        runtime = end - start # calculate runtime for this string
        print(output + "\nRuntime: " + str(1000000*runtime) + " microseconds\n")

def processString(string, machine):
    for i,c in enumerate(string): # iterate through string one character at a time
        if c not in machine['alphabet']: # reject string if it has a character not in alphabet
            return "Rejected"
        elif c not in machine['transition'][machine['current']]: # reject if there is not a rule for the current state and the current input character
            return "Rejected"
        else:
            nextState = machine['transition'][machine['current']][c] # find next state based on transition function
            index = machine['rules'].index([machine['current'], c, nextState]) # calculate rule number
            # print('{},{}=?{}').format(machine['current'],c,nextState)
            print('{},{},{},{},{}').format(i+1, index + 1, machine['current'], c, nextState) # print out iteration, rule #, current state, input char, next state
            machine['current'] = nextState # move machine to next state
    if machine['current'] in machine['accept']: # if machine ends on accept state return accept
        return 'Accepted'
    else: # if machine ends on a state that is not accept, reject the string
        return 'Rejected'

args = sys.argv[1:] # command line arguments
dfa = readDFA(args[0]) # read in DFA from inputted file
print('\n')
readStrings(args[1], dfa) # process each string from given file with the read in DFA
