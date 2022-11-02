import sys
from itertools import permutations
#------------------------------------------------------------#------------------------------------------------------------

def importCSP(filename):
    """Creates the CSP from text file."""
    my_file = open(filename)
    data = my_file.read()
    dataList = data.split("\n")
    my_file.close()

    return dataList
    
    print("Constraints are: ", getConstraint(dataList))

def getDomain(dataList):
    return dataList[0].split(':')
    #Creates dictionary for domains. "X" : Domain of X
    # domLine = dataList[0].split(':')
    # domLen = len(domLine)
    # domDic = {}

    # x0dom = []
    # i = 0
    # while i < (int(domLine[0])):
    #     x0dom.append(i)
    #     i+=1

    # x1dom = []
    # i = 0
    # while i < (int(domLine[1])):
    #     x1dom.append(i)
    #     i+=1
    
    # domDic = {"X0": x0dom, "X1": x1dom
    # }

    # if domLen > 2:
    #     xndom = []
    #     i = 0
    #     while i < (int(domLine[2])):
    #         xndom.append(i)
    #         i+=1
    #     domDic["X_N"] = xndom
    
    # return domDic


def getConstraint(dataList):
    #Creates a dictionary for constraints. "constraint" : # of variables needed for constraint
    conArray = dataList[1:] 
    for line in conArray:
        getConRel(line)
    return conArray


def getConRel(constraintStr):
    constraint = constraintStr.split()
    constraintVarNum = []
    #set stuff
    firstCoeff = int(constraint[0])
    firstVar = constraint[2]
    firstVarNum = int(firstVar[1])
    addNum = int(constraint[4])
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
        secondVarNum = int(secondVar[1:])
        constraintVarNum.append(secondVarNum)
        ###check THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        rel = lambda firstX, secX: relDic[exp](firstCoeff * firstX + addNum , secX)
    else:
        #then there is only one X, and last num is just an int
        conInt = int(constraint[6])
        rel = lambda firstX: relDic[exp](firstCoeff * firstX + addNum, conInt)
    
    return constraintVarNum, rel


    #create and set values to CSP
    # csp = CSP()
    # csp.vars = max(conDic.keys())
    # csp.domains = domDic
    # csp.neighbors = None
    # csp.constraints = conArray
#     # csp.assignment = {}
# #------------------------------------------------------------#------------------------------------------------------------
# #  get relevant variables and expression CONSTRAINT
# def variablesNeededForConstraint(constraint):
#     """Checks # of different variables needed for a constraint"""
#     xInd = constraint.split()
#     xArr=[]
#     for items in xInd:
#         if 'X' in items:
#             xArr.append(items)
#     for items in xArr:
#         if xArr.count(items) > 1:
#             xArr.remove(items)

#     return len(xArr)



#10/31 did constraintRel and CSP arguments --> not sure about assignment still



#------------------------------------------------------------#------------------------------------------------------------
class CSP():
    def __init__(self, file, forwardCheck):

        self.numVar = 0
        self.domains = []
        self.constraints = []
        self.forwardCheck = forwardCheck
        self.assignment = []

        dataList = importCSP(file)

        for item in getDomain(dataList):
            self.domains.append(list(range(int(item))))
        
        for constraintLines in dataList[1:]:
            self.constraints.append(getConRel(constraintLines))

        for con in self.constraints:
            limit = max(con[0])
            if self.numVar < limit:
                self.numVar = limit + 1

        dom = self.domains[-1]
        for i in range(len(self.domains), self.numVar):
            self.domains.append(dom)

    def assign(var, val, assignment):
        """Assigns a value to a variable."""
        assignment[var] = val


    def numConflicts(self, fX, sX):
        """Returns the number of conflict that a variable-value assignment has."""
        conflict = None
        count = 0
        #if there is no conflict (constraint violation), then we loop each constraint
        while conflict is None and count < len(self.constraints):
            #count each conflict found; set conflict so it doesn't loop more than it needs to
            if fX in self.constraints[count][0] and sX in self.constraints[count][0]: 
                conflict = self.constraints[count]
            count += 1
        
        return conflict


    def ac_3(self):
        tempDom = self.domains
        for con in self.constraints:
            if len(con[0]) == 1:
                for x in tempDom[con[0][0]]:
                    if not con[1](x):
                        tempDom[con[0][0]].remove(x)
        
        queue = list(permutations(list(range(self.numVar)), 2))
        while len(queue) != 0:
            fX, sX = queue.pop(0)
            ordDom = self.revise(fX, sX, tempDom)
            if ordDom:
                if len(tempDom[fX]) == 0:
                    return False, tempDom
                for k in [i for i in range(self.numVar) if i != fX]:
                    queue.append((fX, k))

    def revise(self, fX, sX, tempDom):    #domain copy is passed by reference
            ordDom = False
            # look for a constraint between xi and xj
            confxsx = self.numConflicts(fX, sX)
            if confxsx is None:
                return False
            # iterate over each value in the domain of xi, ex [0,1,2,3,4]
            for x in tempDom[fX]:
                # if there is no value x in domain Di of xj that allows (x,y) to satisfy the constraint between xi and xj
                done = False
                for y in tempDom[sX]:
                    if confxsx[1](x,y):
                        done = True
                if not done:
                    # delete x from Di
                    tempDom[fX].remove(x)
                    ordDom = True

            return ordDom


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
    print("assignment: ", csp.assignment, "varNum: ", csp.numVar, "domain: ", csp.domains, "constraints: ", csp.constraints)
    return Backtrack(csp.assignment, csp)

def Backtrack(assignment, csp):
    """Recursive part of the backtrack search."""
    #returns a solution, failure
    
    #if assignment list (list with assigned vars is = to # of vars, we done)
    if len(assignment) == csp.numVar:
        return assignment

    #if not, then assign it!!!
    var = select_unassigned_variable(csp)
    for val in order_domain_values(var, assignment, csp):
        csp.assign(var, val, assignment)
        result = Backtrack(assignment, csp)
        
        if result is not None:
            return result
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
    return unassigned[0]




    # MRVar = None
    # numLegalVal = 1000000 #we want to choose var with least legal val, so start big
    # for unvar in unassigned:
    #     legalComp = numLegalVal(csp, unvar, csp.assignment)
    #     if legalComp < numLegalVal:
    #         numLegalVal = legalComp
    #         MRVar = unvar
    #     #if tie, use degree heuristic
    #     elif legalComp == numLegalVal:
    #         numConflicts = csp.numConflicts(csp, unvar, unvar.keys(), unassigned)
    #     if numConflicts > conf:
    #         conf = numConflicts
    #         MRVar = unvar
    #     #if still tie, choose first unassigned var
    #     else:
    #         return unassigned[0]
    # return MRVar

def order_domain_values(var, assignment, csp):
    """Orders the values in the domain based on LCV."""
    # #implements least constrained value to order the domain
    # #whichever domain has the least constraints eg. most values, then it is put first
    # if csp.currDomains:
    #     domain = csp.currDomain[var]
    # else:
    #     domain = csp.domains[var][:]
    
    # conf = 0
    # for val in domain:
    #     conf = csp.numConflicts(var, val, assignment)
    #     domain.sort()
    
    # while domain:
    #     yield domain.pop()
    
    return csp.domain

#------------------------------------------------------------#------------------------------------------------------------
#INFERENCES --> AC-3

def main():
    file = sys.argv[-2]
    forwardCheck = sys.argv[-1]
    if forwardCheck == '1': forwardCheck = True
    if forwardCheck == '0': forwardCheck = False

    csp = CSP(file, forwardCheck)
    print(csp.ac_3())

main()
