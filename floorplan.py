# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:50:00 2020

* file is read and converted to its Unicode int representation
    * the floor plan needs to be rectangular atm (This could be changed in by filling it to rectangular shape in the future)
* all room names are search (identifying them by their enclosing brackets)
* starting from the the the opening brackets position the algorithm select coordinates a Manhattan distance of 1 away
---> this coordinates are then checked if they contain wall elements
---> if so they are removed from this set of coordinates
---> from this new set again the neighbors of each point a Manhattan distance of 1 away are select
...
---> This goes on as long as the area is growing
* all names and wall elements are removed from the floor plan to get the coordinates of all chairs
* The chairs are mapped into the rooms by coordinates
* results are printed

@author: Florian Peter Pribahsnik
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt


def read_file(planfile):
    """
    read floorplan file and convert it into an UTF-8 int representation
        * input  TextIOWrapper
        * output either 2D int array or 1 if planfile dat does not show rectangular pattern
    """
    plan = planfile.readlines()
    plan = [row.rstrip('\n') for row in plan]
    plan = [list(map(ord, line)) for line in plan]

    if len(set([len(line) for line in plan])) == 1:  # check for equal length
        plan = np.array(plan)
    else:
        print('Floor plan lecks rectangular shape.')
        plan = 1
    return plan


def map_room(plan, room, args):
    """
    maps room in plan file.
        * input  plan (2D array) and room dict (must conatin startpoint)
        * output 2D array (array of [x,y] points)
    """
    area = [room['startpoint']]
    search = True

    while search:
        # go from evrey point in every direction
        area_expanded = np.tile(area, (len(DIRECTIONS), 1)) + np.repeat(DIRECTIONS, len(area), axis=0)
        # get unique points
        area_expanded = np.unique(area_expanded, axis=0)
        # delete wall item points
        area_expanded = area_expanded[np.isin(plan[tuple(map(tuple, area_expanded.T))], WALL_ITEMS, invert=True)]

        if len(area) == len(area_expanded):
            break
        area = list(map(tuple, area_expanded))

        # Plot progress
        if args.progress:
            plt.scatter(*zip(*area_expanded))
            plt.gca().set_aspect('equal', adjustable='box')
            plt.show()

    return area_expanded


WALL_ITEMS = np.array(list(map(ord, ['|', '-', '\\', '/', '_', '‾', '+'])))
CHAIR_ITEMS = np.array(list(map(ord, ['W', 'P', 'S', 'C'])))
CHAIR_MARKER = {'W': 'X', 'P': 'D', 'S': '*', 'C': 'v'}
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]


def main(args):
    """ Main method doing all the work :-P"""
    plan = read_file(args.file)

    # Find rooms and their names by '(' and ')' and set their starting point
    name_start = np.argwhere(plan == ord('('))
    name_end = np.argwhere(plan == ord(')'))

    rooms = {''.join(list(map(chr, plan[name_start[i][0], name_start[i][1]+1:name_end[i][1]]))): {'startpoint': tuple(name_start[i])} for i in range(len(name_start))}

    # map rooms
    for room in rooms:
        rooms[room]['area'] = map_room(plan, rooms[room], args)
        if args.plot:
            plt.scatter(*zip(*rooms[room]['area']), marker='s')
            plt.annotate(room, rooms[room]['startpoint'], rotation=90)

    # get chair positions
    chair_pos = np.copy(plan)
    # remove wall items
    np.place(chair_pos, np.isin(plan, WALL_ITEMS), [ord(' ')])
    # remove room names
    for i, _ in enumerate(name_start):
        chair_pos[name_start[i][0], name_start[i][1]:name_end[i][1]+1] = ord(' ')

    # map chairs in room
    for chairtype in CHAIR_ITEMS:
        for room in rooms:
            rooms[room][chr(chairtype)] = rooms[room]['area'][(rooms[room]['area'][:, None] == np.argwhere(plan == chairtype)).all(-1).any(-1)]
            if args.plot and rooms[room][chr(chairtype)].size != 0:
                plt.scatter(*zip(*rooms[room][chr(chairtype)]), marker=CHAIR_MARKER[chr(chairtype)], color='w')

    # Write output
    print('total:')
    print(', '.join(chairtype+': '+str(len(np.concatenate([rooms[room][chairtype] for room in rooms]))) for chairtype in list(map(chr, CHAIR_ITEMS))))

    for room in sorted(rooms.keys()):
        print(room+':')
        print(', '.join([chairtype+': '+str(len(rooms[room][chairtype])) for chairtype in list(map(chr, CHAIR_ITEMS))]))

    if args.plot:
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apartment And Chair Delivery Limited.\nChair counting tool')
    parser.add_argument('file', type=argparse.FileType('r'), help='File with the floorplan to process')
    parser.add_argument('--plot', dest='plot', action='store_true', help='if set plots map from file')
    parser.add_argument('--progress', dest='progress', action='store_true', help='if set plot room search progress. ')
    main(parser.parse_args())
