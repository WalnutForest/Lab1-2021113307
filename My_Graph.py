import string
from collections import deque

import My_Edge
from graphviz import Digraph
import random

class My_Graph:
    txt = ""
    words = []
    graph = []

    def __init__(self, file_path = "test_file/test.txt"):
        #读取文本文件，返回一个string
        with open(file_path, 'r') as f:
            tmp_string = f.read()
        #将tmp_string中除了a-z,A-Z以外的字符替换为空格
        for i in range(len(tmp_string)):
            if not tmp_string[i].isalpha():
                tmp_string = tmp_string.replace(tmp_string[i], ' ')
        self.txt = tmp_string
        #将txt中的文本按照空格分割，返回一个list，由于之后需要单词的邻接关系，需要顺序不变
        self.words = self.txt.split()
        #将单词转换为小写
        for i in range(len(self.words)):
            self.words[i] = self.words[i].lower()
        #依据单词的邻接关系，构建图
        self.graph = []
        for i in range(len(self.words) - 1):
            self.graph.append(My_Edge.My_Edge(self.words[i], self.words[i + 1], 1))
        #将重复的边合并，权重相加
        for i in range(len(self.graph) - 2):
            for j in range(i + 1, len(self.graph) - 1):
                if j >= len(self.graph):
                    break
                if self.graph[i].__eq__(self.graph[j]):
                    self.graph[i].weight += self.graph[j].weight
                    self.graph.pop(j)


    def print_graph(self):
        for i in range(len(self.graph)):
            print(self.graph[i])

    def showDirectedGraph(self):
        #使用Graphviz绘制有向图
        dot = Digraph(comment='Directed Graph')
        for i in range(len(self.graph)):
            dot.edge(self.graph[i].node1, self.graph[i].node2, label=str(self.graph[i].weight))
        #将图保存为png格式
        dot.render('test-output/round-table.gv', view=True, format='png')

    def calcShortestPathsToAllWords(self, word1: string):
        #检查word1是否在self.words中
        if word1 not in self.words:
            #返回三个空list
            return  [], [], []
        #使用Floyd算法计算word1到所有单词的最短路径
        tmp_words = self.words
        #对self.words进行去重，保持顺序不变
        self.words = []
        for i in range(len(tmp_words)):
            if tmp_words[i] not in self.words:
                self.words.append(tmp_words[i])
        path = []
        distence = []
        for i in range(len(self.words)):
            path.append([])
            distence.append([])
            for j in range(len(self.words)):
                path[i].append(0)
                distence[i].append(0)

        for i in range(len(self.words)):
            for j in range(len(self.words)):
                path[i][j] = -1
                distence[i][j] = 9999999
        for i in range(len(self.words)):
            for j in range(len(self.words)):
                if i == j:
                    distence[i][j] = 0
                    path[i][j] = i
        for i in range(len(self.graph)):
            distence[self.words.index(self.graph[i].node1)][self.words.index(self.graph[i].node2)] = self.graph[i].weight
            path[self.words.index(self.graph[i].node1)][self.words.index(self.graph[i].node2)] = self.words.index(self.graph[i].node2)
        for k in range(len(self.words)):
            for i in range(len(self.words)):
                for j in range(len(self.words)):
                    if distence[i][j] > distence[i][k] + distence[k][j]:
                        distence[i][j] = distence[i][k] + distence[k][j]
                        path[i][j] = path[i][k]
        #例如：输入to和and，则其最短路径为to→explore→strange→new→life→and
        path_list = []
        for i in range(len(self.words)):
            #path_list[i]表示word1到words[i]的最短路径
            path_list.append([])
            next = path[self.words.index(word1)][i]
            if next == -1 or i == self.words.index(word1):
                path_list[i].append("No path")
                continue
            while next != i:
                path_list[i].append(self.words[next])
                next = path[next][i]
            path_list[i].append(self.words[i])
            path_list[i].insert(0, word1)
        self.words = tmp_words
        return path, distence, path_list

    def calcShortestPath(self, word1: string, word2: string) -> string :
        #检查word1和word2是否在self.words中
        if word1 not in self.words or word2 not in self.words:
            return "No such word"
        #使用calcShortestPathsToAllWords的结果计算word1到word2的最短路径
        path, distance, path_list = self.calcShortestPathsToAllWords(word1)
        tmp_words = self.words
        # 对self.words进行去重，保持顺序不变
        self.words = []
        for i in range(len(tmp_words)):
            if tmp_words[i] not in self.words:
                self.words.append(tmp_words[i])
        path_word1_2_word2 = path_list[self.words.index(word2)]
        #将path_word1_2_word2转换为很多个edge
        tmp_path_word1_2_word2_edge = []
        dot = Digraph(comment='Directed Graph')
        for i in range(len(path_word1_2_word2) - 1):
            tmp_path_word1_2_word2_edge.append(My_Edge.My_Edge(path_word1_2_word2[i], path_word1_2_word2[i + 1], 1))
        for i in range(len(self.graph)):
            if self.graph[i] in tmp_path_word1_2_word2_edge:
                #点和边的颜色都为红色
                dot.edge(self.graph[i].node1, self.graph[i].node2, label=str(self.graph[i].weight), color='red')
            else:
                dot.edge(self.graph[i].node1, self.graph[i].node2, label=str(self.graph[i].weight))
        dot.render('test-output/round-table.gv', view=True, format='png')
        #在path_word1_2_word2最后加上距离
        path_word1_2_word2.append(str(distance[self.words.index(word1)][self.words.index(word2)]))
        self.words = tmp_words
        return path_word1_2_word2


    def randomWalk(self) -> string:
        #随机游走
        #从第一个单词开始，根据权重随机选择下一个单词，直到遇到重复边或者无法继续
        #返回游走的路径
        tmp_words = self.words
        # 对self.words进行去重，保持顺序不变
        self.words = []
        for i in range(len(tmp_words)):
            if tmp_words[i] not in self.words:
                self.words.append(tmp_words[i])
        #随机选择第一个单词
        path = []
        path.append(self.words[random.randint(0, len(self.words) - 1)])
        #遍历graph,将起始点为path的边加入到可选边中
        available_edges = []
        for i in range(len(self.graph)):
            if self.graph[i].node1 == path[0]:
                available_edges.append(self.graph[i])
        #随机选择下一个单词，并标记已经访问过的边
        exist_edge = []
        while len(available_edges) > 0:
            next = available_edges[random.randint(0, len(available_edges) - 1)]
            path.append(next.node2)
            #检验是否有重复边
            if next in exist_edge:
                break
            exist_edge.append(next)
            #清空可选边，将下一个单词的边加入到可选边中
            available_edges = []
            for i in range(len(self.graph)):
                if self.graph[i].node1 == next.node2:
                    available_edges.append(self.graph[i])
        self.words = tmp_words
        return path

    def showBridgeWords(self, word1: string, word2: string) -> string:
        flag1 = 0
        flag2 = 0

        if word1 not in self.words:
            flag1 = 1
        if word2 not in self.words:
            flag2 = 1

        if flag1:
            if flag2:
                return "No " + word1 + " and " + word2 + " in the graph!"
            else:
                return "No " + word1 + " in the graph!"
        else:
            if flag2:
                return "No " + word2 + " in the graph!"

        unique_words = list(dict.fromkeys(self.words))
        index_map = {word: idx for idx, word in enumerate(unique_words)}
        visited = set()
        queue = deque([(word1, 0)])
        result = {word1: []}
        brigdeWord = [""]
        ans = ""

        while queue:
            current_node, layer = queue.popleft()
            if layer >= 2:
                continue

            for edge in self.graph:
                if edge.node1 == current_node and edge.node2 not in visited:
                    if layer == 0:
                        visited.add(edge.node2)
                        result[word1].append(edge.node2)
                        queue.append((edge.node2, layer + 1))
                    if layer == 1 and word2.__eq__(edge.node2):
                        brigdeWord.append(current_node)
                        # return "The bridges word from " + word1 + " to " + word2 + " is: " + current_node

        # return brigdeWord

        if (len(brigdeWord) <= 1):
            ans = "No bridge words from " + word1 + " to " + word2 + "!"
        elif (len(brigdeWord) == 2):
            ans = "The bridges word from " + word1 + " to " + word2 + " is: " + brigdeWord[1]
        else:
            ans = "The bridges word from " + word1 + " to " + word2 + " are: "
            for i in range(len(brigdeWord) - 2):
                if i > 0:
                    ans = ans + brigdeWord[i] + ','
            ans = ans + brigdeWord[-2] + " and " + brigdeWord[-1]
        return ans

    def calcBrigdeWords(self, word1: string, word2: string) -> string:

        if word1 not in self.words or word2 not in self.words:
            return " "

        unique_words = list(dict.fromkeys(self.words))
        index_map = {word: idx for idx, word in enumerate(unique_words)}
        visited = set()
        queue = deque([(word1, 0)])
        result = {word1: []}

        while queue:
            current_node, layer = queue.popleft()
            if layer >= 2:
                continue

            for edge in self.graph:
                if edge.node1 == current_node and edge.node2 not in visited:
                    visited.add(edge.node2)
                    result[word1].append(edge.node2)
                    queue.append((edge.node2, layer + 1))
                    if layer == 1 and word2.__eq__(edge.node2):
                        return " " + current_node + " "
        return " "
    def generateNewText(self, text: string) -> string:
        for i in range(len(text)):
            if not text[i].isalpha():
                text = text.replace(text[i], ' ')
        self.txt = text
        # 将txt中的文本按照空格分割，返回一个list，由于之后需要单词的邻接关系，需要顺序不变
        self.words = self.txt.split()
        # 将单词转换为小写
        for i in range(len(self.words)):
            self.words[i] = self.words[i].lower()

        result = self.words[0]

        for i in range(len(self.words) - 1):
            tmp = self.calcBrigdeWords(self.words[i], self.words[i + 1])
            result = result + tmp + self.words[i + 1]

        return result