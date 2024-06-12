import unittest
import My_Graph


class MyTestCase(unittest.TestCase):
    def testcase1(self):
        graph = My_Graph.My_Graph()
        self.assertEqual("No such word", graph.calcShortestPath("inexistence", "am"))  # add assertion here

    def testcase2(self):
        graph = My_Graph.My_Graph()
        self.assertEqual("No such word", graph.calcShortestPath("am", "inexistence"))

    def testcase3(self):
        graph = My_Graph.My_Graph()
        self.assertEqual(['No path', '0'], graph.calcShortestPath("i", "i"))

    def testcase4(self):
        graph = My_Graph.My_Graph()
        self.assertEqual(['i', 'am', 'a', '11'], graph.calcShortestPath("i", "a"))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('testcase1'))
    suite.addTest(MyTestCase('testcase2'))
    suite.addTest(MyTestCase('testcase3'))
    suite.addTest(MyTestCase('testcase4'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
