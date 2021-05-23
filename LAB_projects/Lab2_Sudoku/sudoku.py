#!/usr/bin/env python3

import argparse
import itertools
import math
import sys

import math  


from utils import save_dimacs_cnf, solve
import time

def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("board", help="A string encoding the Sudoku board, with all rows concatenated,"
                                      " and 0s where no number has been placed yet.")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Do not print any output.')
    parser.add_argument('-c', '--count', action='store_true',
                        help='Count the number of solutions.')
    return parser.parse_args(argv)


def print_solution(solution):
    """ Print a (hopefully solved) Sudoku board represented as a list of 81 integers in visual form. """
    print(f'Solution: {"".join(map(str, solution))}')
    print('Solution in board form:')
    Board(solution).print()

def trans(pos_x,pos_y,value,board_size):
    #From 3D matrix to 1D array ("positions")
    return board_size*board_size*pos_x + board_size*pos_y + value

def compute_solution(sat_assignment, variables, size):
    solution = []
    # TODO: Map the SAT assignment back into a Sudoku solution
    #Select the True elements of the output of the sat solver.
    for x in range(0,size):
        for y in range(0,size):       
            for v_aux in range(1,10):
                sat_bool_variable_index=trans(x,y,v_aux,size)
                if(sat_assignment[sat_bool_variable_index]):
                    solution.append(v_aux)
    return solution


def generate_theory(board, verbose):
    """ Generate the propositional theory that corresponds to the given board. """
    size = board.size()
    clauses = []
    variables = {}
    n_clauses = 0
    n_clauses_acc = 0
    #Clauses 0 -- our values
    for x, y in board.all_coordinates():
        value = board.value(x, y)
        if value>0:
            clauses.append([trans(x,y,value,size)]) #Take into consideration the values that we have 'last clause'


    n_clauses = len(clauses)
    if (verbose):
        print("Zero clause", n_clauses)
    n_clauses_acc = n_clauses_acc + n_clauses


    #First Clause -- at least one value
    for x, y in board.all_coordinates():
        value = board.value(x,y)
        if value == 0:
            values = []
            for v_aux in range(1,10):
                values.append(trans(x,y,v_aux,size))
            #clauses.append(values)


    n_clauses = len(clauses)
    if (verbose):
        print("First clause" , n_clauses)
    n_clauses_acc = n_clauses_acc + n_clauses

    #Second Clause -- at most one value
    for x, y in board.all_coordinates():
        value = board.value(x,y)
        for v in range(1,10):
            for v_p in range(v + 1,10):
                clauses.append([-trans(x,y,v,size),-trans(x,y,v_p,size)])


    n_clauses = len(clauses)-n_clauses_acc
    if (verbose):
        print("Second clause" , n_clauses)
    n_clauses_acc = n_clauses_acc + n_clauses


    
    #Third Clause rows --all numbers in  rows
    for x, y in board.all_coordinates():
        value = y + 1
        values = []
        for y_ in range(0,9):
            values.append(trans(x,y_,value,size))
        clauses.append(values)


    n_clauses = len(clauses)-n_clauses_acc
    if (verbose):
        print("Third clause" , n_clauses)
    n_clauses_acc = n_clauses_acc + n_clauses
    #Fourth Clause columns -- all numbers in columns
    for x, y in board.all_coordinates():
        value = x + 1
        values = []
        for x_ in range(0,9):
            values.append(trans(x_,y,value,size))
        clauses.append(values)


    n_clauses = len(clauses)-n_clauses_acc
    if (verbose):
        print("Fourth clause" , n_clauses)
    n_clauses_acc = n_clauses_acc + n_clauses


    #Fifth Clause Blocks -- all number in block
    sqrt_size = int(math.sqrt(board.size()))
    for x in range(0,sqrt_size):
        for y in range(0,sqrt_size):
            for value in range(1,10):
                values = []
                for xx in range(0,sqrt_size):
                    for yy in range(0,sqrt_size):
                        values.append(trans(x*sqrt_size + xx,y*sqrt_size + yy,value,size))
                clauses.append(values)


    n_clauses = len(clauses)-n_clauses_acc
    if (verbose):
        print("Fifth clause" , n_clauses)
    variables = list(range(1, size*size*size+1))
    #print(clauses)


    return clauses, variables, size


def count_number_solutions(board, verbose=False):

    clauses, variables, size = generate_theory(board, verbose)
    solution = solve_sat_problem(clauses, "theory.cnf", size, variables, verbose)
    count = 0
    new_clauses = []
    t = time.time()
    #Iterate until no solutions are found
    while(solution != None):
        count = count + 1
        for i in range(1,size*size*size+1):
            #print(solution[i])
            if solution[i]:
                new_clauses.append(-i)
            else:
                new_clauses.append(i)
        clauses.append(new_clauses)# Save all new clauses to he basic clauses
        solution = solve_sat_problem(clauses, "theory.cnf", size, variables, verbose)
        new_clauses = []

    #print(new_clauses)
    print(f'Number of solutions: {count}')# Print counts
    elapsed = time.time() - t
    print(f'Time: {elapsed}')# Time that it took to compute all the solutions
    return None

def find_one_solution(board, verbose=False):
    clauses, variables, size = generate_theory(board, verbose)
    return solve_sat_problem(clauses, "theory.cnf", size, variables, verbose)


def solve_sat_problem(clauses, filename, size, variables, verbose):
    save_dimacs_cnf(variables, clauses, filename, verbose)
    result, sat_assignment = solve(filename, verbose)
    if result != "SAT":
        if verbose:
            print("The given board is not solvable")
        return None
    solution = compute_solution(sat_assignment, variables, size)
    if verbose:
        print_solution(solution)
    return sat_assignment


class Board(object):
    """ A Sudoku board of size 9x9, possibly with some pre-filled values. """
    def __init__(self, string):
        """ Create a Board object from a single-string representation with 81 chars in the .[1-9]
         range, where a char '.' means that the position is empty, and a digit in [1-9] means that
         the position is pre-filled with that value. """
        size = math.sqrt(len(string))
        if not size.is_integer():
            raise RuntimeError(f'The specified board has length {len(string)} and does not seem to be square')
        self.data = [0 if x == '.' else int(x) for x in string]
        self.size_ = int(size)

    def size(self):
        """ Return the size of the board, e.g. 9 if the board is a 9x9 board. """
        return self.size_

    def value(self, x, y):
        """ Return the number at row x and column y, or a zero if no number is initially assigned to
         that position. """
        return self.data[x*self.size_ + y]

    def all_coordinates(self):
        """ Return all possible coordinates in the board. """
        return ((x, y) for x, y in itertools.product(range(self.size_), repeat=2))

    def print(self):
        """ Print the board in "matrix" form. """
        assert self.size_ == 9
        for i in range(self.size_):
            base = i * self.size_
            row = self.data[base:base + 3] + ['|'] + self.data[base + 3:base + 6] + ['|'] + self.data[base + 6:base + 9]
            print(" ".join(map(str, row)))
            if (i + 1) % 3 == 0:
                print("")  # Just an empty line


def main(argv):
    args = parse_arguments(argv)
    board = Board(args.board)

    if args.count:
        count_number_solutions(board, verbose=False)
    else:
        find_one_solution(board, verbose=not args.quiet)


if __name__ == "__main__":
    main(sys.argv[1:])
