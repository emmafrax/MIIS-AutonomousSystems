#!/usr/bin/env python3

import argparse
import sys
import sys, os, time


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("-i", help="Path to the file with the Sokoban instance.")
    return parser.parse_args(argv)


class SokobanGame(object):
    """ A Sokoban Game. """
    def __init__(self, string):
        """ Create a Sokoban game object from a string representation such as the one defined in
            http://sokobano.de/wiki/index.php?title=Level_format
        """
        lines = string.split('\n')
        self.h, self.w = len(lines), max(len(x) for x in lines)
        self.player = None
        self.walls = set()
        self.boxes = set()
        self.goals = set()
        for i, line in enumerate(lines, 0):
            for j, char in enumerate(line, 0):
                if char == '#':  # Wall
                    self.walls.add((i, j))
                elif char == '@':  # Player
                    assert self.player is None
                    self.player = (i, j)
                elif char == '+':  # Player on goal square
                    assert self.player is None
                    self.player = (i, j)
                    self.goals.add((i, j))
                elif char == '$':  # Box
                    self.boxes.add((i, j))
                elif char == '*':  # Box on goal square
                    self.boxes.add((i, j))
                    self.goals.add((i, j))
                elif char == '.':  # Goal square
                    self.goals.add((i, j))
                elif char == ' ':  # Space
                    pass  # No need to do anything
                else:
                    raise ValueError(f'Unknown character "{char}"')

    def is_wall(self, x, y):
        """ Whether the given coordinate is a wall. """
        return (x, y) in self.walls

    def is_box(self, x, y):
        """ Whether the given coordinate has a box. """
        return (x, y) in self.boxes

    def is_goal(self, x, y):
        """ Whether the given coordinate is a goal location. """
        return (x, y) in self.goals


    
def write_instance(game,output,instance):

    #our definition of x and y is opposite from the one in sokobangame
    #there x is row and y is column, for us it follows the cartesian axes
    #this means we also have to turn upside down our idea of increasing y
    
    with open(output, 'w') as file:
        file.write("(define (problem " + instance + ") \n")
        file.write("(:domain sokoban) \n")
        file.write('(:objects ')
        for y in range(game.h):
            file.write("y"+str(y)+ " ")
        file.write(" - y ")
        for x in range(game.w):
            file.write("x"+str(x)+ " ")
        file.write(" - x) \n")
        file.write("(:init \n")
        
        
        for y in range(game.h):
            for x in range(game.w):
                if(game.is_wall(y, x)):
                    file.write("(iswall "+ "x"+str(x) + " " + "y"+str(y) + ") \n")
                if(game.is_box(y, x)):
                    file.write("(hasbox " + "x"+str(x) + " " + "y"+str(y) + ") \n")
                if (y,x) == game.player:
                    file.write("(at " + "x"+str(x) + " " + "y"+str(y) + ")\n")
    
        for y in range(game.h):
            if y != (game.h-1):
                file.write("(decy  "+ "y"+str(y) + " " + "y"+str(y+1) + ") \n")
                file.write("(incy  "+ "y"+ str(y+1) + " "+ "y"+str(y) + ") \n")
            file.write("(samey " + "y"+str(y) + " "+ "y"+str(y) + ") \n")            

            
        for x in range(game.w):
            if x!= (game.w-1):
                file.write("(incx  "+ "x"+str(x) + " "+ "x"+str(x+1) + ") \n")
                file.write("(decx  "+ "x"+str(x+1) + " "+ "x"+str(x) + ") \n")
            file.write("(samex " + "x"+str(x) + " "+ "x"+str(x) + ") \n")

        
        file.write(")\n (:goal (and")
        
        for (y,x) in game.goals:
             file.write("(hasbox " + "x"+str(x) + " "+ "y"+str(y) + ") \n")
        file.write(")))")


def translate_plan(file):
    
    with open(file, 'r') as f:
        for line in f:
            part = line.split()
            if ((part[0] == "(moveup") or (part[0] == "(moveboxup")):
                print('move up')
            if ((part[0] == "(movedown") or (part[0] == "(moveboxdown")):
                print('move down')
            if ((part[0] == "(moveright") or (part[0] == "(moveboxright")):
                print('move right')
            if ((part[0] == "(moveleft") or (part[0] == "(moveboxleft")):
                print('move left')
            if part[0] == "(teleport":
                print('teleport to position ({},{})'.format(part[2],part[4]))
            
    

def main(argv):
    args = parse_arguments(argv)
    with open(args.i, 'r') as file:
        board = SokobanGame(file.read().rstrip('\n'))

    # TODO - Some of the things that you need to do:
    #  1. (Previously) Have a domain.pddl file somewhere in disk that represents the Sokoban actions and predicates.
    #  2. Generate an instance.pddl file from the given board, and save it to disk.
    #  3. Invoke some classical planner to solve the generated instance.
    #  3. Check the output and print the plan into the screen in some readable form.
    write_instance(board,'probl.pddl','one')

    #command
    cmd = 'python D/fast-downward.py --alias seq-sat-lama-2011 --plan-file solution.txt --overall-time-limit 60  domain.pddl probl.pddl '

    # invoke planner
    output = os.system(cmd)
                
        
    #Check if it has a solution + translate
    if os.path.isfile("solution.txt"):
        print("Plan found for " + args.i + "!")
        filepath = 'solution.txt'
        translate_plan(filepath)
        
        #remove
        os.remove(filepath)
        print("---------------------------------------")

    else:
        print("No plan found in the specified time for " + args.i)
        print("---------------------------------------")

if __name__ == "__main__":
    main(sys.argv[1:])
