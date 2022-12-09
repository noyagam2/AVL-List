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


if __name__ == '__main__':
    unittest.main()
