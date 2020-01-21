

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)


class Graph:


    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}


    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()


    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("That vertex does not exist.")


    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]


    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Create an empty queue and enqueue starting vertex ID
        q = Queue()
        q.enqueue(starting_vertex)

        # Create an empty set to store visited verticies
        visited = set()
        order = []

        # While the queue is not empty
        while q.size() > 0:
            # Dequeue the first vertex
            v = q.dequeue()
            # If that vertex has not been visited
            if v not in visited:
                # Mark it as visited
                #print(v)
                order.append(v)
                visited.add(v)
                # Then add all of its neighbors to the back of the queue
                for neighbor in self.vertices[v]:
                    q.enqueue(neighbor)
        return order 


    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Create an empty Stack and push starting vertex ID
        stack = Stack()
        stack.push(starting_vertex)

        # Create an empty set to store visited verticies
        visited = set()

        # While the stack is not empty
        while stack.size() > 0:
            # Pop the first vertex
            v = stack.pop()
            # If that vertex has not been visited
            if v not in visited:
                # Mark it as visited
                print(v)
                visited.add(v)
                # Then add all of its neighbors to the top of the stack
                for neighbor in self.vertices[v]:
                    stack.push(neighbor)


    def dft_recursive(self, starting_vertex, visited = None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()
        visited.add(starting_vertex)
        print(starting_vertex)
        for child_vert in self.vertices[starting_vertex]:
            if child_vert not in visited:
                self.dft_recursive(child_vert, visited)


    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create an empty queue and enqueue starting vertex ID
        q = Queue()
        # Enqueue a list to use as a path
        q.enqueue([starting_vertex])

        # Create an empty set to store visited verticies
        visited = set()

        # While the queue is not empty
        while q.size() > 0:
            # Dequeue the first vertex
            path = q.dequeue()
            v = path[-1]
            # If that vertex has not been visited
            if v not in visited:
                if v == destination_vertex:
                    # Do the thing
                    return path
                visited.add(v)
                # Then add all of its neighbors to the back of the queue
                for neighbor in self.vertices[v]:
                    # Copy path to avoid pass by refference bug
                    new_path  = list(path)
                    new_path.append(neighbor)
                    q.enqueue(new_path)


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Create an empty Stack and push starting vertex ID
        stack = Stack()
        # Push a list to use as a path
        stack.push([starting_vertex])

        # Create an empty set to store visited verticies
        visited = set()

        # While the stack is not empty
        while stack.size() > 0:
            # Pop the first vertex
            path = stack.pop()
            v = path[-1]
            # If that vertex has not been visited
            if v not in visited:
                if v == destination_vertex:
                    # Do the thing
                    return path
                visited.add(v)
                # Then add all of its neighbors to the top of the stack
                for neighbor in self.vertices[v]:
                    # Copy path to avoid pass by refference bug
                    new_path  = list(path)
                    new_path.append(neighbor)
                    stack.push(new_path)


    def dfs_recursive(self, starting_vertex, destination_vertex,
                      visited = None, path = None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()
        if path is None:
            path = []
        visited.add(starting_vertex)
        path = path + [starting_vertex]
        if starting_vertex == destination_vertex:
            return path
        for child_vert in self.vertices[starting_vertex]:
            if child_vert not in visited:
                new_path = self.dfs_recursive(child_vert, destination_vertex,
                 visited, path)
                if new_path:
                    return new_path
        return None
