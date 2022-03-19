import hashlib
import sys

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
        
        if len(leaves) % 2 != 0:
            leaves.append(leaves[-1])

        self.root = (self.buildTree(leaves))
        
    def buildTree(self, nodes)->Node:
        
        mid = len(nodes)//2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], self.hash(nodes[0].val+nodes[1].val), nodes[0].data+'|'+nodes[1].data)

        leftnode = self.buildTree(nodes[:mid])
        rightnode = self.buildTree(nodes[mid:])
        value = self.hash(leftnode.val + rightnode.val)
        data = leftnode.data+'|'+rightnode.data
        return Node(leftnode, rightnode, value, data)

    def hash(self, val)->str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    
    def printTree(self)->None:
        self.Treeout(self.root, 0)
    
    def Treeout(self, node, order)->None:
        #file = open('merkle.tree.txt', 'w+')
        if node != None:            
            print(" "*order+"Hash Value: "+str(node.val))
            print(" "*order+"Input: "+str(node.data))
            print("")
            order += 5
            self.Treeout(node.left, order+5)
            self.Treeout(node.right, order+5)
      

input_string = sys.argv
merkle = MerkleTree(input_string[1:])
print(merkle.printTree())
