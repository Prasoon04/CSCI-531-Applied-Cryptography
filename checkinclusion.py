import json
from operator import index
from xml.sax import make_parser
import sys
import hashlib

class CheckInclusion:
    def __init__(self, Root, Leaves, input) -> None:

        print(self.Inclusion(Root, Leaves, input))
    


    def Inclusion(self, Root, Leaves, input)->None:

        input_hash = hashlib.sha256(input.encode('utf-8')).hexdigest()
        if input_hash not in Leaves:
            return 'No'
        else:
            output = self.Check_Merkle(Root, Leaves, input_hash)
        
        if output == 'No':
            return output
        else:
            return ('Yes', output)


    def Check_Merkle(self, root_hash, proofs, input_hash)->None:

        result = []

        while len(proofs) != 1:
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
            for i in range(0, len(proofs), 2):
                if i == len(proofs)-1:
                    curr.append(proofs[i])
                    break
                else:
                    left = proofs[i]
                    right = proofs[i+1]
                
                concat = left+right
                
                concathash = hashlib.sha256(concat.encode('utf-8')).hexdigest()
                curr.append(concathash)
            proofs = curr
        
        if proofs[0] == root_hash:
            return result
        else:
            return 'No'



input = sys.argv[1]
temp = open('file1.json')
treenodes = json.load(temp)
treeRoot = treenodes[0]
treeLeaves = treenodes[1:]

CheckInclusion(treeRoot, treeLeaves, input)
