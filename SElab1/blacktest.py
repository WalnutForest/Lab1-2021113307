import unittest
import My_Graph


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.graph = My_Graph.My_Graph()

    def test_no_word_in_graph(self):
        result = self.graph.showBridgeWords("wordX", "wordY")
        self.assertEqual(result, "No wordX and wordY in the graph!")

    def test_word1_in_graph_word2_not_in_graph(self):
        result = self.graph.showBridgeWords("python", "wordY")
        self.assertEqual(result, "No wordY in the graph!")

    def test_word1_not_in_graph_word2_in_graph(self):
        result = self.graph.showBridgeWords("wordX", "python")
        self.assertEqual(result, "No wordX in the graph!")

    def test_no_bridge_words(self):
        result = self.graph.showBridgeWords("happy", "python")
        self.assertEqual(result, "No bridge words from happy to python!")

    def test_one_bridge_word(self):
        result = self.graph.showBridgeWords("am", "student")
        self.assertEqual(result, "The bridge words from am to student is: a")

    def test_multiple_bridge_words(self):
        result = self.graph.showBridgeWords("am", "python")
        self.assertEqual(result, "The bridge words from am to python are: studying,learning and using")

    def test_empty_string_input(self):
        result1 = self.graph.showBridgeWords("", "python")
        result2 = self.graph.showBridgeWords("python", "")
        self.assertEqual(result1, "No  in the graph!")
        self.assertEqual(result2, "No  in the graph!")

    def test_single_node_graph(self):
        graph_single = My_Graph.My_Graph()
        result = graph_single.showBridgeWords("python", "python")
        self.assertEqual(result, "No bridge words from python to python!")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('setUp'))
    suite.addTest(MyTestCase('test_no_word_in_graph'))
    suite.addTest(MyTestCase('test_word1_in_graph_word2_not_in_graph'))
    suite.addTest(MyTestCase('test_word1_not_in_graph_word2_in_graph'))
    suite.addTest(MyTestCase('test_no_bridge_words'))
    suite.addTest(MyTestCase('test_one_bridge_word'))
    suite.addTest(MyTestCase('test_multiple_bridge_words'))
    suite.addTest(MyTestCase('test_empty_string_input'))
    suite.addTest(MyTestCase('test_single_node_graph'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
