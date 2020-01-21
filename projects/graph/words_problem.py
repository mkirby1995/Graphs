"""
Given two words (begin_word and end_word), and a dictionary's word list,
return the shortest transformation sequence from begin_word to end_word,
such that:

Only one letter can be changed at a time.
Each transformed word must exist in the word list.
Note that begin_word is not a transformed word.

Note:
Return None if there is no such transformation sequence.
All words contain only lowercase alphabetic characters.
You may assume no duplicates in the word list.
You may assume begin_word and end_word are non-empty and are not the same.

Sample:
begin_word = "hit"
end_word = "cog"
return: ['hit', 'hot', 'cot', 'cog']
begin_word = "sail"
end_word = "boat"
['sail', 'bail', 'boil', 'boll', 'bolt', 'boat']
beginWord = "hungry"
endWord = "happy"
None
"""
from graph import Graph


with open('words.txt', 'r') as file:
    word_list = [line.lower().rstrip() for line in file]

def isEditDistanceOne(s1, s2):

    # Find lengths of given strings
    m = len(s1)
    n = len(s2)

    # If difference between lengths is more than 1,
    # then strings can't be at one distance
    if abs(m - n) > 1:
        return False

    count = 0    # Count of isEditDistanceOne

    i = 0
    j = 0
    while i < m and j < n:
        # If current characters dont match
        if s1[i] != s2[j]:
            if count == 1:
                return False

            # If length of one string is
            # more, then only possible edit
            # is to remove a character
            if m > n:
                i+=1
            elif m < n:
                j+=1
            else:    # If lengths of both strings is same
                i+=1
                j+=1

            # Increment count of edits
            count+=1

        else:    # if current characters match
            i+=1
            j+=1

    # if last character is extra in any string
    if i < m or j < n:
        count+=1

    return count == 1


def shortest_sequence(word_1, word_2):
    graph = Graph()
    short_list = []

    for i in word_list:
        # Filter out words that dont have the same first letter
        # as starting words
        if i[0] == word_1[0] or i[0] == word_2[0]:
            if len(word_1) == len(i):
                short_list.append(i)


    # Create vertices
    for i in short_list:
        graph.add_vertex(i)

    # For each word in short list
    for i in short_list:
        # for each vertex
        for j in list(graph.vertices.keys()):
            #if edit distance is one
            if isEditDistanceOne(i, j):
                #connect the two vertices
                graph.add_edge(i, j)

    return graph.bfs(word_1, word_2)

print(shortest_sequence('sail', 'boat'))
