# buildtree.py
  The program creates a Merkle tree and writes the output into a file “merkle.tree” to present the tree structure in a readable format. The program comprises   of the following:
1.	A Node class with 4 class variables for the Node: left child, right child, Data and the Hash value of that Data.
2.	The Merkle tree class builds a bottom-up tree iteratively
3.	The class also prints and writes the tree. It also generates a file1.JSON file with all the leaf nodes in a list format to be used by checkinclusion.py.

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss1.png)<br>
.\buildtree.py alice bob carlol david<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss2.png)<br>
(For windows: cat alternative) type merkle.tree.txt

# checkinclusion.py
This program takes in the input string and returns whether the string exists in the Merkle tree constructed using buildtree.py along with the intermediate nodes used as proofs to verify the string. The program comprises of the following:
1.	The program takes in the user input and generates a SHA-256 hash of the input and checks if the string is present in the leaf nodes of the Merkle tree. If it is not present, then a No is returned.
2.	If the string is present in the leaf nodes, then the index of input is found in the leaf nodes hash acquired from buildtree.py through file file1.JSON. After finding the index, the sibling of the input is looked for using the index value as the even numbers make the input left node and odd numbers make it right node. The program runs while loop constructing a Merkle tree using the hash value while finding the intermediate nodes using the index of the current node to look for the sibling.<br>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss3.png)<br>
.\checkinclusion.py richard<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss4.png)<br> 
.\checkinclusion.py david
 
# checkconsistency.py
The program takes two lists as input and verifies that they are consistent and return the consistency proofs by showing the intermediate nodes.
1.	The program first builds a tree following the buildtree.py structure.
2.	It then checks if the first input leaf nodes are a subset of the second input leaf nodes. If it is not the case, then a ‘No’ is returned. If it is the case, then we check if the first tree hash is present in the second tree hash:<br>
              a.	 If it is the case, we try to look for the hash of the sibling node in the second tree. We add the hashes of the siblings and generate a hash for the parent and continue this till we reach the second tree root hash. This also gives us all the intermediate proofs hash nodes. We return the proofs node.<br>
              b.	 If it is not the case, we find the left node hash and right node hash of the first tree. We also find the sibling of the right node hash of the first tree in the second tree. The right child of first tree and its sibling in the second tree are combined and hashed  to form the sibling of left node from first tree. After that, the procedure is same above until we reach the root node while grabbing the intermediate nodes as proofs.<br>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss5.png)<br>
.\checkconsistency.py alice bob carlol david , alice bob carlol david eve fred<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss6.png)<br>
(For windows: cat alternative) type merkle.trees.txt<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss7.png)<br>
.\checkconsistency.py alice bob carlol david , alice bob david eve fred<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss8.png)<br>
(For windows: cat alternative) type merkle.trees.txt<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss9.png)<br>
.\checkconsistency.py alice bob carlol david , alice bob carol eve fred davis<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%201/Screenshots/ss10.png)<br> 
(For windows: cat alternative) type merkle.trees.txt
 

