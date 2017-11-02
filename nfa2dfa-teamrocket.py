import sys

def makeESetList(anNfa, astate, thelist):
    retList = thelist#this will be the returned list
    if '~' in anNfa[astate]:#if there is an epsilon
        for nstate in anNfa[astate]['~']:#for each state reached by epsilon
            if nstate not in retList:#if it is not already in the list
                retList.append(nstate)#add it to the list
                retList = makeESetList(anNfa, nstate, list(set(thelist+retList)))#check for its epsilons
    return retList #return the list

def l2s(thelist):#simple function to make lists into strings
    rStr = ''
    thelist = list(set(thelist))
    for el in thelist:
        rStr = rStr+'@@@'+el
    return rStr

def findNext(anNfa, cSt, sChars, theES):
    rDict = {}
    for letter in sChars:
        rDict[letter] = []
        for mini in cSt:
            if letter in anNfa[mini]:
                rDict[letter] = list(set(rDict[letter]+anNfa[mini][letter]))
        for tiny in rDict[letter]:
            rDict[letter] = list(set(rDict[letter]+ theES[tiny]))
    return rDict

theNfa = {}#create dictionary to represent NFA
f = open(sys.argv[1], "r") #open file
name = f.readline().strip()+"_2_DFA" #set the name of the DFA
inputChars = f.readline().strip().split(',') #get list of input characters
stateListNfa = f.readline().strip().split(',')#get list of states
startState = f.readline().strip()#get start state
acceptingStates = f.readline().strip().split(',')#get accepting states
for state in stateListNfa:
    theNfa[state] = {}#initializes all state keys to have values of empty dictionaries
for line in f:
    line = line.strip().split(',')
    if line[1] not in theNfa[line[0]]:#if the input char is not in the state yet
        theNfa[line[0]][line[1]] = [line[2]]#create a list for its resultant state
    else:
        theNfa[line[0]][line[1]].append(line[2])#or append the possible result to the list

esets = {} # initialize dictionary for the epsilon set things
for state in stateListNfa:
    strtList = [state] # all esets contain the state itself
    esets[state] = makeESetList(theNfa, state, strtList)#map a state to the set it can reach

dfa = {}
todoStates = [esets[startState]]
doneStates = []
while len(todoStates) > 0:
    nowState = todoStates.pop()
    doneStates.append(nowState)
    temp = findNext(theNfa, nowState, inputChars, esets)
    for k, v in temp.items():
        if v not in doneStates:
            todoStates.append(v)
    dfa[l2s(nowState)] = temp

print dfa
