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

    stack =[]
    json_stack = []

    def fileOut(self)->None:
        file = open('merkle.tree.txt', 'w+')
        for line in self.stack:
            file.write(line+"\n")
        self.Inorder(self.root)
        with open('example.json','w') as outfile:
            json.dump(self.json_stack, outfile)

    def Inorder(self,node)->None:
        if node != None:
            self.Inorder(node.left)
            self.json_stack.append(["Hash Value: "+str(node.val), "Input: "+str(node.data)])
            self.Inorder(node.right)


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
