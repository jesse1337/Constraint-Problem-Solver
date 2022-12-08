# Constraint-Problem-Solver

This repository contains the python file with algorithms to solve constraint satisfaction problems.
It uses backtrack search and forward search (in this case, AC-3) algorithms to solve these problems.

CSP text files are problems with constraints and are given in the format:

3:3
1 * X0 + 0 > 0
1 * X1 + 0 > 0
-1 * X0 + 3 < X1

'3:3' means that there are 2 variables, each with 3 possible values in its domain.
The rest are constraints for those variables.
