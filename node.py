# Binary Tree Code by Greg Hewgill (http://stackoverflow.com/users/893/greg-hewgill)
# Adapted for n-Tree by Bruno (http://stackoverflow.com/users/1774900/bruno)

class Node(object):

    def __init__(self):
        self.name=None
        self.node=[]
        self.col = None
        self.row = None
        self.prevv=None

    def nex(self,child):
        "Gets a node by number"
        return self.node[child]

    def prev(self):
        return self.prevv

    def goto(self, row, col):
        "Gets the node by name"
        for child in range(0,len(self.node)):
            if((self.node[child].row==row) and (self.node[child].col==col)):
                return self.node[child]
    def add(self):
        node1=Node()
        self.node.append(node1)
        node1.prevv=self
        return node1