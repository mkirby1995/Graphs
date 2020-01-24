from room import Room
from player import Player
from world import World

import sys

import random
from ast import literal_eval
from util import Graph, Queue, Stack
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"
verbosity = int(sys.argv[1])
# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# Work Space
################################################################################
# Lets try again

def shortest_path(start):
    "Let's find the shortest path to an unknown"
    q = Queue()
    q.enqueue([start])
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]

        if v not in visited:
            #print(f"Let's check room {v}")
            if '?' in list(traversial_graph[v].values()):
                #print(f"Found one! It's at room {v}")
                #print(path)
                return path
            #print(f"None here {traversial_graph[v]}")
            visited.add(v)
            for neighbor in list(traversial_graph[v].values()):
                new_path = list(path)
                new_path.append(neighbor)
                q.enqueue(new_path)
    return None


def reverse_dict(dictionary):
    return {v: k for k, v in dictionary.items()}


def unexplored_directions(dictionary):
    possible = []
    for i in dictionary:
        if dictionary[i] == '?':
            possible.append(i)
    return possible


# Create a dictionary of rooms
traversial_graph = {
    player.current_room.id: dict.fromkeys(player.current_room.get_exits(), '?')
}
if verbosity >= 7:
    print('Initializing traversial graph', traversial_graph)

done = False
iter = 0

while done == False:
    # Pick a random unexplored direction
    possible_moves = unexplored_directions(traversial_graph[player.current_room.id])
    if len(possible_moves) > 0:
        move = random.choice(possible_moves)

        #possible_moves = list(traversial_graph[player.current_room.id].keys())
        if verbosity >= 6:
            print(f"We're in room {player.current_room.id}. We can go {possible_moves}")
            print(f"Let's go {move}")

        # Travel to that room and log the direction
        previous_room_id = player.current_room.id
        player.travel(move)
        traversial_graph[previous_room_id][move] = player.current_room.id
        if verbosity >= 3:
            print(f"If we go {move} in room {previous_room_id} we end up in {player.current_room.id}")
        traversal_path.append(move)
        if verbosity >= 2:
            print(f"Let's add that to our path {traversal_path}")
            print(f"Updating traversial_graph {traversial_graph}")

        # If the room isn't in traversial_graph
        if player.current_room.id not in list(traversial_graph.keys()):
            if verbosity >= 6:
                print(f"Looks like {player.current_room.id} hasn't been visited yet.")
            # Add room to the traversial_graph
            traversial_graph[player.current_room.id] = dict.fromkeys(player.current_room.get_exits(), '?')
            if verbosity >= 3:
                print(f"Let's add it to our traversial graph {traversial_graph}")

        if move == 'n':
            traversial_graph[player.current_room.id]['s'] = previous_room_id
            if verbosity >= 7:
                print(f"If we go s in room {player.current_room.id} we end up in {previous_room_id}")
                print(f"Updating traversial_graph {traversial_graph}")
        elif move == 's':
            traversial_graph[player.current_room.id]['n'] = previous_room_id
            if verbosity >= 7:
                print(f"If we go n in room {player.current_room.id} we end up in {previous_room_id}")
                print(f"Updating traversial_graph {traversial_graph}")
        elif move == 'e':
            traversial_graph[player.current_room.id]['w'] = previous_room_id
            if verbosity >= 7:
                print(f"If we go w in room {player.current_room.id} we end up in {previous_room_id}")
                print(f"Updating traversial_graph {traversial_graph}")
        elif move == 'w':
            traversial_graph[player.current_room.id]['e'] = previous_room_id
            if verbosity >= 7:
                print(f"If we go e in room {player.current_room.id} we end up in {previous_room_id}")
                print(f"Updating traversial_graph {traversial_graph}")

    else:
        #while '?' in list(traversial_graph[player.current_room.id].values()) == False:
        if verbosity  >= 6:
            print(f"Looks like we know where all the paths out of this room go. {traversial_graph[player.current_room.id]}")
            print("Looks like there are still some unknown paths out there")
        # find the shortest path to a room with an unexplored path
        short_path = shortest_path(player.current_room.id)
        if short_path == None:
            if verbosity  >= 2:
                print("We've found all the unknowns")
            break
        if verbosity >= 5:
            print(f"Looks like the closest unknown path is in room {short_path[-1]}")
        if short_path:
            if verbosity >= 5:
                print(f'The shortest path from {short_path[0]} to {short_path[-1]} is {short_path}')
            directed_path = []
            for i in range(len(short_path) + 1):
                if i + 1 < len(short_path):
                    #print(f"To get from {short_path[i]} to {short_path[i + 1]}")
                    direction = reverse_dict(traversial_graph[short_path[i]])[short_path[i+1]]
                    #print(f"We need to go {direction}")
                    #print('Path', traversal_path)
                    #print('Graph', traversial_graph)
                    directed_path.append(direction)

            # Travel along that path and log the direction
            for direction in directed_path:
                if verbosity >= 10:
                    print(direction)
                previous_room_id = player.current_room.id
                player.travel(direction)
                if verbosity >= 3:
                    print(f"If we go {direction} in room {previous_room_id} we end up in {player.current_room.id}")
                traversal_path.append(direction)
                if verbosity >= 3:
                    print(f"Let's add that to our path {traversal_path}")


    # Iteration
    values = []
    for adj_dict in list(traversial_graph.values()):
        for i in list(adj_dict.values()):
            values.append(i)
    iter += 1

    if '?' in values or len(traversial_graph) != len(room_graph):
        if verbosity >= 10:
            print("Looks like there are still some unknown paths out there")
        done = False
    else:
        done = True






################################################################################


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
"""
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
"""
