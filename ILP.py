#!/usr/bin/python

import sys
import math
from gurobipy import *
import time

start_time = time.time()

if len(sys.argv) < 2:
    print('Usage: ILP.py filename')
    quit()

f = open(sys.argv[1])

grid = f.read().split()

n = len(grid[0])
m = 5


# Create our 3-D array of model variables

model = Model('sudoku')

vars = model.addVars(n,n,m, vtype=GRB.BINARY, name='G')


# Fix variables associated with cells whose values are pre-specified

for i in range(n):
    for j in range(n):
        if grid[i][j] != '.':
            v = int(grid[i][j])
            vars[i,j,v].LB = 1

# Each cell must take one value

model.addConstrs((vars.sum(i,j,'*') == 1
                 for i in range(n)
                 for j in range(n)), name='V')

# Each value appears once per row

model.addConstrs((vars.sum(i,'*',v) == 1
                 for i in range(n)
                 for v in range(1,m)), name='R')

model.addConstrs((vars.sum(i,'*',0) == 4
                 for i in range(n)), name='R')

# Each value appears once per column

model.addConstrs((vars.sum('*',j,v) == 1
                 for j in range(n)
                 for v in range(1,m)), name='C')

model.addConstrs((vars.sum('*',j,0) == 4
                 for j in range(n)), name='C')


# Each value appears once per subgrid

#2
model.addConstr(vars[5,1,0] + vars[7,1,0] + vars[6,0,0] + vars[6,2,0] == 3)
model.addConstr(vars[5,1,2] + vars[7,1,2] + vars[6,0,2] + vars[6,2,2] == 1)

#3
model.addConstr(vars[0,2,0] + vars[2,2,0] + vars[1,1,0] + vars[1,3,0] == 3)
model.addConstr(vars[0,2,3] + vars[2,2,3] + vars[1,1,3] + vars[1,3,3] == 1)

#4
model.addConstr(vars[4,3,1] + vars[5,2,1] + vars[5,4,1] == 1)
model.addConstr(vars[4,3,2] + vars[5,2,2] + vars[5,4,2] == 1)

#6
model.addConstr(vars[0,4,2] + vars[0,6,2] + vars[1,5,2] == 1)
model.addConstr(vars[0,4,1] + vars[0,6,1] + vars[1,5,1] == 1)
model.addConstr(vars[0,4,3] + vars[0,6,3] + vars[1,5,3] == 1)

#7
model.addConstr(vars[4,6,3] + vars[3,5,3] + vars[3,7,3] == 1)
model.addConstr(vars[4,6,1] + vars[3,5,1] + vars[3,7,1] == 1)
model.addConstr(vars[4,6,2] + vars[3,5,2] + vars[3,7,2] == 1)

#5
'''
a0 = model.addVar(vtype = GRB.INTEGER)
a1 = model.addVar(vtype = GRB.INTEGER)
a2 = model.addVar(vtype = GRB.INTEGER)
a3 = model.addVar(vtype = GRB.INTEGER)

model.addConstr(sum(v * vars[3,4,v] for v in range(1,m)) == a0)
model.addConstr(sum(v * vars[2,3,v] for v in range(1,m)) == a1)
model.addConstr(sum(v * vars[1,4,v] for v in range(1,m)) == a2)
model.addConstr(sum(v * vars[2,5,v] for v in range(1,m)) == a3)

model.addConstr(a0 + a1 + a2 + a3 == 5)
'''

model.addConstr(vars[3,4,0] + vars[2,3,0] + vars[1,4,0] + vars[2,5,0] == 2)
model.addConstr(vars[3,4,1] + vars[2,3,1] + vars[1,4,1] + vars[2,5,1] == 0)
model.addConstr(vars[3,4,2] + vars[2,3,2] + vars[1,4,2] + vars[2,5,2] == 1)
model.addConstr(vars[3,4,3] + vars[2,3,3] + vars[1,4,3] + vars[2,5,3] == 1)


model.optimize()

model.write('sudoku.lp')

print('')
print('Solution:')
print('')

# Retrieve optimization result

solution = model.getAttr('X', vars)

for i in range(n):
    sol = ''
    for j in range(n):
        for v in range(m):
            if solution[i,j,v] > 0.5:
                sol += str(v)
    print(sol)

print("--- %s seconds ---" % (time.time() - start_time))