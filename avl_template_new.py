# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - noy's branch


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0
        self.size = 1

    def initVirtualValues(self):
        self.right = None
        self.left = None
        self.parent = None
        self.height = -1
        self.size = 0

    """
         creates virtual sons for node and attaches them appropriately

         :returns: A legal node with 2 virtual sons
         """

    def makeNodeLeaf(self):
        right_virtual_son = AVLNode("")
        left_virtual_son = AVLNode("")
        right_virtual_son.initVirtualValues()
        left_virtual_son.initVirtualValues()
        self.right = right_virtual_son
        right_virtual_son.parent = self
        self.left = left_virtual_son
        left_virtual_son.parent = self
        self.height = 0

    def isLeaf(self):
        return self.height == 0

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node
        node.parent = self

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node
        node.parent = self

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def __str__(self) -> str:
        return str(self.value)

    def isRealNode(self):
        if self.height == -1:
            return False
        return True

    def getSize(self):
        return self.size

    def setSize(self, size):
        self.size = size

    def computeHeight(self):
        return max(self.getLeft().getHeight(), self.getRight().getHeight()) + 1

    def updateHeight(self):
        self.setHeight(self.computeHeight())

    def updateSize(self):
        self.setSize(self.left.size + self.right.size + 1)

    def updateMySizeHeight(self):
        self.updateHeight()
        self.updateSize()


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.size = 0
        self.root = None
        self.first_item = None
        self.last_item = None

    def __repr__(self):
        out = ""
        for row in self.printree(self.root):
            out = out + row + "\n"
        return out

    def append(self, val):
        self.insert(self.length(), val)

    def getTreeHeight(self):
        return self.root.height

    # add your fields here

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

    def successor(self, node):
        """returns the successor of node or a virtual node if node is max, complexity O(logn)
         @pre: node belongs to this AVLTreeList
         :type node: AVLNode
         :rtype : AVLNode
         :param node: the node we want to find the successor for
         :returns the successor of given node in the tree
        """
        if node is self.last_item:
            return self.last_item.right
        if node.right.height == -1:
            father = node.parent
            while father.right is node:
                father = father.parent
                node = node.parent
            return father
        else:
            node = node.right
            while node.left.height != -1:
                node = node.left
            return node

    def predecessor(self, node):
        """returns the predecessor of node or a virtual node if node is min, complexity O(logn)
        @pre: node belongs to this AVLTreeList
        :type node: AVLNode
        :rtype: AVLNode
        :param node: the node we want to find the predecessor for
        :returns the predecessor of given node in the tree
        """
        if node is self.first_item:
            return self.first_item_item.left
        if node.left.height == -1:
            father = node.parent
            while father.left is node:
                father = father.parent
                node = node.parent
            return father
        else:
            node = node.left
            while node.right.height != -1:
                node = node.right
            return node

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):
        if i >= self.size:
            return None
        node = self.retrieve_node(i)
        if node is not None:
            return node.getValue()
        return None

    def retrieve_node(self, i):
        node = self.getRoot()
        if not node.isRealNode():  # list is empty
            return None
        if i == self.size - 1:
            return self.last_item
        elif i == 0:
            return self.first_item
        while i >= 0:
            if i == node.getLeft().getSize():
                return node
            elif i < node.getLeft().getSize():
                node = node.getLeft()
            elif i > node.getLeft().getSize():
                i = i - node.getLeft().getSize() - 1
                node = node.getRight()

    def leftRotation(self, node):
        """
        Handles the rotation where a node Balance Factor is -2, and it's right son's
        Balance Factor is -1

        (node)
              \
               \
                (r_son)
                   \
                    \
                     (tree)

        @pre: BF(node) == -2 and BF(node.getRight()) == -1
        :param node: the "AVL criminal"
        :type node: AVLNode
        """

        direction = "N"
        parent_of_node = node.getParent()
        if parent_of_node is not None:
            direction = "r" if parent_of_node.getRight() is node else "l"
        right_son = node.getRight()
        node.setRight(right_son.getLeft())
        right_son.setLeft(node)
        right_son.setParent(parent_of_node)
        if direction == "r":
            right_son.getParent().setRight(right_son)
        elif direction == "l":
            right_son.getParent().setLeft(right_son)
        else:
            self.root = right_son

        node.updateMySizeHeight()
        right_son.updateMySizeHeight()

    def rightThenLeftRotation(self, node):
        """
        Handles the rotation where a node Balance Factor is -2, and it's right son's
        Balance Factor is +1

       (node)
             \
              \
               (r_son)
              /
            /
        (tree)

         @pre: BF(node)== -2 and BF(node.getRight())== 1
        :param node: the "AVL criminal"
        :type node: AVLNode
        """
        right_son = node.getRight()
        self.rightRotation(right_son)
        self.leftRotation(node)

    def leftThenRightRotation(self, node):
        """
        Handles the rotation where a node Balance Factor is +2, and it's left son's
        Balance Factor is -1

               (node)
              /
            /
        (l_son)
           \
            \
             (tree)


        @pre: BF(node) == 2 and BF(node.getLeft()) == -1
        :param node: the "AVL criminal"
        :type node: AVLNode
        """
        left_son = node.getLeft()
        self.leftRotation(left_son)
        self.rightRotation(node)

    def rightRotation(self, node):
        """
        Handles the rotation where a node Balance Factor is +2, and it's left son's
        Balance Factor is +1

                       (node)
                      /
                    /
                (l_son)
              /
            /
        (tree)

        @pre: BF(node) == 2 and BF(node.getLeft()) == 1
        :param node: the "AVL criminal"
        :type node: AVLNode
        """
        direction = "N"
        parent_of_node = node.getParent()
        if parent_of_node is not None:
            direction = "r" if parent_of_node.getRight() is node else "l"
        parent_of_node = node.getParent()
        left_son = node.getLeft()
        node.setLeft(left_son.getRight())
        left_son.setRight(node)
        left_son.setParent(parent_of_node)
        if direction == "r":
            left_son.getParent().setRight(left_son)
        elif direction == "l":
            left_son.getParent().setLeft(left_son)
        else:
            self.root = left_son
        node.updateMySizeHeight()
        left_son.updateMySizeHeight()

    def makeRotation(self, parent, BFparent, BFnode):
        if BFparent == 2:
            if BFnode == 1 or BFnode == 0:
                self.rightRotation(parent)
            elif BFnode == -1:
                self.leftThenRightRotation(parent)
            return 1

        elif BFparent == -2:
            if BFnode == 1:
                self.rightThenLeftRotation(parent)
            elif BFnode == -1 or BFnode == 0:
                self.leftRotation(parent)
            return 1
        return 0

    def balanceTree(self, node, called_from):
        count = 0
        if node is self.getRoot():
            if node.isLeaf():
                return 0
            parent = node
            if node.getRight().isRealNode():
                son = node.getRight()
            else:
                son = node.getLeft()
            BFparent = node.getLeft().getHeight() - node.getRight().getHeight()
            BFnode = son.getLeft().getHeight() - son.getRight().getHeight()
            return self.makeRotation(parent, BFparent, BFnode)
        while node.getParent() is not None:
            parent = node.getParent()
            BFparent = parent.getLeft().getHeight() - parent.getRight().getHeight()
            BFnode = node.getLeft().getHeight() - node.getRight().getHeight()
            if BFnode == -2 or BFnode == 2:  # Handle the case when node is AVL criminal and not parent
                parent = node
                node = node.getRight() if BFnode == -2 else node.getLeft()
                BFparent = BFnode
                BFnode = node.getLeft().getHeight() - node.getRight().getHeight()
            count += self.makeRotation(parent, BFparent, BFnode)
            if count == 1 and called_from == "insert":
                return count
            node = parent
        return count

    def handleSizesHeights(self, node):
        while node is not None:
            node.updateMySizeHeight()
            node = node.getParent()

    def insertFirstNode(self, node):
        """
        Handles the insert of the first node in the tree
        :param node: the to-be root node
        :type node: AVLNode
        """
        self.root = node
        self.last_item = node
        self.first_item = node
        self.size = 1

    def need_balance(self, parent, prev_height):
        BFparent = parent.getLeft().getHeight() - parent.getRight().getHeight()
        curr_parent_height = parent.computeHeight()
        if -2 < BFparent < 2 and prev_height == curr_parent_height:
            return False
        return True

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        node = AVLNode(val)
        node.makeNodeLeaf()
        if self.size == 0:
            self.insertFirstNode(node)
            return 0
        if i == self.size:
            prev_height = self.last_item.computeHeight()
            self.last_item.setRight(node)
            self.last_item = node
        elif i == 0:
            prev_height = self.first_item.computeHeight()
            self.first_item.setLeft(node)
            self.first_item = node
        else:
            current_i = self.retrieve_node(i)
            if current_i.getLeft().isRealNode() == False:
                prev_height = current_i.computeHeight()
                current_i.setLeft(node)
            else:
                pred = self.predecessor(current_i)
                prev_height = pred.computeHeight()
                pred.setRight(node)
        self.size += 1
        rotations_num = 0
        self.handleSizesHeights(node)
        if self.need_balance(node.getParent(), prev_height):
            rotations_num = self.balanceTree(node, "insert")
            self.handleSizesHeights(node)
        return rotations_num

    def deleteNodeIsLeaf(self, node):
        virtual = AVLNode("")
        virtual.initVirtualValues()
        if node.getParent().getRight() is node:
            node.getParent().setRight(virtual)
        else:
            node.getParent().setLeft(virtual)

    def deleteLessThenTwo(self, node):
        if node.isLeaf():
            self.deleteNodeIsLeaf(node)
        else:
            parent_of_node = node.getParent()
            direction = "N"
            if parent_of_node is not None:
                direction = "r" if parent_of_node.getRight() is node else "l"
            son = node.getRight() if node.getRight().isRealNode() else node.getLeft()
            if direction == "r":
                node.getParent().setRight(son)
            elif direction == "l":
                node.getParent().setLeft(son)
            else:
                self.root = son
                self.root.setParent(None)
                son.makeNodeLeaf()

    def deleteNodeHasTwoChildren(self, node):
        successor = self.successor(node)
        self.deleteLessThenTwo(successor)
        successor.setRight(node.getRight())
        successor.setLeft(node.getLeft())
        successor.setParent(node.getParent())
        if node is self.root:
            self.root = successor
        else:
            direction = "r" if node.getParent().getRight() is node else "l"
            if direction == "r":
                node.getParent().setRight(successor)
            else:
                node.getParent().setLeft(successor)

    """deletes the i'th item in the list

      @type i: int
      @pre: 0 <= i < self.length()
      @param i: The intended index in the list to be deleted
      @rtype: int
      @returns: the number of rebalancing operation due to AVL rebalancing
      """

    def delete(self, i):
        if i >= self.size:
            return -1
        node = self.retrieve_node(i)
        parent = node.getParent()
        if self.size == 1:
            self.root = None
            self.size = 0
            self.first_item = None
            self.last_item = None
            return 0
        if i == 0:  # delete first item
            self.first_item = self.successor(self.first_item)
        if i == self.size - 1:  # delete last item
            start_balance = self.predecessor(node)
            self.last_item = self.predecessor(self.last_item)
        else:
            start_balance = self.successor(node)
            if node is self.root:  # delete root
                parent = start_balance.parent
                if parent is node:
                    parent = start_balance
        if node.getLeft().isRealNode() and node.getRight().isRealNode():
            self.deleteNodeHasTwoChildren(node)
        else:
            self.deleteLessThenTwo(node)
        self.handleSizesHeights(parent)
        rotations_num = self.balanceTree(start_balance, "delete")
        self.handleSizesHeights(start_balance)
        self.size -= 1
        return rotations_num

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        if self.size == 0:
            return None
        return self.first_item.getValue()

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.size == 0:
            return None
        return self.last_item.getValue()

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        array = []
        node = self.first_item
        for i in range(self.size):
            array.append(str(node))

        return array

    """returns the size of the list

    @rtype: int
    @returns: the size of the list"""

    def length(self):
        return self.size

    """sort the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are sorted by the info of the original list.
    """

    def sort(self):
        return None

    """permute the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """

    def permutation(self):
        return None

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        return None

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        node = self.first_item
        count = 0
        while node.isRealNode() and node.getValue() != val:
            count += 1
            node = self.successor(node)
        return count if node.isRealNode() else -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root

    ########### printing the tree ###########

    def printree(self, t, bykey=False):
        """Print a textual representation of t
        bykey=True: show keys instead of values"""
        # for row in trepr(t, bykey):
        #        print(row)
        return self.trepr(t, bykey)

    def trepr(self, t, bykey=False):
        """Return a list of textual representations of the levels in t
        bykey=True: show keys instead of values"""
        if t.getHeight() == -1:
            return ["#"]

        thistr = str(t.value)

        return self.conc(self.trepr(t.left, bykey), thistr, self.trepr(t.right, bykey))

    def conc(self, left, root, right):
        """Return a concatenation of textual represantations of
        a root node, its left node, and its right node
        root is a string, and left and right are lists of strings"""

        lwid = len(left[-1])
        rwid = len(right[-1])
        rootwid = len(root)

        result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

        ls = self.leftspace(left[0])
        rs = self.rightspace(right[0])
        result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

        for i in range(max(len(left), len(right))):
            row = ""
            if i < len(left):
                row += left[i]
            else:
                row += lwid * " "

            row += (rootwid + 2) * " "

            if i < len(right):
                row += right[i]
            else:
                row += rwid * " "

            result.append(row)

        return result

    def leftspace(self, row):
        """helper for conc"""
        # row is the first row of a left node
        # returns the index of where the second whitespace starts
        i = len(row) - 1
        while row[i] == " ":
            i -= 1
        return i + 1

    def rightspace(self, row):
        """helper for conc"""
        # row is the first row of a right node
        # returns the index of where the first whitespace ends
        i = 0
        while row[i] == " ":
            i += 1
        return i
