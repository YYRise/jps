#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
# sys.path.append("..")
import json
import math
# 地图数据；0：能通过；1:障碍，不能通过
map_test = [[0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            ]

# 可行走方向
g_dir = [[1, 0], [0, 1], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
class Node:
    def __init__(self, parent, pos, g, h):
        self.parent = parent
        self.pos = pos
        self.g = g
        self.h = h
        self.f = g + h
    def get_direction(self):
        return self.parent and [self.pos[0] != self.parent.pos[0] and (self.pos[0] - self.parent.pos[0]) / abs(self.pos[0] - self.parent.pos[0]) or 0, self.pos[1] != self.parent.pos[1] and (self.pos[1] - self.parent.pos[1]) / abs(self.pos[1] - self.parent.pos[1]) or 0] or [0, 0]

# test_map = []
class JPS:

    # 注意w,h两个参数，如果你修改了地图，需要传入一个正确值或者修改这里的默认参数
    def __init__(self, width, height):
        self.s_pos = None
        self.e_pos = Node

        self.width = width
        self.height = height
        self.open = []
        self.close = []
        self.path = []

    def prune_neighbours(self, c):
        nbs = []
         # 不是起始点
        if c.parent:
            # 进入的方向
            dir = c.get_direction()
            if self.is_pass(c.pos[0] + dir[0], c.pos[1] + dir[1]):
                nbs.append([c.pos[0] + dir[0], c.pos[1] + dir[1]])
            print "dir = ", dir
             # 对角线行走; eg:右下(1, 1)
            if dir[0] != 0 and dir[1] != 0:
                # 下（0， 1）
                if self.is_pass(c.pos[0], c.pos[1] + dir[1]):
                    nbs.append([c.pos[0], c.pos[1] + dir[1]])
                 # 右（1， 0）
                if self.is_pass(c.pos[0]+dir[0], c.pos[1]):
                    nbs.append([c.pos[0]+dir[0], c.pos[1]])
                 # 左不能走且下可走
                if not self.is_pass(c.pos[0] - dir[0], c.pos[1]) and self.is_pass(c.pos[0], c.pos[1] + dir[1]):
                    # 左下（-1， 1）
                    nbs.append([c.pos[0] - dir[0], c.pos[1] + dir[1]])
                 # 上不能走且右可走
                if not self.is_pass(c.pos[0], c.pos[1]-dir[1]) and self.is_pass(c.pos[0]+dir[0], c.pos[1]):
                    # 右上（1， -1）
                    nbs.append([c.pos[0]+dir[0], c.pos[1]-dir[1]])
            else:  # 直行
                # 垂直走
                if dir[0] == 0:
                     # 右不能走
                    if not self.is_pass(c.pos[0]+1, c.pos[1]):
                        # 右下
                        nbs.append([c.pos[0]+1, c.pos[1]+dir[1]])
                     # 左不能走
                    if not self.is_pass(c.pos[0]-1, c.pos[1]):
                        # 左下
                        nbs.append([c.pos[0]-1, c.pos[1]+dir[1]])

                else:  # 水平走，向右走为例                     
                     # 下不能走
                    if not self.is_pass(c.pos[0], c.pos[1]+1):
                         # 右下
                         nbs.append([c.pos[0]+dir[0], c.pos[1]+1])
                     # 上不能走
                    if not self.is_pass(c.pos[0], c.pos[1]-1):
                         # 右上
                         nbs.append([c.pos[0]+dir[0], c.pos[1]-1])

        else:
            for d in g_dir:
                if self.is_pass(c.pos[0] + d[0], c.pos[1] + d[1]):
                    nbs.append([c.pos[0] + d[0], c.pos[1] + d[1]])
        print "prune_neighbours c= %s, nbs = %s" % ([c.pos[0], c.pos[1]], nbs)
        return nbs
    # ↑ ↓ ← → ↖ ↙ ↗ ↘
    def jump_node(self, now, pre):
        dir = [a != b and (a - b)/abs(a-b) or 0 for a, b in zip(now, pre)]
        print "now = %s, pre = %s, dir = %s" %(now, pre, dir)        

        if now == self.e_pos:
            return now

        if self.is_pass(now[0], now[1]) is False:
            return None
        if dir[0] != 0 and dir[1] != 0:
            # 左下能走且左不能走，或右上能走且上不能走
            if (self.is_pass(now[0] - dir[0], now[1] + dir[1]) and not self.is_pass(now[0]-dir[0], now[1])) or (self.is_pass(now[0] + dir[0], now[1] - dir[1]) and not self.is_pass(now[0], now[1]-dir[1])):
                return now
        else:
            # 水平方向
            if dir[0] != 0:
                # 右下能走且下不能走， 或右上能走且上不能走
                '''
                * 1 0       0 0 0
                0 → 0       0 0 0
                * 1 0       0 0 0
                
                '''
                print '水平方向:', self.is_pass(now[0] + dir[0], now[1] + 1), self.is_pass(now[0], now[1]+1), self.is_pass(now[0] + dir[0], now[1] - 1), self.is_pass(now[0], now[1]-1)
                if (self.is_pass(now[0] + dir[0], now[1] + 1) and not self.is_pass(now[0], now[1]+1)) or (self.is_pass(now[0] + dir[0], now[1] - 1) and not self.is_pass(now[0], now[1]-1)):
                    return now
            else: # 垂直方向
                # 右下能走且右不能走，或坐下能走且左不能走
                '''
                0 0 0
                1 ↓ 1
                0 0 0
                                
                '''
                print '垂直方向:', self.is_pass(now[0] + 1, now[1] + dir[1]), self.is_pass(now[0] + 1, now[1]), self.is_pass(now[0]-1 , now[1] + dir[1]), self.is_pass(now[0] - 1, now[1])
                if (self.is_pass(now[0] + 1, now[1] + dir[1]) and not self.is_pass(now[0]+1, now[1])) or (self.is_pass(now[0] - 1, now[1] + dir[1]) and not self.is_pass(now[0]-1, now[1])):
                    return now

        if dir[0] != 0 and dir[1] != 0:
            t1 = self.jump_node([now[0]+dir[0], now[1]], now)
            t2 = self.jump_node([now[0], now[1] + dir[1]], now)
            if t1 or t2:
                return now
        if self.is_pass(now[0] + dir[0], now[1]) or self.is_pass(now[0], now[1] + dir[1]):
            t = self.jump_node([now[0] + dir[0], now[1] + dir[1]], now)
            if t:
                return t

        return None

    def extend_round(self, c):
        nbs = self.prune_neighbours(c)
        print "************[%d, %d] --- %s, parent = [%d, %d]" % (c.pos[0], c.pos[1], nbs, c.pos[0], c.pos[1])
        for n in nbs:
            jp = self.jump_node(n,[c.pos[0], c.pos[1]])
            print "expandSuccessors:parent = %s, nb = %s, jp = %s" % ([c.pos[0], c.pos[1]], n, jp)
            if jp:
                if self.node_in_close(jp):
                    continue
                g = self.get_g(jp, c.pos)
                h = self.get_h(jp, self.e_pos)
                node = Node(c, jp, c.g + g, h)
                i = self.node_in_open(node)
                if i != -1:
                    # 新节点在开放列表
                    if self.open[i].g > node.g:
                        # 现在的路径到比以前到这个节点的路径更好~
                        # 则使用现在的路径
                        self.open[i].parent = c
                        self.open[i].g = node.g
                        self.open[i].f = node.g + self.open[i].h
                    continue
                self.open.append(node)

    def is_pass(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height and (map_test[x][y] != 1 or [x, y] == self.e_pos)

    # 查找路径的入口函数
    def find_path(self, s_pos, e_pos):
        self.s_pos, self.e_pos = s_pos, e_pos
        # 构建开始节点
        p = Node(None, self.s_pos, 0, abs(self.s_pos[0]-self.e_pos[0]) + abs(self.s_pos[1]-self.e_pos[1]))
        self.open.append(p)
        while True:
            # 扩展F值最小的节点

            # 如果开放列表为空，则不存在路径，返回
            if not self.open:
                return "not find"
            # 获取F值最小的节点
            idx, p = self.get_min_f_node()
            print("find path with extend_round(%d, %d), open_list = %s" % (p.pos[0], p.pos[1], [[n.pos[0], n.pos[1]] for n in self.open]))
            # 找到路径，生成路径，返回
            if self.is_target(p):
                self.make_path(p)
                return
            self.extend_round(p)
            # 把此节点压入关闭列表，并从开放列表里删除
            self.close.append(p)
            del self.open[idx]

    def make_path(self, p):
        # 从结束点回溯到开始点，开始点的parent == None
        while p:

            if p.parent:
                dir = p.get_direction()
                n = p.pos
                while n != p.parent.pos:
                    self.path.append(n)
                    n = [n[0] - dir[0], n[1] - dir[1]]
            else:
                self.path.append(p.pos)
            p = p.parent
        self.path.reverse()
    def is_target(self, n):
        return n.pos == self.e_pos

    def get_min_f_node(self):
        best = None
        bv = -1
        bi = -1
        for idx, node in enumerate(self.open):
            # value = self.get_dist(i)  # 获取F值
            if bv == -1 or node.f < bv:  # 比以前的更好，即F值更小
                best = node
                bv = node.f
                bi = idx
        return bi, best
    # 计算g值；直走=1；斜走=1.4
    def get_g(self, pos1, pos2):
        if pos1[0] == pos2[0]:
            return abs(pos1[1] - pos2[1])
        elif pos1[1] == pos2[1]:
            return abs(pos1[0] - pos2[0])
        else:
            return abs(pos1[0] - pos2[0]) * 1.4
    # 计算h值
    def get_h(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def node_in_close(self, node):
        for i in self.close:
            if node == i.pos:
                return True
        return False

    def node_in_open(self, node):
        for i, n in enumerate(self.open):
            if node == n.pos:
                return i
        return -1

    def get_searched(self):
        l = []
        for i in self.open:
            l.append((i.pos[0], i.pos[1]))
        for i in self.close:
            l.append((i.pos[0], i.pos[1]))
        return l

    def print_path(self):
        for n in self.path:
            map_test[n[0]][n[1]] = 6

        print '------------------------------'
        for ns in map_test:
            print ''.join(str(ns))

def find_path(s_pos, e_pos):
    jps = JPS(7, 7)
    err = jps.find_path(s_pos, e_pos)
    searched = jps.get_searched()
    path = jps.path
    print "path length is %d" % (len(path))
    print "searched %s" % (searched)
    print "err = ", err
    # print(path)
    # print(json.dumps(jps.map_data.data))
    if len(path) > 0:
        print("find_path, start_pos:%s" % s_pos, "end_pos:%s" % e_pos, "path = ",
                json.dumps(path), "len(path) = ", len(path), "len(searched) = ", len(searched))
    else:
        print("find_path not find path, start_pos:%s" % s_pos, "end_pos:%s" % e_pos,
                "len(searched) = ", len(searched))
    jps.print_path()
    return path, err


def check_pos_valid(x, y):
    jps = JPS(None, x, y, x, y)
    return jps.is_valid_coord(x, y)


if __name__ == "__main__":
    # tilemap.tile_manager.load("../maps/")
    # find_path(MAP_CONFIG_NAME, 23, 19, 25, 19)
    find_path([0, 0], [1, 3])
