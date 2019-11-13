# -*- coding: utf-8 -*-

from regex2postfix import *

E = 'epsilon'


class node:
    ID = 0
    ALL_NODES = []

    def __init__(self):
        self.next_nodes = {}
        self.id = node.ID
        # self.is_start = False
        # self.is_end = False

        node.ID += 1
        node.ALL_NODES.append(self)

    def add_next_node(self, path, next_node):
        if path not in self.next_nodes:
            self.next_nodes[path] = []
        self.next_nodes[path].append(next_node)
        return self

    def get_id(self):
        return self.id


class graph:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    # 且运算
    def and_operate(self, other_graph):
        self.end.add_next_node(E, other_graph.start)
        self.end = other_graph.end
        return self

    # 或运算
    def union_operate(self, other_graph):
        temp_start = node()
        temp_end = node()

        temp_start.add_next_node(E, self.start)
        temp_start.add_next_node(E, other_graph.start)

        self.end.add_next_node(E, temp_end)
        other_graph.end.add_next_node(E, temp_end)

        self.start = temp_start
        self.end = temp_end

        return self

    # *运算
    def repeat_operate(self):
        temp_start = node()
        temp_end = node()

        temp_start.add_next_node(E, self.start)
        self.end.add_next_node(E, self.start)
        self.end.add_next_node(E, temp_end)
        temp_start.add_next_node(E, temp_end)

        self.start = temp_start
        self.end = temp_end

        return self


# NFA检查
def out_nfa(nfa):
    print("起点: " + str(nfa.start.get_id()))
    print("终点: " + str(nfa.end.get_id()))

    for i in node.ALL_NODES:
        print(i.get_id())
        for j in i.next_nodes.keys():
            print(" ===" + j, end="===>")
            for k in i.next_nodes[j]:
                print("      " + str(k.get_id()), end=" ")
            print("")


def postfix_2_nfa(regex):
    # graph类型
    stack = []
    for i in regex:
        if i != '$':
            if i not in OPERATOR:
                tmp_start = node()
                tmp_end = node()
                tmp_start.add_next_node(i, tmp_end)
                stack.append(graph(tmp_start, tmp_end))
            elif i in AND_OPERATOR:
                tmp = stack.pop()
                stack.append(stack.pop().and_operate(tmp))
            elif i in UNION_OPERATOR:
                tmp = stack.pop()
                stack.append(stack.pop().union_operate(tmp))
            elif i == '*':
                stack.append(stack.pop().repeat_operate())
    result = stack.pop()
    return result


if __name__ == '__main__':
    Regex = input("Regex :")

    _Regex = add_connector(Regex)
    print(_Regex)

    postfix_Regex = infix_2_postfix(_Regex)
    print(postfix_Regex)

    nfa_Regex = postfix_2_nfa(postfix_Regex)
    out_nfa(nfa_Regex)
