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
    thelist = sorted(list(set(thelist)))
    for el in thelist:
        rStr = rStr+el
    return rStr

def findNext(anNfa, cSt, sChars, theES):#finds the paths to the next states from one state
    rDict = {} #this will be returned
    for letter in sChars: #for each character in the alphabet
        rDict[letter] = []#create an empty list in the dictionary
        for mini in cSt:#for each substate in the current state
            if letter in anNfa[mini]:#if the character is in the substate's dictionary
                rDict[letter] = list(set(rDict[letter]+anNfa[mini][letter]))#add the state it leads to
        for tiny in rDict[letter]:#add all of the epsilon sets
            rDict[letter] = list(set(rDict[letter]+ theES[tiny]))
        if rDict[letter] == []:#delete empty dictionaries
            del rDict[letter]
    return rDict#return the dictionary

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

dfa = {}#initialize the dfa graph
todoStates = [esets[startState]]#put the start state at the top of the stack to search from
doneStates = []#states that have already been searched from
while len(todoStates) > 0:#while there are still unsearched states
    nowState = todoStates.pop()#get the top state from the stack
    if l2s(nowState) not in doneStates:
        doneStates.append(l2s(nowState))#assign it as completed
    temp = findNext(theNfa, nowState, inputChars, esets)#find the states it leads to
    for k, v in temp.items():
        if l2s(v) not in doneStates:
            todoStates.append(v)#add these states
    dfa[l2s(nowState)] = temp #set the path dictionary as the value of the current state
nf = open("dfa_of_"+sys.argv[1], 'w')
nf.write(name+'\n')
nf.write(",".join(inputChars)+'\n')
#newz = [l2s(x) for x in doneStates]
nf.write(",".join(doneStates)+'\n')
nf.write(l2s(esets[startState])+'\n')
finalaccept = []
for somestate in doneStates:
    for initials in acceptingStates:
        if initials in somestate:
            finalaccept.append(somestate)
            break
nf.write(",".join(finalaccept)+'\n')
for k, v in dfa.items():
    for l, w in v.items():
        nf.write(k+','+l+','+l2s(w)+'\n')
nf.close()
