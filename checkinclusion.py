import json
from operator import index
from xml.sax import make_parser
import sys
import hashlib


class Node:
    def __init__(self, val, data) -> None:
        self.left = None
        self.right = None
        self.val = val
        self.data = data

class CheckInclusion:
    def __init__(self, inorder, preorder) -> None:

        global mp
        #print('********************')
        #print(inorder)
        
        for i in range(len(inorder)):
            mp[inorder[i][1]] = i
        
        #print(mp)
        
        self.root = self.buildTree(inorder, preorder, 0, len(inorder)-1)

    def buildTree(self, ino, pre, start, end )->Node:

        global preIndex, mp

        if start > end:
            return None
        
        curr = pre[preIndex]
        preIndex += 1
        tempNode = Node(curr[0], curr[1])

        if start == end:
            return tempNode

        InIndex = mp[curr[1]]
        #print(InIndex)
        tempNode.left = self.buildTree(ino, pre, start, InIndex-1)
        tempNode.right = self.buildTree(ino,pre, InIndex+1, end)

        return tempNode        

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
        #print(self.leaves)

    def Inclusion(self, input)->None:

        input_hash = hashlib.sha256(input.encode('utf-8')).hexdigest()
        if input_hash not in self.leaves:
            return 'No'
        else:
            output = self.Check_Merkle(self.root.val, self.leaves, input_hash)
        
        if output == 'No':
            return output
        else:
            return ('Yes', output)


    def Check_Merkle(self, root_hash, proofs, input_hash)->None:

        leaves = proofs
        result = []

        while len(leaves) != 1:
            index_val = proofs.index(input_hash)
            if index_val % 2 == 0:
                result.append(proofs[index_val+1])
                concat = input_hash + proofs[index_val+1]
                input_hash = hashlib.sha256(concat.encode('utf-8')).hexdigest()
                  
            else:
                result.append(proofs[index_val-1])
                concat = proofs[index_val-1] + input_hash
                input_hash = hashlib.sha256(concat.encode('utf-8')).hexdigest()
            
            curr = []
            for i in range(0, len(leaves), 2):
                if i == len(leaves)-1:
                    curr.append(leaves[i])
                    break
                else:
                    left = leaves[i]
                    right = leaves[i+1]
                
                concat = left+right
                
                concathash = hashlib.sha256(concat.encode('utf-8')).hexdigest()
                curr.append(concathash)
            leaves = curr
            proofs = curr
        
        if leaves[0] == root_hash:
            return result
        else:
            return 'No'

    def printTree(self) -> None:
        self.Treeout(self.root, 0)

    def Treeout(self, node, order)->None:
        if node != None:            
            print(" "*order+"Hash Value: "+str(node.val))
            print(" "*order+"Input: "+str(node.data))
            print("")
            order += 5
            self.Treeout(node.left, order+5)
            self.Treeout(node.right, order+5)


input = sys.argv[1]
temp = open('file1.json')
treenodes = json.load(temp)
inorder = open('inorder.json')
preorder = open('preorder.json')
inorder_traversal = json.load(inorder)
preorder_traversal = json.load(preorder)
mp = {}
preIndex = 0
#for i in range(len(inorder_traversal)):
#    print(inorder_traversal[i], i)
Tree = CheckInclusion(inorder_traversal, preorder_traversal)
Tree.printTree()
Tree.leafnodes()
print('**********')
print(Tree.Inclusion(input))
#print(Tree.Inclusion('richard'))


#print(root.val)
#print(root.data)