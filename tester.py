import unittest
import avl_template_new


class MyTestCase(unittest.TestCase):
    def test_Node(self):
        node1 = avl_template_new.AVLNode("5")
        node1.makeNodeLeaf()
        node2 = avl_template_new.AVLNode("6")
        node2.setRight(node1)
        node3 = avl_template_new.AVLNode("7")
        node2.setLeft(node3)
        node2.getValue()
        node4 = avl_template_new.AVLNode("8")

        self.assertEqual(int(node2.getValue()), 6, "Should be 6")  # add assertion here
        self.assertEqual(node2.getHeight(), 0, "Should be 0")
        self.assertTrue(node2.getLeft() is node3)
        self.assertTrue(node2.getRight() is node1)
        self.assertTrue(node1.getLeft() is not None)
        self.assertEqual(node1.getRight().getHeight(), -1, "should be -1")
        self.assertEqual(node1.getParent(), node2)
        self.assertTrue(node1.isRealNode())
        self.assertFalse(node1.getLeft().isRealNode())
        self.assertTrue(node4.getParent() is None)

    def init_list(self, my_list):
        my_list.insert(0, 5)
        my_list.insert(1, 2)
        my_list.insert(0, 8)
        my_list.insert(2, -7)
        my_list.insert(2, 14)


    def test_first_last(self):
        my_list = avl_template_new.AVLTreeList()
        self.init_list(my_list)
        self.assertEqual(int(my_list.first().getValue()), 8, "error 1  in first")
        self.assertEqual(int(my_list.last().getValue()), 2, "error 1 in last")

    def test_insert_retrieve(self):
        my_list = avl_template_new.AVLTreeList()

        rotation_num = my_list.insert(0, 5)
        self.assertEqual(int(my_list.retrieve(0).getValue()), 5, "Error in 1st insert/retrieve")
        self.assertEqual(0, rotation_num,)

        rotation_num = my_list.insert(1, 2)
        self.assertEqual(int(my_list.retrieve(1).getValue()), 2, "Error in 2nd insert/retrieve")
        self.assertEqual(0, rotation_num)

        rotation_num = my_list.insert(0, 8)
        self.assertEqual(0, rotation_num)
        self.assertEqual(int(my_list.retrieve(0).getValue()), 8, "Error in 3rd insert/retrieve")

        rotation_num = my_list.insert(2, -7)
        self.assertEqual(0,rotation_num)
        self.assertEqual(int(my_list.retrieve(2).getValue()), -7, "Error in 4th insert/retrieve")

        rotation_num = my_list.insert(2, 14)
        self.assertEqual(int(my_list.retrieve(2).getValue()), 14, "Error in 5th insert/retrieve")
        self.assertEqual(1, rotation_num)

        rotation_num = my_list.insert(3, 12)
        self.assertEqual(int(my_list.retrieve(3).getValue()), 12, "Error in 5th insert")
        self.assertEqual(1, rotation_num)




        # rotation_num = my_list.insert(5, 25)
        # self.assertEqual(int(my_list.retrieve(5).getValue()), 25, "Error in 6th insert/retrieve")
        # self.assertEqual(1, rotation_num)
        #
        # rotation_num = my_list.insert(6, -13)
        # self.assertEqual(int(my_list.retrieve(6).getValue()), -13, "Error in 7th insert/retrieve")
        # self.assertEqual(1, rotation_num)

    def test_search_delete(self):
        my_list = avl_template_new.AVLTreeList()
        self.init_list(my_list)
        self.assertEqual(int(my_list.search(3)), -1, "Error 1 in search")
        self.assertEqual(int(my_list.search(-7)), 3, "Error 2 in search")

        rotation_num = my_list.delete(3)
        self.assertEqual(int(rotation_num), 0)
        self.assertEqual(int(my_list.length()), 4, "error in delete")
        self.assertEqual(int(my_list.retrieve(3).getValue()), 2, " error in delete")
        self.assertEqual(int(my_list.search(-7)), -1, "Error 3 in search/delete")

        rotation_num = my_list.delete(0)
        self.assertEqual(int(rotation_num), 1)
        self.assertEqual(int(my_list.length()), 3, "error in delete")
        self.assertEqual(int(my_list.retrieve(0).getValue()), 5, " error in delete")
        self.assertEqual(int(my_list.search(8)), -1, "Error 3 in search/delete")



    def test_list_to_array(self):
        my_list = avl_template_new.AVLTreeList()
        self.init_list(my_list)
        array = [8, 5, 14, -7, 2]
        array2 = my_list.listToArray()
        for i in range(len(array)):
            self.assertEqual(array2[i], array[i], "error in list to array,  index " + str(i))

    def test_sorted_permutation(self):
        my_list = avl_template_new.AVLTreeList()
        self.init_list(my_list)
        my_list_sorted = my_list.sort()
        sorted2 = avl_template_new.AVLTreeList()
        sorted2.insert(0, -7)
        sorted2.insert(0, 2)
        sorted2.insert(0, 5)
        sorted2.insert(0, 8)
        sorted2.insert(0, 14)

        for i in range(sorted2.length()):
            self.assertEqual(int(my_list_sorted.retrieve(i).getValue()),
                             int(sorted2.retrieve(i).getValue()), "Error in sorted")
        permutation = my_list_sorted.permutation()

        bool = True
        for i in range(permutation.length()):
            bool = bool and int(permutation.retrieve(i).getValue()) == \
                   int(sorted2.retrieve(i).getValue())
        self.assertFalse(bool, "Error in permutation")

    def test_length(self):
        my_list = avl_template_new.AVLTreeList()
        self.assertEqual(int(my_list.length()), 5, "error in length")


if __name__ == '__main__':
    unittest.main()
