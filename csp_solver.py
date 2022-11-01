
#------------------------------------------------------------#------------------------------------------------------------

def importCSP(filename):
    """Creates the CSP from text file."""
    my_file = open(filename, "r")
    data = my_file.read()
    dataList = data.split("\n")
    my_file.close()

    print("Domain is: ", getDomain(dataList))
    print("Constraints are: ", getConstraint(dataList))

def getDomain(dataList):
    #Creates dictionary for domains. "X" : Domain of X
    domLine = dataList[0].split(':')
    domLen = len(domLine)
    domDic = {}

    x0dom = []
    i = 0
    while i < (int(domLine[0])):
        x0dom.append(i)
        i+=1

    x1dom = []
    i = 0
    while i < (int(domLine[1])):
        x1dom.append(i)
        i+=1
    
    domDic = {"X0": x0dom, "X1": x1dom
    }

    if domLen > 2:
        xndom = []
        i = 0
        while i < (int(domLine[2])):
            xndom.append(i)
            i+=1
        domDic["X_N"] = xndom
    
    return domDic
def getConstraint(dataList):
    #Creates a dictionary for constraints. "constraint" : # of variables needed for constraint
    conArray = dataList[1:] 
    for line in conArray:
        getConRel(line)


    #create and set values to CSP
    # csp = CSP()
    # csp.vars = max(conDic.keys())
    # csp.domains = domDic
    # csp.neighbors = None
    # csp.constraints = conArray
    # csp.assignment = {}
#------------------------------------------------------------#------------------------------------------------------------
#  get relevant variables and expression CONSTRAINT
def variablesNeededForConstraint(constraint):
    """Checks # of different variables needed for a constraint"""
    xInd = constraint.split()
    xArr=[]
    for items in xInd:
        if 'X' in items:
            xArr.append(items)
    for items in xArr:
        if xArr.count(items) > 1:
            xArr.remove(items)

    return len(xArr)


def getConRel(constraintStr):
    constraint = constraintStr.split()
    constraintVarNum = []
    #set stuff
    firstCoeff = constraint[0]
    firstVar = constraint[2]
    firstVarNum = int(firstVar[1])
    addNum = constraint[4]
    exp = constraint[5]
    secondVar = constraint[6]
    secondVarNum = None
    constraintVarNum.append(firstVarNum)

    #"Rel is either ==, !=, <=, >=, <, or > and Var_Or_Integer is either a variable or an integer."
    relDic = {
        '==' : int.__eq__,
        '!=' : int.__ne__,
        '<=' : int.__le__,
        '>-' : int.__ge__,
        '<' : int.__lt__,
        '>' : int.__gt__
    }

    if secondVar[0] == 'X':
        secondVarNum = int(secondVar[1])
        constraintVarNum.append(secondVarNum)
        ###check THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        rel = lambda firstX, secX: relDic[exp](firstCoeff * firstX + addNum , secX)
    else:
        #then there is only one X, and last num is just an int
        conInt = int(constraint[6])
        rel = lambda firstX: relDic[exp](firstCoeff * firstX + addNum, conInt)
    
    return constraintVarNum, rel



#10/31 did constraintRel and CSP arguments --> not sure about assignment still

#------------------------------------------------------------#------------------------------------------------------------
class CSP():
    def __init__(self, numVar, domains, neighbors, constraints, assignment):

        numVar = 0
        domains = []
        constraints = []
        assignment = assignment

    def assign(var, val, assignment):
        """Assigns a value to a variable."""
        assignment[var] = val


    def numConflicts(self, var, val, assignment):
        """Returns the number of conflict that a variable-value assignment has."""
        def conflict(secondVar):
            secondVal = assignment.get(secondVar, None)
            return secondVal != None and not self.constraints(var, val, secondVar, secondVal)

        
        return count_if(conflict, self.neighbors[var])

#------------------------------------------------------------#------------------------------------------------------------
def numOfLegalVal(csp, var, assignment):
    """Determines the number of legal values that a variable can have."""
    if csp.currDomains:
        return len(csp.currDomains[var])
    else:
        retVal = count_if(lambda val: csp.nconflicts(var, val, assignment) == 0, csp.domains[var])
        return retVal     

def count_if(cond, list):
    """Counts how many times a list satisfies a condition."""
    return sum(1 for item in list if cond(item))

 
#------------------------------------------------------------#------------------------------------------------------------

def backtracking_search(csp): 
    """Main backtracking search that will be used with CSP."""
    #returns a solution, or failure
    return Backtrack({}, csp)

def Backtrack(assignment, csp):
    """Recursive part of the backtrack search."""
    #returns a solution, failure

    #if assignment list (list with assigned vars is = to # of vars, we done)
    if (assignment) == len(csp.vars):
        return assignment

    #if not, then assign it!!!
    var = select_unassigned_variable(csp)
    for val in order_domain_values(var, assignment, csp):
        csp.assign(var, val, assignment)
        sol = backtracking_search(assignment, csp)
        
        if sol is not None:
            return sol
        else:
            print("NO SOLUTION")
            return None





def select_unassigned_variable(csp):
    """Returns an unassigned variable based off MRV or degree heuristic."""
    #implements MRV/MCV, and then degree heuristic for tiebreakers

    unassigned = []
    #add all unassigned variables to unassigned[]
    for variable in csp.vars:
        if variable not in csp.assignment:
            unassigned.append(variable)





    MRVar = None
    numLegalVal = 1000000 #we want to choose var with least legal val, so start big
    for unvar in unassigned:
        legalComp = numLegalVal(csp, unvar, csp.assignment)
        if legalComp < numLegalVal:
            numLegalVal = legalComp
            MRVar = unvar
        #if tie, use degree heuristic
        elif legalComp == numLegalVal:
            numConflicts = csp.numConflicts(csp, unvar, unvar.keys(), unassigned)
        if numConflicts > conf:
            conf = numConflicts
            MRVar = unvar
        #if still tie, choose first unassigned var
        else:
            return unassigned[0]
    return MRVar

def order_domain_values(var, assignment, csp):
    """Orders the values in the domain based on LCV."""
    #implements least constrained value to order the domain
    #whichever domain has the least constraints eg. most values, then it is put first
    if csp.currDomains:
        domain = csp.currDomain[var]
    else:
        domain = csp.domains[var][:]
    
    conf = 0
    for val in domain:
        conf = csp.numConflicts(var, val, assignment)
        domain.sort()
    
    while domain:
        yield domain.pop()
         

#------------------------------------------------------------#------------------------------------------------------------

def main():
    data = importCSP("problem_filename.txt")
    #csp = CSP()




    return
main()
