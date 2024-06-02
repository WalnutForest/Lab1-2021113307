import os

from My_Graph import My_Graph
import tkinter as tk

def gui_calcShortestPath(graph, text_output, entry1, entry2):
    path_single_tmp = graph.calcShortestPath(entry1.get(), entry2.get())
    if path_single_tmp == "No such word":
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "No such word\n")
        return
    #将path_single_tmp转换为word1->word2->word3->...->wordn的形式
    path_single = ""
    for i in range(len(path_single_tmp)):
        path_single += path_single_tmp[i]
        if i != len(path_single_tmp) - 1:
            path_single += "->"
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, path_single)

def gui_calcShortestPathsToAllWords(graph, text_output, entry1):
    path, distance, path_list = graph.calcShortestPathsToAllWords(entry1.get())
    text_output.delete(1.0, tk.END)
    if path_list == []:
        text_output.insert(tk.END, "No such word\n")
        return
    tmp_words = graph.words
    # 对self.words进行去重，保持顺序不变
    graph.words = []
    for i in range(len(tmp_words)):
        if tmp_words[i] not in graph.words:
            graph.words.append(tmp_words[i])
    #遍历path_list，将path_list转换为word1->word2->word3->...->wordn的形式
    for i in range(len(path_list)):
        path_single = ""
        path_single = "Path " + entry1.get() + " to " + graph.words[i] + " :"
        for j in range(len(path_list[i])):
            path_single += path_list[i][j]
            if j != len(path_list[i]) - 1:
                path_single += "->"
        text_output.insert(tk.END, path_single + "\n")

def gui_randomWalk(graph, text_output):
    random_path = graph.randomWalk()
    text_output.delete(1.0, tk.END)
    #将random_path转换为word1->word2->word3->...->wordn的形式
    path_single = ""
    for i in range(len(random_path)):
        path_single += random_path[i]
        path_single += " "
    text_output.insert(tk.END, path_single)
    #将path_single写入文件random_path.txt后面
    with open("random_path.txt", "a") as f:
        f.write(path_single + "\n")

def gui_graph_init(graph, entry3, text_output):
    if entry3.get() == "":
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "Please input a file path\n")
        #读取test_file中的文件目录，输出到text_output中
        file_list = os.listdir("test_file")
        for i in range(len(file_list)):
            text_output.insert(tk.END, "test_file/" + file_list[i] + "\n")
        return
    else:
        graph.__init__(entry3.get())
        text_output.delete(1.0, tk.END)


def gui_showBridgeWords(graph, entry1, entry2, text_output):
    text_output.delete(1.0, tk.END)
    bridge_words = graph.showBridgeWords(entry1, entry2)
    text_output.insert(tk.END, bridge_words)
#gui_showBridgeWords从entry1和entry2中获取参数word1和word2，调用graph.showBridgeWords函数，返回bridge_words，显示在text_output中
def gui_generateNewText(graph, entry1, text_output):
    text_output.delete(1.0, tk.END)
    new_text = graph.generateNewText(entry1)
    text_output.insert(tk.END, new_text)
#gui_generateNewText从entry1中获取参数text，调用graph.generateNewText函数，返回new_text，显示在text_output中


if __name__ == "__main__":
    graph = My_Graph("test_file/test.txt")
    root = tk.Tk()
    root.title("Lab1")
    #获取屏幕宽度和高度
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    #设置窗口宽高为屏幕宽高
    root.geometry("%dx%d" % (screenwidth, screenheight))
    #在窗口上添加三个输入文本框
    label = tk.Label(root, text="word1")
    label.grid(row=0, column=0)
    entry1 = tk.Entry(root, width=50)
    entry1.grid(row=0, column=1)
    label2 = tk.Label(root, text="word2")
    label2.grid(row=0, column=2)
    entry2 = tk.Entry(root, width=50)
    entry2.grid(row=0, column=3)
    label3 = tk.Label(root, text="file path")
    label3.grid(row=0, column=4)
    entry3 = tk.Entry(root, width=50)
    entry3.grid(row=0, column=5)
    # 在窗口上添加一个文本框，显示结果
    text_output = tk.Text(root, width=100, height=50)
    text_output.grid(row=3, column=0, columnspan=6)
    #在窗口上添加五个按钮，一个显示最短路径，一个显示所有最短路径，一个显示随机路径，一个创建有向图，一个展示有向图，点击按钮后调用对应的函数，并保存结果
    button1 = tk.Button(root, text="Show Shortest Path", command=lambda: gui_calcShortestPath(graph, text_output, entry1, entry2))
    button1.grid(row=1, column=0)
    button2 = tk.Button(root, text="Show All Shortest Paths", command=lambda: gui_calcShortestPathsToAllWords(graph, text_output, entry1))
    button2.grid(row=1, column=1)
    button3 = tk.Button(root, text="Show Random Path", command=lambda: gui_randomWalk(graph, text_output))
    button3.grid(row=1, column=2)
    button4 = tk.Button(root, text="Create Directed Graph", command=lambda: gui_graph_init(graph, entry3, text_output))
    button4.grid(row=1, column=3)
    button5 = tk.Button(root, text="Show Directed Graph", command=lambda: graph.showDirectedGraph())
    button5.grid(row=2, column=0)


    #按钮6，查询桥接词
    button6 = tk.Button(root, text="Show Bridge Words", command=lambda: gui_showBridgeWords(graph, entry1.get(), entry2.get(), text_output))
    button6.grid(row=2, column=1)
    #按钮7，根据bridge word生成新文本
    button7 = tk.Button(root, text="Generate New Text", command=lambda: gui_generateNewText(graph, entry1.get(), text_output))
    button7.grid(row=2, column=2)

    #按钮8，退出
    button8 = tk.Button(root, text="Exit", command=root.quit)
    button8.grid(row=2, column=3)

    root.mainloop()
