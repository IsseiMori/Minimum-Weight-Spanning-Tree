import sys
import os
from collections import defaultdict 

class Edge:

  def __init__(self, u, v, w, index):
    self.u = u;
    self.v = v;
    self.w = w;
    self.index = index;

  def __eq__(self, other):
    return self.w == other.w

  def __lt__(self, other):
    return self.w < other.w

  def __ne__(self, other):
      return not self.__eq__(other)

  def __le__(self, other):
      return self.__lt__(other) or self.__eq__(other)

  def __gt__(self, other):
      return not self.__le__(other)

  def __ge__(self, other):
      return not self.__lt__(other)



class Graph:

  # Initializer is called at instance creation time
  def __init__(self, v_num):
    self.v_num = v_num
    self.edges = [] # Main list of edges
    self.graph = defaultdict(list)  # List of edges to detect cycle

  # Add an edge u to v, one way
  def add_edge(self, e):
    self.edges.append(e)
    self.graph[e.u].append(e.v) 

  # Recursion function to find the parent (top of the tree)
  def find_parent(self, parent_list, i):
    if parent_list[i] == -1:
      return i;
    else:
      return self.find_parent(parent_list, parent_list[i])

  def union(self, parent_list, x, y):
    parent_list[self.find_parent(parent_list, x)] = self.find_parent(parent_list, y)

  def is_cyclic(self):
    parent_list = [-1] * (self.v_num + 1) # index 1~n 

    for i in self.graph: 
      for j in self.graph[i]: 
          x = self.find_parent(parent_list, i)  
          y = self.find_parent(parent_list, j) 
          if x == y: 
            return True
          self.union(parent_list,x,y) 

  def will_be_cyclic(self, e):
    self.graph[e.u].append(e.v)
    cycle = self.is_cyclic()
    self.graph[e.u].remove(e.v)
    if cycle:
      return True
    else:
      return False

# ----------- Read file and construct a graph ----------

if (len(sys.argv) < 3):
  sys.exit()

infile_path = sys.argv[1]
outfile_path = sys.argv[2]

infile = open(infile_path,"r")

infile_lines = infile.readlines()

v_num = int(infile_lines[0])
e_num = int(infile_lines[1])


edge_list = []

for i in range(0, e_num):

  nums = infile_lines[2+i].split()

  if(len(nums) != 3):
    print("invalid file format")
    sys.exit()

  edge_list.append(Edge(int(nums[0]), int(nums[1]), int(nums[2]), i+1))

infile.close()

# ----------- Construct a minimum weight spanning tree using Kruskal's algorithm ----------

graph = Graph(v_num)

edge_list.sort()

e_count = 0;
while e_count < v_num and len(edge_list) != 0:
  e = edge_list.pop(0)
  if(not graph.will_be_cyclic(e)):
    graph.add_edge(e)

# ----------- Output to a file ----------

outfile = open(outfile_path,"w+")

graph.edges.sort()

total_weight = 0;
for e in graph.edges:
  outfile.write("{:>4}".format(e.index) + ": (" + str(e.u) + ", " + str(e.v) + ") " + "{:.1f}".format(e.w) + "\n")
  total_weight = total_weight + e.w

outfile.write("Total Weight = " + "{:.2f}\n".format(total_weight))
outfile.close()