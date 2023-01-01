# username - Orerez
# id1      - 314623372
# name1    - Noy Agam
# id2      - 318970951
# name2    - Or Erez


"""A class represnting a node in an AVL tree"""
import random


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

    def isRealNode(self):
        if self.height == -1:
            return False
        return True

    # ----------------------- AVLNode private methods -----------------------#

    def initVirtualValues(self):
        """This function is used to initialize the virtual nodes"""
        self.right = None
        self.left = None
        self.parent = None
        self.height = -1
        self.size = 0

    def makeNodeLeaf(self):
        """creates virtual sons for node and attaches them appropriately
         :returns: A legal node with 2 virtual sons"""
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
        """checks if node is a leaf"""
        return self.height == 0

    def getSize(self):
        """
        returns the size of the current node
        :return: the size of the subtree rooted at self
        :rtype: int
        """
        return self.size

    def setSize(self, size):
        """ sets the size of the node"""
        self.size = size

    def computeHeight(self):
        """computes the height of the node
        :return: the height of the node
        :rtype: int"""
        return max(self.getLeft().getHeight(), self.getRight().getHeight()) + 1

    def updateHeight(self):
        """updates the height of the node"""
        self.setHeight(self.computeHeight())

    def updateSize(self):
        """updates the size of the node"""
        self.setSize(self.left.size + self.right.size + 1)

    def updateMySizeHeight(self):
        """updates the size and height of the node
        uses only the size and height of the sons, thus O(1)"""
        self.updateHeight()
        self.updateSize()

    def computeBF(self):
        """computes the balance factor of the node
        @pre self is not a virtual node
        :return: the balance factor of the node
        :rtype: int"""
        return self.getLeft().getHeight() - self.getRight().getHeight()


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.size = 0
        self.root = AVLNode("")
        self.root.initVirtualValues()
        self.first_item = None
        self.last_item = None

    def __repr__(self):
        out = ""
        for row in self.printree(self.root):
            out = out + row + "\n"
        return out

    def append(self, val):
        numOfBalanceOps = self.insert(self.length(), val)
        return numOfBalanceOps

    def getTreeHeight(self):
        return self.root.height

    # add your fields here

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

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
        node = self.retrieveNode(i)
        if node is not None:
            return node.getValue()
        return None

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
            current_i = self.retrieveNode(i)
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
        if self.needBalance(node.getParent(), prev_height):
            rotations_num = self.balanceTree(node, "insert")
            self.handleSizesHeights(node)
        return rotations_num

    """deletes the i'th item in the list

      @type i: int
      @pre: 0 <= i < self.length()
      @param i: The intended index in the list to be deleted
      @rtype: int
      @returns: the number of rebalancing operation due to AVL rebalancing
      """

    def delete(self, i):
        # If node has 2 children, O(log(n)). First update sizes and heights, O(log(n)), then balance the tree,
        # O(log(n)). Second update sizes and heights, O(log(n)). Overall, O(log(n)) in worst case.
        if i >= self.size:
            return -1
        node = self.retrieveNode(i)
        if node is None:
            return -1
        if self.size == 1:
            self.root = None
            self.size = 0
            self.first_item = None
            self.last_item = None
            return 0
        if i == 0:  # delete first item
            self.first_item = self.successor(self.first_item)
        if i == self.size - 1:  # delete last item
            self.last_item = self.predecessor(self.last_item)
        if node.getLeft().isRealNode() and node.getRight().isRealNode():
            start_balance = self.deleteNodeHasTwoChildren(node)  # node has two children, O(log(n))
        else:
            start_balance = self.deleteLessThenTwo(node)  # node has less than two children, O(1)
        self.handleSizesHeights(start_balance)
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
            array.append(node.getValue())
            node = self.successor(node)

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
        sorted_tree_list = AVLTreeList()
        array = self.listToArray() # O(n)
        n = len(array)
        self.randQuicksort(array, 0, n - 1)  # O(nlog(n)) in average case
        for i in range(n):
            sorted_tree_list.insert(0, array[n - 1 - i])  # O(log(n))
        return sorted_tree_list

    """permute the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """

    def permutation(self):
        permutated_tree = AVLTreeList()
        array = self.listToArray() # O(n)
        rand = random.Random()

        while self.size > 0:
            i = rand.randint(0, self.size - 1)
            val = self.retrieve(i)
            permutated_tree.insert(0, val)
            self.delete(i)

        for i in range(len(array)):  # reverse the list to its original state
            self.insert(0, array[len(array) - 1])

        return permutated_tree

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        delta = abs(self.getTreeHeight() - lst.getTreeHeight())

        if self.size == 0 and lst.size != 0:
            self.size = lst.size
            self.root = lst.root
            self.first_item = lst.first_item
            self.last_item = lst.last_item
            return delta
        if lst.size == 0 and self.size != 0:
            return delta
        if self.size == 0 and lst.size == 0:
            return delta

        totalSize = self.size + lst.size

        if self.size == 1:
            lst.insert(0, self.getRoot().getValue())
            self.size = lst.size
            self.root = lst.root
            self.first_item = lst.first_item
            self.last_item = lst.last_item
            return delta

        if lst.size == 1:
            self.insert(self.size, lst.getRoot().getValue())
            return delta

        if self.getTreeHeight() <= lst.getTreeHeight():
            x = AVLNode(self.last_item.getValue())
            self.delete(self.size - 1)
            x.setLeft(self.getRoot())
            x.setHeight(self.getTreeHeight() + 1)
            x.setSize(self.size + 1)
            self.size += 1
            self.root = x
            self.last_item = x
            b = lst.getRoot()
            while b.getHeight() > self.getTreeHeight() - 1:
                b = b.getLeft()
            if b == lst.getRoot():
                x.setRight(b)
                x.setSize(totalSize)
                self.size = totalSize
                self.root = x
                self.last_item = lst.last_item
                return delta

            c = b.getParent()
            c.setLeft(x)
            x.setRight(b)

            self.root = lst.root
            self.size = totalSize
            self.balanceTree(x, "concat")
            self.handleSizesHeights(b)
            self.last_item = lst.last_item

        else:
            x = self.last_item
            self.delete(self.size - 1)
            x.setRight(lst.getRoot())

            x.setHeight(lst.getTreeHeight() + 1)  #
            x.setSize(lst.size + 1)  #

            b = self.getRoot()
            while b.getHeight() > lst.getTreeHeight():
                b = b.getRight()
            if b == self.getRoot():
                x.setLeft(b)
                return delta
            c = b.getParent()
            c.setRight(x)
            x.setLeft(b)
            self.size = totalSize
            self.balanceTree(x, "concat")
            self.handleSizesHeights(b)
            self.last_item = lst.last_item

        return delta

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        if self.size == 0:
            return -1
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

    # ------------------------------------------ AVLTreeList Private Methods -------------------------------------------

    # ----------------------- iterator methods -----------------------

    def successor(self, node):
        """returns the successor of node or a virtual node if node is last, complexity O(logn)
         @pre: node belongs to this AVLTreeList
         :type node: AVLNode
         :rtype : AVLNode
         :param node: the node we want to find the successor for
         :returns the successor of given node in the tree, virtual node if node is max
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
        :returns the predecessor of given node in the tree, virtual node if node is min
        """
        if node is self.first_item:
            return self.first_item.left
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

    # ----------------------- retrieve helper methods -----------------------
    def retrieveNode(self, i):
        """
        returns the node in the i'th position in the list in complexity O(log n)
        @pre: 0 <= i < self.length()
        :param i: index in the list
        :rtype: AVLNode
        :return: AVLNode in the i'th position in the list
        """
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

    # ----------------------- rotation methods -----------------------
    def leftRotation(self, node):
        """
        Handles the rotation where a node Balance Factor is -2, and it's right son's
        Balance Factor is -1 (or 0), works in O(1)

        (node)
              \
               \
                (r_son)
                   \
                    \
                     (tree)

        @pre: BF(node) == -2 and (BF(node.getRight()) == -1 or BF(node.getRight()) == 0)
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
        Balance Factor is +1 , works in O(1)

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
        Balance Factor is -1 , works in O(1)

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
        Balance Factor is +1 (or 0), works in O(1)

                       (node)
                      /
                    /
                (l_son)
              /
            /
        (tree)

        @pre: BF(node) == 2 and (BF(node.getLeft()) == 1 or BF(node.getLeft()) == 0)
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
        """makes a rotation needed to balance the tree, returns the number of rotations made, works in O(1)
        :param parent: the parent of the node with BF = 2 or -2
        :type parent: AVLNode
        :param BFparent: the BF of the parent
        :type BFparent: int
        :param BFnode: the BF of the node
        :type BFnode: int
        :return: the number of rotations made (1 for single rotation, 2 for double rotation)
        :rtype: int
        """
        if BFparent == 2:
            if BFnode == 1 or BFnode == 0:
                self.rightRotation(parent)
                return 1
            if BFnode == -1:
                self.leftThenRightRotation(parent)
                return 2

        elif BFparent == -2:
            if BFnode == 1:
                self.rightThenLeftRotation(parent)
                return 2
            if BFnode == -1 or BFnode == 0:
                self.leftRotation(parent)
                return 1
        return 0

    # ----------------------- insert helper methods -----------------------
    def balanceTree(self, node, called_from):
        """ balances the tree from the node upwards, works in O(log n)
        @pre called_from is either "insert" or "delete"
        :param node: the node to start balancing from
        :type node: AVLNode
        :param called_from: the function from which balanceTree was called from
        :type called_from: str
        :return: the number of rotations performed
        :rtype: int"""

        count = 0
        if node is self.getRoot():  # handle the case where node is the root, and thus has no parent, works in O(1)
            return self.balanceFromRoot()
        while node.getParent() is not None:  # handle the case where node is not the root
            node.updateMySizeHeight()
            parent = node.getParent()
            BFparent = parent.computeBF()
            BFnode = node.computeBF()
            if BFnode == -2 or BFnode == 2:  # handle the case when node is the AVL criminal and not parent
                parent = node
                node = node.getRight() if BFnode == -2 else node.getLeft()
                BFparent = BFnode
                BFnode = node.computeBF()
            count += self.makeRotation(parent, BFparent, BFnode)
            if count == 1 and called_from == "insert":
                return count
            node = parent
        return count

    def balanceFromRoot(self):
        """balances the tree from the root, works in O(1)
        @pre: the root is the AVL criminal
        :return: the number of rotations performed
        :rtype: int
        """
        node = self.root
        if node.isLeaf():
            return 0
        parent = node
        if node.getRight().isRealNode():
            son = node.getRight()
        else:
            son = node.getLeft()
        BFparent = node.computeBF()
        BFnode = son.computeBF()
        return self.makeRotation(parent, BFparent, BFnode)

    def handleSizesHeights(self, node):
        """updates the sizes and heights of the nodes in the tree from node
        upwards to the root, works in O(log n)
        :param node: the node to start updating from
        :type node: AVLNode
        """
        while node is not None:
            node.updateMySizeHeight()
            node = node.getParent()

    def insertFirstNode(self, node):
        """Handles the insert of the first node in the tree
        :param node: the to-be root node
        :type node: AVLNode
        """
        self.root = node
        self.last_item = node
        self.first_item = node
        self.size = 1

    def needBalance(self, parent, prev_height):
        """checks if the tree needs to be balanced after an insert, works in O(1)
        :param parent: the parent of the inserted node
        :type parent: AVLNode
        :param prev_height: the height of the parent before the insert
        :type prev_height: int
        :return: True if the tree needs to be balanced, False otherwise"""
        BFparent = parent.getLeft().getHeight() - parent.getRight().getHeight()
        curr_parent_height = parent.computeHeight()
        if -2 < BFparent < 2 and prev_height == curr_parent_height:
            return False
        return True

    # ----------------------- delete helper methods -----------------------
    def deleteNodeIsLeaf(self, node):
        """deletes a node that is a leaf, works in O(1)
        :param node: the node to delete
        :type node: AVLNode
        :return: the number of rotations needed to balance the tree after the deletion
        """
        virtual = AVLNode("")
        virtual.initVirtualValues()
        if node.getParent().getRight() is node:
            node.getParent().setRight(virtual)
        else:
            node.getParent().setLeft(virtual)

    def deleteLessThenTwo(self, node):
        """deletes a node that has less than 2 sons, works in O(1)
        @pre: node.getRight().isRealNode() == False or node.getLeft().isRealNode() == False
        :param node: the node to delete
        :type node: AVLNode
        :return: the number of rotations needed to balance the tree after the deletion
        :rtype: AVLNode"""
        if node.isLeaf():
            parent = node.getParent()
            self.deleteNodeIsLeaf(node)
            return parent
        else:
            parent_of_node = node.getParent()
            direction = "N"
            if parent_of_node is not None:
                direction = "r" if parent_of_node.getRight() is node else "l"
            son = node.getRight() if node.getRight().isRealNode() else node.getLeft()
            if direction == "r":
                node.getParent().setRight(son)
                return parent_of_node
            elif direction == "l":
                node.getParent().setLeft(son)
                return parent_of_node
            else:
                self.root = son
                self.root.setParent(None)
                son.makeNodeLeaf()
                return self.root

    def deleteNodeHasTwoChildren(self, node):
        """deletes a node that has two children, works in O(log(n))
        @pre: node.getRight().isRealNode() == True and node.getLeft().isRealNode() == True
        :param node: the node to delete
        :type node: AVLNode
        :return: the number of rotations needed to balance the tree after the deletion
        :rtype: AVLNode"""
        successor = self.successor(node)
        balance_start = successor if successor.getParent() is node else successor.getParent()
        self.deleteLessThenTwo(successor)
        successor.setRight(node.getRight())
        successor.setLeft(node.getLeft())
        successor.setParent(node.getParent())
        if node is self.root:
            self.root = successor
            return balance_start
        else:
            direction = "r" if node.getParent().getRight() is node else "l"
            if direction == "r":
                node.getParent().setRight(successor)
            else:
                node.getParent().setLeft(successor)
        return balance_start

    # ----------------------- sort helper methods -----------------------
    def replaceVals(self, array, k, m):
        """
        Replaces 2 values in array in indexes k and m, works in place and in O(1)
        :param array: the array to replace values in
        :param k: the position of the first item to replace in the array
        :type k: int
        :param m: the position of the second item to replace in the array
        :type m: int
        """
        temp = array[k]
        array[k] = array[m]
        array[m] = temp

    def lomutoPartition(self, array, l, r):
        """
        Implementation of lomuto's partition, works in place in O(n)
        :param array: the array to partition
        :param l: left index
        :type l: int
        :param r: right index
        :type r: int
        :return: the position of pivot
        :rtype: int
        """
        ran = random.Random()
        pivot = ran.randint(l, r)
        self.replaceVals(array, pivot, r)

        i = l - 1
        for j in range(l, r):
            if array[j] < array[r]:
                i += 1
                self.replaceVals(array, i, j)
        self.replaceVals(array, i + 1, r)
        return i + 1

    def randQuicksort(self, array, l, r):
        """
        A recursive, random quicksort for arrays based on lomuto's partition,
        works in O(n^2) in the worst case, but in O(nlogn) in the average case
        :param array: array to sort
        :param l: left bound
        :type l: int
        :param r: right bound
        :type r: int
        """
        if l < r:
            p = self.lomutoPartition(array, l, r)
            self.randQuicksort(array, l, p - 1)
            self.randQuicksort(array, p + 1, r)

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

    def __repr__(self):
        out = ""
        for row in self.printree(self.root):
            out = out + row + "\n"
        return out

        # -----------------------testing the tree-----------------------

    def append(self, val):
        self.insert(self.length(), val)

    def getTreeHeight(self):
        return self.root.height






