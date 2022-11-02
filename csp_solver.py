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

def getDomain(dataList):
    return dataList[0].split(':')

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
    return unassigned[0]
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
def ac_3(csp):
        temp = csp.domains
        for cons in csp.constraints:
            if len(cons[0]) == 1:
                for i in temp[cons[0][0]]:
                    if not cons[1](i):
                        temp[cons[0][0]].remove(i)


        queue = list(permutations(list(range(csp.numVar)), 2))
        while len(queue) != 0:
            fX, sX = queue.pop(0)
            ordered = revise(csp,fX, sX, temp)
            if ordered:
                if len(temp[fX]) == 0:
                    return False, temp
                for k in [i for i in range(csp.numVar) if i != fX]:
                    queue.append((fX, k))

        return temp
def revise(csp, fX, sX, temp):
        order = False
        fsCon = csp.numConflicts(sX, fX)
        if fsCon is None:
            return False
        for x in temp[fX]:
            done = False
            for y in temp[fX]:
                if fsCon[1](x,y):
                    done = True
            if not done:
                temp[fX].remove(x)
                order = True

        return order

def main():
    file = sys.argv[-2]
    forwardCheck = sys.argv[-1]
    if forwardCheck == '1': forwardCheck = True
    if forwardCheck == '0': forwardCheck = False

    csp = CSP(file, forwardCheck)
    print("Constraints: ", csp.constraints)
    print("Domains: ", csp.domains)
    print("numVar: ", csp.numVar)
    print(ac_3(csp))

    #11/2/2022
    #did ac-3/inference/forward checking i guess? tomorrow: finish backtrack
main()
