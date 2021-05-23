#!/usr/bin/env python3

import argparse
import sys
import sys, os, time
import re, subprocess

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


def write_instance(game, output, instance):
    # our definition of x and y is opposite from the one in sokobangame
    # there x is row and y is column, for us it follows the cartesian axes
    # this means we also have to turn upside down our idea of increasing y

    with open(output, 'w') as file:
        file.write("(define (problem " + instance + ") \n")
        file.write("(:domain sokoban) \n")
        file.write('(:objects ')
        for y in range(game.h):
            file.write("y" + str(y) + " ")
        file.write(" - y ")
        for x in range(game.w):
            file.write("x" + str(x) + " ")
        file.write(" - x) \n")
        file.write("(:init \n")

        for y in range(game.h):
            for x in range(game.w):
                if (game.is_wall(y, x)):
                    file.write("(iswall " + "x" + str(x) + " " + "y" + str(y) + ") \n")
                if (game.is_box(y, x)):
                    file.write("(hasbox " + "x" + str(x) + " " + "y" + str(y) + ") \n")
                if (y, x) == game.player:
                    file.write("(at " + "x" + str(x) + " " + "y" + str(y) + ")\n")

        for y in range(game.h):
            if y != (game.h - 1):
                file.write("(decy  " + "y" + str(y) + " " + "y" + str(y + 1) + ") \n")
                file.write("(incy  " + "y" + str(y + 1) + " " + "y" + str(y) + ") \n")
            file.write("(samey " + "y" + str(y) + " " + "y" + str(y) + ") \n")

        for x in range(game.w):
            if x != (game.w - 1):
                file.write("(incx  " + "x" + str(x) + " " + "x" + str(x + 1) + ") \n")
                file.write("(decx  " + "x" + str(x + 1) + " " + "x" + str(x) + ") \n")
            file.write("(samex " + "x" + str(x) + " " + "x" + str(x) + ") \n")

        file.write(")\n (:goal (and")

        for (y, x) in game.goals:
            file.write("(hasbox " + "x" + str(x) + " " + "y" + str(y) + ") \n")
        file.write(")))")


def main(argv):
    args = parse_arguments(argv)
    print(args)# We select the heuristic from the cmd line


    with open('test_sol_'+str(args.i)+'.txt' , 'w') as file_test:#File were the olution of the test is stored
        number_succes =[]
        for i in range(1, 51):#51
            file_name = 'level' + str(i) + '.sok' #Select problem
            # print(file)
            with open('benchmarks/sasquatch/' + file_name, 'r') as file:
                board = SokobanGame(file.read().rstrip('\n'))

            write_instance(board, 'probl.pddl', str(i))

            cmd = 'D/fast-downward.py --overall-time-limit 60 domain.pddl probl.pddl   --search "astar(ipdb())" '

            out_cm = os.popen(cmd).read() #Execute and save the output of the command line



            if "search exit code: 0" in out_cm: #If solution found
                #print(out_cm)
                result = re.search('Plan length:(.*)step', out_cm).group(1) #Find path length
                print(result)
                rr = 'Plan length:' + result + 'Solution found'
                print("Plan found for " + file_name + "!")
                print("---------------------------------------")
                file_test.write("Plan found for " + file_name + "\n")
                file_test.write(rr + "\n");
                file_test.write("--------------------------------------- \n")
                number_succes.append(i)
            else:
                print("No plan found in the specified time for " + file_name)
                print("---------------------------------------")
                file_test.write("No plan found in the specified time for " + file_name + "\n")
                file_test.write("---------------------------------------\n")
                
        print('The planner was successful for {}/50 levels in less than 1 minute.'.format(len(number_succes)))



if __name__ == "__main__":
    main(sys.argv[1:])
