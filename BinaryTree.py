from Tree import Tree

class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure."""
    
    #------------additional abstract methods-----------
    def left(self, p):
        """Return a Position representing p's left child.
        
        Return None if p does not have a left child.
        """
        raise NotImplementedError('must be implemented by subclass')
    
    def right(self, p):
        """Return a Position representing p's right child.
        
        Return None if p does not have a right child.
        """
        raise NotImplementedError('must be implemented by subclass')
    
    #-----------concrete methods implementing in this class-----------
    def sibling(self, p):
        """Return a Position representing p's sibling (or None if no sibling.)"""
        parent = self.parent(p)
        if parent is None:          # p must be the root
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)       # possibly None
            else:
                return self.left(parent)        # possibly None
    
    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)
    
    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p
                
    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.left(p) is not None:        # if let child exists, traverse its subtree
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p                 # visit p between its subtrees
        if self.right(p) is not None:       # if right child exists, traverse its subtree
            for other in self._subtree_inorder(self.right(p)):
                yield other
    
    # override inherited version to make inorder the default
    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.inorder()       # make inorder the default
        
            
class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""
    
    class _Node:        # Lightweight nonpublic class for storing a node.
        __slots__ = '_element', '_parent', '_left', '_right'
        def __init__(self, element, parent, left, right):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            
    class Position(BinaryTree.Position):
        """An abstraction representing the location of a single element."""
        
        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node
            
        def element(self):
            """Return the element stored at this Position."""
            return self._node._element
        
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type.')
        if p._container is not self:
            raise ValueError('p does not belong to this container.')
        if p._node._parent is p._node:      #convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node
    
    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None
    
    #----------binary tree constructor---------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0
        
    #-------------public accessors---------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size
    
    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)
    
    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)"""
        node = self._validate(p)
        return self._make_position(node._parent)
    
    def left(self, p):
        """Return the Position of p's left child (or None if not left child)."""
        node = self._validate(p)
        return self._make_position(node._left)
    
    def left(self, p):
        """Return the Position of p's right child (or None if not left child)."""
        node = self._validate(p)
        return self._make_position(node._right)
    
    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:      # left child exists
            count += 1
        if node._right is not None:      # right child exists
            count += 1
            
    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.
        
        Raise ValueError if tree nonempty.
        """
        if self._root is not None: raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)
    
    def __add_left(self, p, e):
        """Create a new left child for Position p, storing element e.
        
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None: raise ValueError('Left child exists.')
        self._size += 1
        node._left = self._Node(e, node)            # node is its parent
        return self._make_position(node._left)
    
    def __add_right(self, p, e):
        """Create a new right child for Position p, storing element e.
        
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None: raise ValueError('Right child exists.')
        self._size += 1
        node._right = self._Node(e, node)            # node is its parent
        return self._make_position(node._left)
    
    def _replace(self, p, e):
        """Replace the element at position p with e, and return old element."""
        node = self._validate(p)
        old = node._element
        node.element = e
        return old
    
    def _delete(self, p):
        """Delete the node at Position p, and replace it with its child, if any.
        
        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        
        node = self._validate(p)
        if self.num_children(p) == 2: raise ValueError('p has two children.')
        child = node._left if node._left else node._right # might be None
        if child is not None:
            child._parent = node._parent        # child's grandparent becomes parent
        if node is self._root:
            self._root = child          # child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node             # convention for deprecated node
        return node._element
    
    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):       # all 3 trees must be same type
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():       # attached t1 as left subtree of node
            t1._root._parent = node
            node._left = t1._root
            t1._root = None         # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():       # attached t2 as right subtree of node
            t2._root._parent = node
            node._right = t2._root
            t2._root = None         # set t2 instance to empty
            t2._size = 0
        