#!/usr/bin/python
#!/usr/bin/env python3


import hashlib
import sys
import json

class Node:
    def __init__(self, left, right,val, data) -> None:
        self.left = left
        self.right = right
        self.val = val
        self.data = data

class MerkleTree:
    def __init__(self, inputs) -> None:
        leaves = []
        for element in inputs:
            hashed = self.hash(element)
            leaves.append(Node(None,None,hashed,element))
        self.root = self.buildTree(leaves)
    
    def buildTree(self, nodes)->Node:
        while len(nodes) != 1:
            curr = []
            for i in range(0, len(nodes), 2):
                if i == len(nodes)-1:
                    curr.append(nodes[i])
                    break
                else:
                    left_node = nodes[i]
                    right_node = nodes[i+1]
                concathash = self.hash(left_node.val + right_node.val)
                ancestor = Node(None, None, concathash, left_node.val+' | '+right_node.val)
                ancestor.left = left_node
                ancestor.right = right_node
                curr.append(ancestor)
            nodes = curr
        return nodes[0]       

    def hash(self, val)->str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    leaves = []
    def leafnodes(self)->None:
        temp = []
        temp.append(self.root)
        while temp:
            curr = temp.pop()
            if curr.left:
                temp.append(curr.left)
            if curr.right:
                temp.append(curr.right)
            elif not curr.left and not curr.right:
                self.leaves.append(curr.val)
        self.leaves.reverse()
    
    def printTree(self)->None:
        self.Treeout(self.root, 0)

    stack =[]

    def fileOut(self)->None:
        file = open('merkle.tree.txt', 'w+')
        for line in self.stack:
            file.write(line+"\n")
        self.leafnodes()
        self.leaves = [self.root.val] + self.leaves
        with open('file1.json', 'w') as leavesfile:
            json.dump(self.leaves, leavesfile)

    def Treeout(self, node, order)->None:
        if node != None:            
            print(" "*order+"Hash Value: "+str(node.val))
            print(" "*order+"Input: "+str(node.data))
            print("")
            self.stack.append(" "*order+"Hash Value: "+str(node.val))
            self.stack.append(" "*order+"Input: "+str(node.data))
            self.stack.append("")
            order += 5
            self.Treeout(node.left, order+5)
            self.Treeout(node.right, order+5) 

input_string = sys.argv
merkle = MerkleTree(input_string[1:])
merkle.printTree()
merkle.fileOut()
