import os
import argparse
import json
from shapely.geometry import Polygon
from anytree import Node, RenderTree, PreOrderIter
from anytree.search import findall, findall_by_attr
from anytree.exporter import DictExporter

from apted import APTED, Config, PerEditOperationConfig
from apted.helpers import Tree

from pprint import pprint
import yaml
import numpy as np

class DocTree():

    def __init__(self, config, log):
        config = yaml.safe_load(open(config['dtree']['config']))
        
        self.unique_fields = config['unique_fields']
        self.duplicatable_fields = config['duplicatable_fields']

        self.text_field = config['text_field']
        self.min_overlap = config['min_overlap']
        self.log = log

    def build_response(self, root):
        # create empty tree to fill
        value = {}
        confidence={}
        coord = {}

        # fill in tree starting with roots (those with no parent)
        self.__export(root, value, value_type='text')
        self.__export(root, confidence, value_type='confidence')
        self.__export(root, coord, value_type='coord')

        rs = {
                'value':value, 
                'confidence':confidence,
                'coord':coord
             }

        return rs
    
    def get_value(self, child, value_type):
        if value_type == 'text':
            value = child.text
        elif value_type == 'confidence':
            value = float(child.prob)
        elif value_type == 'coord':
            value = (child.x, child.y, child.w, child.h)
        
        return value

    def __export(self, root, container, value_type):
        if value_type not in ['text', 'confidence', 'coord']:
            raise ValueError('value_type: {} is not supported'.format(value_type))

        children = sorted(root.children, key=lambda child: child.y)

        for child in children:
            key = child.name
            if child.is_leaf:
                value = self.get_value(child, value_type)
                if key in self.duplicatable_fields:
                    container[key] = container.get(key, [])
                    container[key].append(value)
                else:
                    container[key] = value
            else:
                next_container = {}
                if key in self.duplicatable_fields:
                    container[key] = container.get(key, [])
                    container[key].append(next_container)
                else:
                    container[key] = next_container
                self.__export(child, next_container, value_type)

    def merge(self, node):
        children = sorted(node.children, key=lambda child: child.y)

        # recursive to leaf
        for child in children:
            self.merge(child)
 
        # join content node
        if len(children) > 0 and all(child.name == self.text_field and child.is_leaf for child in children):
            text = [child.text for child in children]
            text = ' '.join(text)
            node.text = text

            for child in children:
                child.parent = None

        # keep only best node in unique_fields
        for unique_node in self.unique_fields:
            nodes = []
            for child in children:
                if child.name == unique_node:
                    nodes.append(child)

            if len(nodes):
                best_node = max(nodes, key=lambda n: n.prob)

                for n in nodes:
                    if n != best_node:
                        n.parent = None

        # uplevel for nested same type node
        is_up = False
        for child in children:
            if child.name == node.name:
                child.parent = node.parent
                is_up = True

        if is_up:
            node.parent = None

    def create_node(self, bd):
        x1, y1, x2, y2 = bd['x'], bd['y'], bd['x'] + bd['w'], bd['y'] + bd['h']
        points = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

        return Polygon(points)

    def score(self, ra, rb):
        a = ra['x'], ra['y'], ra['x'] + ra['w'], ra['y'] + ra['h']
        b = rb['x'], rb['y'], rb['x'] + rb['w'], rb['y'] + rb['h']

        dx = min(a[2], b[2]) - max(a[0], b[0])
        dy = min(a[3], b[3]) - max(a[1], b[1])

        inter_area = 0.0
        if (dx>=0) and (dy>=0):
            inter_area = dx*dy*1.0

        a_area = ra['w']*ra['h']

        return inter_area/a_area

    def get_leaves(self, bds):
        bds = [{**bd, 'index':i} for i, bd in enumerate(bds)]
        root = self.build_tree(bds)
        leaves = root.leaves
        leaves_idx = [leaf.index for leaf in leaves if leaf.index != -1]
        
        return leaves_idx

    def build_tree(self, bds):
        bds = sorted(bds, key=lambda x:x['w']*x['h'])

        root = Node(**{'x': 0, 'y': 0, 'w': 10**6, 'h':10**6, 'name': 'root', 'prob': 0.99, 'index':-1})
                
        nodes = [Node(**bd, parent=root) for bd in bds]

        for i in range(len(bds)):
            recta = bds[i]

            for j in range(i+1, len(bds)):
                rectb = bds[j]
                
                score = self.score(recta, rectb)

                if score > self.min_overlap:
                    nodes[i].parent = nodes[j]
                    break

        return root
    
    def bracket(self, node):
        """Show tree using brackets notation"""
        result = str(node.name)
        children = sorted(node.children, key=lambda n:n.name)
        for child in children:
            result += self.bracket(child)
        return "{{{}}}".format(result)

    def edit_distance(self, boxes1, boxes2):
        tree1 = self.build_tree(boxes1)
        self.merge(tree1)

        tree2 = self.build_tree(boxes2)
        self.merge(tree2)

        tree1 = Tree.from_text(self.bracket(tree1))
        tree2 = Tree.from_text(self.bracket(tree2))

        apted = APTED(tree1, tree2, PerEditOperationConfig(1,1,1))
        ted = apted.compute_edit_distance()

        return ted

    def build_layout(self, bds):
        """
        bds: array, {x, y, w, h, prob, name, text}
        """
        root = self.build_tree(bds)
        self.merge(root)
    
        if self.log:
            print(RenderTree(root))
       
        rs = self.build_response(root)

        return rs
