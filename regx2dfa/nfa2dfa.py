#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from postfix2nfa import *
from graphviz import Digraph


def get_closure(index, path, result):
    for i in node.ALL_NODES[index].next_nodes.keys():
        if i == path:
            for j in node.ALL_NODES[index].next_nodes[i]:
                if j not in result:
                    result.add(j.get_id())
                    get_closure(j.get_id(), path, result)
                    get_closure(j.get_id(), E, result)
    return result


def nfa_2_dfa(nfa, alphabet):
    table = []
    state = []
    epsilon_state = get_closure(nfa.start.get_id(), path=E, result=set())
    epsilon_state.add(nfa.start.get_id())
    state.append(epsilon_state)

    index = 0
    for i in state:
        table.append([])
        for j in range(len(alphabet)):
            tmp = set()
            for k in i:
                tmp = tmp | get_closure(k, alphabet[j], set())
            if tmp not in state and len(tmp) != 0:
                state.append(tmp)
            if len(tmp) == 0:
                table[index].append(tmp)
            else:
                table[index].append(tmp)
        index += 1
    return table, state


def get_alphabet(regex):
    result = []
    for i in regex:
        if i not in OPERATOR and i not in result:
            result.append(i)
    return result


def out_dfa(dfa, alphabet, state):
    print(" ", end=" ")
    print(alphabet)
    for index in range(len(dfa)):
        print(state[index], end=" ")
        print(dfa[index])


def dfa_2_mini_dfa(dfa, alphabet, state):
    tmp = []
    new_state = []
    new_dfa = []
    get_id = {}
    get_c = {}

    for index in range(len(state)):
        # 给每个状态编号
        get_id[str(state[index])] = index

    index = 0

    # 干掉输出相同的行
    for i in range(len(dfa)):
        if dfa[i] not in tmp:
            tmp.append(dfa[i])
            get_c[str(dfa[i])] = chr(index + 65)
            new_state.append(chr(index + 65))
            index += 1

    tmp.clear()
    index = 0

    for i in dfa:
        # i 每一行的结果集列表
        if i not in tmp:
            # 找出输出相同的起始状态
            tmp.append(i)
            # tmp_list mini_dfa每一行的转移结构集列表
            tmp_list = []
            for j in i:
                # j是每 1 行的 1 个结果
                if len(j) == 0:
                    # 经过该路径无法转移
                    tmp_list.append(' ')
                else:
                    # 可以转移就放入新的结果集列表
                    tmp_list.append(get_c[str(dfa[get_id[str(j)]])])
            new_dfa.append(tmp_list)
        index += 1
    return new_dfa, new_state


def draw_dfa(dfa, state, regex, alphabet):
    dot = Digraph(comment=regex)

    for i in state:
        dot.node(i, i)

    for index in range(len(dfa)):
        for j in dfa[index]:
            if j != ' ':
                dot.edge(state[index], j, label=alphabet[index])

    dot.format = 'png'
    dot.render('out')


if __name__ == '__main__':
    Regex = input("Regex :")

    _Regex = add_connector(Regex)
    print(_Regex)

    postfix_Regex = infix_2_postfix(_Regex)
    print(postfix_Regex)

    nfa_Regex = postfix_2_nfa(postfix_Regex)
    out_nfa(nfa_Regex)

    alphabet_Regex = get_alphabet(Regex)
    # print(get_closure(nfa_Regex.start.get_id(), E, set()))
    dfa_Regex, State = nfa_2_dfa(nfa_Regex, alphabet_Regex)
    mini_dfa, mini_state = dfa_2_mini_dfa(dfa_Regex, alphabet_Regex, State)

    out_dfa(dfa_Regex, alphabet_Regex, State)
    print(State)

    out_dfa(mini_dfa, alphabet_Regex, mini_state)
    print(mini_state)

    draw_dfa(mini_dfa, mini_state, Regex, alphabet_Regex)
