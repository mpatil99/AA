import random


def readCNF(file):
    """ This function parses CNF from a simplified version of the DIMACS format
    http://www.satcompetition.org/2009/format-benchmarks2009.html
    """
    numvars = 0
    numclauses = 0
    clauses = []
    variables = []
    with open(file) as text:
        for line in text:
            if line[0] == 'c':
                pass
            elif line[0] == 'p':
                line = line.split()
                numvars = line[2]
                numclauses = line[3]
            else:
                clause = line.split()[:-1]
                clause = [int(var) for var in clause ]
                # for var in clause:
                #     variables.append(abs(var))
                clauses.append(clause)
    return numvars, numclauses, clauses#, set(variables)

def count_literals(formula):
    """ This function counts the literals in the given formula"""
    count = {}
    for clause in formula:
        for literal in clause:
            if literal in count:
                count[literal] += 1
            else:
                count[literal] = 1
    return count


def propogate(formula, unit):
    """
    Apply the unit to the formula.
    Remove clauses in which the unit exists
    Update clauses in which -unit exists
    """
    updated = []
    for clause in formula:
        if unit in clause: continue
        if -unit in clause:
            clause = [c for c in clause if c != -unit]
            if len(clause) == 0: return -1
            updated.append(clause)
        else:
            updated.append(clause)
    return updated

def assignPureLiterals(formula):
    count = count_literals(formula)
    assignment = []
    pures = [x for x in count.keys() if -x not in count]
    for pure in pures:
        formula = propogate(formula, pure)
    assignment += pures
    return formula, assignment

def assignUnitClauses(formula):
    count = count_literals(formula)
    assignment = []
    units = [u for u in formula if len(u) == 1]

    #The assignment of a unit could result in more unit clauses being created
    while len(units) > 0:
        unit = units[0]
        formula = propogate(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        units = [u for u in formula if len(u) == 1]

    return formula, assignment

def evaluateCNF(formula, assignment):
    print("Formula", formula)
    formula, pureassignemnt = assignPureLiterals(formula)
    formula, unitassignment = assignUnitClauses(formula)
    print("Formula Cleaned", formula)
    assignment = assignment + pureassignemnt + unitassignment
    if formula == -1:
        return False
    if not formula:
        return assignment

    randomLiteral = random.choice(list(count_literals(formula).keys()))

    #Implemenation of Backtracking
    soln = evaluateCNF(propogate(formula,randomLiteral), assignment + [randomLiteral])
    if not soln:
        soln = evaluateCNF(propogate(formula,-randomLiteral), assignment + [-randomLiteral])
    return soln


def main():
    numvars, numclauses, clauses = readCNF("cnf.txt")
    solution = evaluateCNF(clauses, [])
    if( solution):
        print(solution)
        solution += [x for x in list(count_literals(formula).keys())) if x not in solution and -x not in solution]
        solution.sort(key=lambda x: abs(x))
        print( 'The given CNF formula is satisfiable with the follwing inputs: ')
        print( ' ' + ' '.join([str(x) for x in solution]))
    else:
        print( 'The given CNF formula is not satisfiable :(')

if __name__ == '__main__':
    main()
