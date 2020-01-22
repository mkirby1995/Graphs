import random
from queue import Queue

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def bft(self, starting_user):
        # Create empty queue and enqueue starting user
        q = Queue()
        q.put(starting_user)

        # Create empty set to store visited users
        visited = set()
        traversal = []

        # While the queue is not empty
        while q.qsize() > 0:
            # Dequeue first user
            u = q.get()

            # If that user has not been visited
            if u not in visited:
                # Mark as visited
                visited.add(u)
                # Do thing
                traversal.append(u)
                # Then add all of its neighbors to the back of the queue
                for friend in self.friendships[u]:
                    q.put(friend)
        return traversal

    def bfs(self, starting_user, destination_user):
        # Create an empthy queue and enqueue the starting vertex
        q = Queue()
        q.put([starting_user])

        # Create and empty set to store visited
        visited = set()

        # While queue is not empty
        while q.qsize() > 0:

            # Dequeue the first vertex
            path = q.get()
            u = path[-1]
            # If that vertex has not been visited
            if u not in visited:
                # If vertex is destination vertex
                if u == destination_user:
                    return path
                    # Do the thing and return
                visited.add(u)
                # Add all of its neighbors to the back of the queue
                # copy path to avoid pass by reference bug
                for friend in self.friendships[u]:
                    new_path = list(path)
                    new_path.append(friend)
                    q.put(new_path)


    def populate_graph(self, num_users, avg_friendships, return_ = False):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        counter_ = 0

        # Add users
        for i in range(num_users):
            self.add_user(str(i))

        # Create friendships
        k = round(random.normalvariate(2, .5))
        for user in self.users:
            for i in range(k - 1 ):
                friend = random.choice(list(self.users.keys()))
                self.add_friendship(user, friend)
                counter_ += 1

        if return_ == True:
            return counter_


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        for user in self.bft(user_id):
            visited[user] = self.bfs(user_id, user)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)

    sg_2 = SocialGraph()
    print("Add friends called:", sg_2.populate_graph(100, 10, return_ = True))

    sg_3 = SocialGraph()
    sg_3.populate_graph(1000, 5)
    connections_2 = sg.get_all_social_paths(1)
    # get a random user
    print((len(sg_3.bft(random.choice(list(sg_3.users.keys())))) / len(sg_3.users)) * 100, "%")
    # divide len(bft) of that user aginst the total number of users
    a = [len(i) for i in list(connections_2.values())]
    print(sum(a) / len(a))
