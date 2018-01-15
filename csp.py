from constraint import *
import time
import sys
import math

def func(a, b, c, d, e, f, g, h):
    array = [0, 0, 0, 0, 0]
    list = [a,b,c,d,e,f,g,h]
    for ele in list:
        array[ele] += 1
    if array[0] != 4:
        return False
    return array[1] == 1 and array[2] ==1 and array[3] == 1 and array[4] == 1

def s(a,b,c):
    return a*n*m + b*m + c

start_time = time.time()

if len(sys.argv) < 2:
    print('Usage: csp.py filename')
    quit()

f = open(sys.argv[1])

grid = f.read().split()

n = len(grid[0])
m = 5
print (n)

solver = BacktrackingSolver()
problem = Problem(solver)
problem.addVariables(range(320), range(2))

for i in range(n):
    for j in range(n):
        problem.addConstraint(ExactSumConstraint(1), [i * n * m + j * m + v for v in range(5)])
        if grid[i][j] != '.':
            v = int(grid[i][j])
            problem.addConstraint(ExactSumConstraint(1), [i*n*m + j*m + v])

for i in range(n):
    problem.addConstraint(ExactSumConstraint(4), [i*n*m+j*m+0 for j in range(n)])
    problem.addConstraint(ExactSumConstraint(1), [i * n * m + j * m + 1 for j in range(n)])
    problem.addConstraint(ExactSumConstraint(1), [i * n * m + j * m + 2 for j in range(n)])
    problem.addConstraint(ExactSumConstraint(1), [i * n * m + j * m + 3 for j in range(n)])
    problem.addConstraint(ExactSumConstraint(1), [i * n * m + j * m + 4 for j in range(n)])


for i in range(n):
    problem.addConstraint(ExactSumConstraint(4), [j*n*m+j*m+0 for j in range(n)])
    problem.addConstraint(ExactSumConstraint(1), [j * n * m + i * m + 1 for j in range(n)])
    problem.addConstraint(ExactSumConstraint(1), [j * n * m + i * m + 2 for j in range(n)])
    problem.addConstraint(ExactSumConstraint(1), [j * n * m + i * m + 3 for j in range(n)])
    problem.addConstraint(ExactSumConstraint(1), [j * n * m + i * m + 4 for j in range(n)])

problem.addConstraint(ExactSumConstraint(3), [s(5,1,0), s(7,1,0), s(6,0,0), s(6,2,0)])
problem.addConstraint(ExactSumConstraint(1), [s(5,1,2), s(7,1,2), s(6,0,2), s(6,2,2)])

problem.addConstraint(ExactSumConstraint(3), [s(0,2,0), s(2,2,0), s(1,1,0), s(1,3,0)])
problem.addConstraint(ExactSumConstraint(1), [s(0,2,3), s(2,2,3), s(1,1,3), s(1,3,3)])

problem.addConstraint(ExactSumConstraint(1), [s(4,3,1), s(5,2,1), s(5,4,1)])
problem.addConstraint(ExactSumConstraint(1), [s(4,3,2), s(5,2,2), s(5,4,2)])

problem.addConstraint(ExactSumConstraint(1), [s(0,4,2), s(0,6,2), s(1,5,2)])
problem.addConstraint(ExactSumConstraint(1), [s(0,4,1), s(0,6,1), s(1,5,1)])
problem.addConstraint(ExactSumConstraint(1), [s(0,4,3), s(0,6,3), s(1,5,3)])

problem.addConstraint(ExactSumConstraint(1), [s(4,6,3), s(3,5,3), s(3,7,3)])
problem.addConstraint(ExactSumConstraint(1), [s(4,6,2), s(3,5,2), s(3,7,2)])
problem.addConstraint(ExactSumConstraint(1), [s(4,6,1), s(3,5,1), s(3,7,1)])

problem.addConstraint(ExactSumConstraint(1), [s(3,4,3), s(2,3,3), s(1,4,3), s(2,5,3)])
problem.addConstraint(ExactSumConstraint(1), [s(3,4,2), s(2,3,2), s(1,4,2), s(2,5,2)])
#problem.addConstraint(ExactSumConstraint(0), [s(3,4,4), s(2,3,4), s(1,4,4), s(2,5,4)])
problem.addConstraint(ExactSumConstraint(2), [s(3,4,0), s(2,3,0), s(1,4,0), s(2,5,0)])


dict = problem.getSolution()
if dict == None:
    print None
for i in range(n):
    sol = ''
    for j in range(n):
        for v in range(m):
            index = i*n*m + j*m + v
            if dict[index] == 1:
                sol += str(v)
                break
    print sol

print("--- %s seconds ---" % (time.time() - start_time))