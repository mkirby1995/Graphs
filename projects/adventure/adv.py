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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"
# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
player_2 = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# Work Space
################################################################################

def bfs(start):
    q = Queue()
    q.enqueue([start])
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited:
            if '?' in list(traversial_graph[v].values()):
                return path
            visited.add(v)
            for neighbor in list(traversial_graph[v].values()):
                new_path = list(path)
                new_path.append(neighbor)
                q.enqueue(new_path)
    return None

def reverse_dict(dictionary):
    return {v: k for k, v in dictionary.items()}

# Create a dictionary of rooms
traversial_graph = {
    player_2.current_room.id:
        dict.fromkeys(player_2.current_room.get_exits(), '?')
}

done = False

while done == False:
    current = player_2.current_room

    # Pick a random unexplored direction
    possible_moves = [i for i in traversial_graph[current.id]\
                        if traversial_graph[current.id][i] == '?']

    if len(possible_moves) > 0:
        move = random.choice(possible_moves)
        # Travel to that room and log the direction
        previous_room_id = current.id
        player_2.travel(move)
        current = player_2.current_room
        traversial_graph[previous_room_id][move] = current.id
        traversal_path.append(move)

        # If the room isn't in traversial_graph
        if current.id not in list(traversial_graph.keys()):
            # Add room to the traversial_graph
            traversial_graph[current.id] = dict.fromkeys(
                                               current.get_exits(), '?')

        if move == 'n':
            traversial_graph[current.id]['s'] = previous_room_id
        elif move == 's':
            traversial_graph[current.id]['n'] = previous_room_id
        elif move == 'e':
            traversial_graph[current.id]['w'] = previous_room_id
        elif move == 'w':
            traversial_graph[current.id]['e'] = previous_room_id

    else:
        # find the shortest path to a room with an unexplored path
        short_path = bfs(current.id)
        if short_path == None:
            break
            
        directed_path = []
        for i in range(len(short_path) + 1):
            if i + 1 < len(short_path):
                direction = reverse_dict(
                    traversial_graph[short_path[i]])[short_path[i+1]]
                directed_path.append(direction)

        # Travel along that path and log the direction
        for direction in directed_path:
            previous_room_id = current.id
            player_2.travel(direction)
            traversal_path.append(direction)


    # Iteration
    values = []
    for adj_dict in list(traversial_graph.values()):
        for i in list(adj_dict.values()):
            values.append(i)

    if '?' in values or len(traversial_graph) != len(room_graph):
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
