#!/usr/bin/env python3

import hashlib
import sys
from typing import Tuple

class Node:
    def __init__(self, left, right, val, data) -> None:
        self.left = left
        self.right = right
        self.val = val
        self.data = data

class CheckConsistency:
    def __init__(self, list1, list2) -> None:

        tree1 = self.Tree(list1)
        print('******************************'*4)
        tree2 = self.Tree(list2)
        index = 0
        while index < len(list1):
            if list1[index] != list2[index]:
                break
            index += 1
        if index < len(list1):
            print(self.outNo())
            return

        parent = self.list_parent(tree2)
        leftNodes = self.list_left(tree2)
        rightNodes = self.list_right(tree2)
        
        present = False

        if tree1.val in parent:
            present = True
        print(self.calculateConsistency(present, leftNodes, rightNodes, tree1, tree2))
    
    def outNo(self)->None:
        return 'No'
    
    def calculateConsistency(self,present, leftNodes, rightNodes, tree1, tree2)->None:
        output = self.consistency(present, leftNodes, rightNodes, tree1, tree2)
        return ("Yes", output)

    def consistency(self, flag, leftN, rightN, tree1, tree2)->None:
        tree2nodes = self.levelOrder(tree2)
        result = []
        if flag:
            out = []
            hashcomb = ''
            leftchild = tree1.val
            while hashcomb != tree2.val:
                if leftchild in leftN:
                    i = leftN.index(leftchild)
                    rightchild = rightN[i]
                    out.append(rightchild)
                    break

                concat = leftchild+rightchild
                hashcomb = self.hash(concat)
                leftchild = concat
            
            result.append(tree1.val)
            result+=out
            result.append(tree2.val)
            return result
        
        else:
            tree1lc = tree1.left.val
            tree1rc = tree1.right.val
            tree1rcsibling = tree2nodes[tree2nodes.index(tree1rc)+1]
            out = []
            out.append(tree1lc)
            out.append(tree1rc)
            out.append(tree1rcsibling)
            tree1rc_concat = tree1rc+tree1rcsibling
            hashcomb = ''
            leftchild = tree1lc
            rightchild = self.hash(tree1rc_concat)
            while hashcomb != tree2.val:
                concat = leftchild+rightchild
                hashcomb = self.hash(concat)
                leftchild = concat
                if leftchild in leftN:
                    i = leftN.index(leftchild)
                    rightchild = rightN[i]
                    out.append(rightchild)
                    break
            
            result.append(tree1.val)
            result+=out
            result.append(tree2.val)
            return result

    def levelOrder(self, tree2)->None:
        q = []
        nodes = []
        q.append(tree2)
        while len(q)>0:
            node = q.pop(0)
            nodes.append(node.val)

            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
        return nodes

    def list_left(self, root)->None:
        result = []
        q = []
        q.append(root)

        while len(q)>0:
            node = q.pop(0)

            if node.left is not None:
                result.append(node.left.val)
                q.append(node.left)
            
            if node.right is not None:
                q.append(node.right)
        return result

    def list_right(self, root)->None:
        result = []
        q = []
        q.append(root)

        while len(q)>0:
            node = q.pop(0)

            if node.left is not None:
                q.append(node.left)
            
            if node.right is not None:
                result.append(node.right.val)
                q.append(node.right)
        return result

    def list_parent(self, root)->None:
        result = []
        q = []
        q.append(root)

        while len(q) > 0:
            node = q.pop(0)
            if node.left and node.right:
                result.append(node.val)
                q.append(node.left)
                q.append(node.right)
        return result

    
    def Tree(self, inputs)->None:
        leaves = []
        for element in inputs:
            hashed = self.hash(element)
            leaves.append(Node(None,None,hashed,element))
        self.root = self.buildTree(leaves)
        self.printTree(self.root)
        self.fileOut()
        return self.root
    
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

    stack = []

    def fileOut(self)->None:
        file = open('merkle.trees.txt', 'w+')
        for line in self.stack:
            file.write(line+"\n")
        file.write("\n")
        file.close()

    def printTree(self, node)->None:
        self.Treeout(node, 0)

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

if __name__ == "__main__":     
    input_string = sys.argv
    char = input_string.index(',')
    list1 =input_string[1:char]
    list2 = input_string[char+1:]
    merkle = CheckConsistency(list1, list2)


