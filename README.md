# Tree
Tree data structure.

## Tree.py
The Tree.py file contains an abstract base class representing a tree structure.

## BinaryTree.py
The BinaryTree.py file contains both a BinaryTree class and a LinkedBinaryTree class. The BinaryTree class is an Abstract base class representing a binary tree structure and inherits the base Tree class.

The LinkedBinaryTree class is linked representation of a binary tree structure. This class inherits the BinaryTree class.

## Tree Traversal Algorithms

### Preorder Traversal
In a preorder traversal of a tree T, the root of T is visited first and then the subtrees rooted at its children are traversed recursively. If the tree is ordered, then
the subtrees are traversed according to the order of the children

### Postorder Traversal
Another important tree traversal algorithm is the postorder traversal. In some
sense, this algorithm can be viewed as the opposite of the preorder traversal, because it recursively traverses the subtrees rooted at the children of the root first, and
then visits the root (hence, the name “postorder”).

### Inorder Traversal of a Binary Tree
During an inorder traversal, we visit a position between the recursive traversals of its left and right subtrees. The inorder traversal of a binary tree T can be
informally viewed as visiting the nodes of T “from left to right.” Indeed, for every
position p, the inorder traversal visits p after all the positions in the left subtree of
p and before all the positions in the right subtree of p