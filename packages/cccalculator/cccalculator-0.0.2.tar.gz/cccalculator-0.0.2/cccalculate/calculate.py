from tree_sitter import Language, Parser
import multiprocessing as mp
import os
from multiprocessing.pool import Pool

import sys

__version__ = '0.0.2'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SO_FILE = os.path.join(BASE_DIR,'cccalculate','lang_build','my-languages.so')
VENDOR_FILE = os.path.join(BASE_DIR,'cccalculate','vendor','tree-sitter-python')
Language.build_library(
  SO_FILE,
  [VENDOR_FILE]
)

PY_LANGUAGE = Language(SO_FILE, 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

class MccabeFactory(object):
    """go through every node of AST to record each node"""
    def __init__(self):
        # last processed verticle
        self.end_verticle = None
        self.edge_list = []
        self.edge = None

    def add_to_path(self, verticle):
        # todo: add commit
        if not self.end_verticle:
            return
        self.edge.link_verticles(self.end_verticle, verticle)
        self.end_verticle = verticle

    def visit_statement(self,node):
        node_name = node.type
        visit_func = getattr(self, node_name+'_visitor',self.linear_statement_visitor)
        return visit_func(node)

    def do_visit(self,tree):
        self.visit_statement(tree.root_node)


    def class_definition_visitor(self,node):
        line_start = node.start_point[0] + 1
        class_name = 'class:{}'.format(line_start)
        for inode in node.children:
            if inode.type == 'block':
                for iinode in inode.children:
                    if iinode.type == 'function_definition':
                        self.function_definition_visitor(iinode, class_name=class_name)

    def function_definition_visitor(self, node,class_name=None):
        line_start = node.start_point[0] + 1
        fun_name = 'fun:{}'.format(line_start)
        if class_name:
            fun_name = class_name + '--' + fun_name
        fun_verticle = Verticle(fun_name)
        self.edge = Edge(fun_name)
        self.end_verticle = fun_verticle
        self.block_visitor(node)
        self.end_verticle = None
        self.edge_list.append(self.edge)
        self.edge = None

    def module_visitor(self, node):
        for inode in node.children:
            self.visit_statement(inode)

    children_visitor = module_visitor

    def with_statement_visitor(self, node):
        if self.edge == None:
            return
        line_start = node.start_point[0] + 1
        name = 'with:{}'.format(line_start)
        with_verticle = Verticle(name)
        self.add_to_path(with_verticle)
        self.block_visitor(node)

    def block_visitor(self, node):
        for inode in node.children:
            if inode.type == 'block':
                self.children_visitor(inode)
    def if_statement_visitor(self, node):
        if self.edge == None:
            return
        line_start = node.start_point[0] + 1
        name = 'if:{}'.format(line_start)
        if_verticle = Verticle(name)
        if not self.end_verticle:
            self.end_verticle = if_verticle
        else:
            self.add_to_path(if_verticle)
        self.if_block_visitor(if_verticle, node)

    def if_block_visitor(self, begin_verticle, node):
        final_verticle = Verticle('')
        possible_end = [begin_verticle]
        for inode in node.children:
            if inode.type == 'block':
                self.children_visitor(inode)
                possible_end.append(self.end_verticle)
            if inode.type == 'elif_clause':
                self.end_verticle = begin_verticle
                self.block_visitor(inode)
                possible_end.append(self.end_verticle)
            if inode.type == 'else_clause':
                self.end_verticle = begin_verticle
                self.block_visitor(inode)
                possible_end.append(self.end_verticle)
                # if the 'if' statement has 'else' statement, the 'if' statement no longer need to be linked to the final verticel
                possible_end = possible_end[1:]
        for iend in possible_end:
            self.edge.link_verticles(iend, final_verticle)
        self.end_verticle = final_verticle

    def try_block_visitor(self, begin_verticle, node):
        final_verticle = Verticle('')
        possible_end = []
        for inode in node.children:
            if inode.type == 'block':
                self.children_visitor(inode)
                possible_end.append(self.end_verticle)
            if inode.type == 'except_clause':
                self.end_verticle = begin_verticle
                self.block_visitor(inode)
                possible_end.append(self.end_verticle)
        for iend in possible_end:
            self.edge.link_verticles(iend, final_verticle)
        self.end_verticle = final_verticle

    def try_statement_visitor(self, node):
        if self.edge == None:
            return
        line_start = node.start_point[0] + 1
        name = 'try:{}'.format(line_start)
        try_verticle = Verticle(name)
        if not self.end_verticle:
            self.end_verticle = try_verticle
        else:
            self.add_to_path(try_verticle)
        self.try_block_visitor(try_verticle, node)

    def linear_statement_visitor(self, node):
        if self.edge == None:
            return
        line_start = node.start_point[0] + 1
        name = 'simple:{}'.format(line_start)
        sim_verticle = Verticle(name)
        self.add_to_path(sim_verticle)

    def while_statement_visitor(self, node):
        if self.edge == None:
            return
        line_start = node.start_point[0] + 1
        name = 'while:{}'.format(line_start)
        while_verticle = Verticle(name)
        if not self.end_verticle:
            self.end_verticle = while_verticle
        else:
            self.add_to_path(while_verticle)
        self.block_visitor(node)
        final_verticle = Verticle('')
        self.edge.link_verticles(self.end_verticle, final_verticle)
        self.edge.link_verticles(while_verticle, final_verticle)

    def for_statement_visitor(self, node):
        if self.edge == None:
            return
        line_start = node.start_point[0] + 1
        name = 'for:{}'.format(line_start)
        for_verticle = Verticle(name)
        if not self.end_verticle:
            self.end_verticle = for_verticle
        else:
            self.add_to_path(for_verticle)
        self.block_visitor(node)
        final_verticle = Verticle('')
        self.edge.link_verticles(self.end_verticle, final_verticle)
        self.edge.link_verticles(for_verticle, final_verticle)
        self.end_verticle = final_verticle


class Verticle(object):
    def __init__(self,name):
      self.name = name


class Edge(object):
    """the edge_verticle dictionary records the verticles and edges of the python file.
        keys of edge_verticle are all the verticles.
        value of each key represents all the possible next verticles of the key.
    """
    def __init__(self,name):
        self.name = name
        self.edge_verticle = {}

    def link_verticles(self,v1,v2):
        self.edge_verticle.setdefault(v1,[]).append(v2)
        self.edge_verticle[v2] = []

    def compute_complex(self):
        # You can print the edge_verticle dictionary to see the flow graph
        # for key,value in self.edge_verticle.items():
        #     print('key--{}, value--{}'.format(key.name,[i.name for i in value]))
        nodes = len(self.edge_verticle)
        edges = sum([len(i) for i in self.edge_verticle.values()])
        return edges-nodes+2

def do_calculate(file_name,lock):
    code = read_file(file_name)
    tree = parser.parse(bytes(code, "utf8"))
    visitor = MccabeFactory()
    visitor.do_visit(tree)
    if not lock:
        print(file_name + '\n')
        for iedge in visitor.edge_list:
            print('   ' + iedge.name + '----------' + str(iedge.compute_complex())+'\n')
    else:
        lock.acquire()
        print(file_name + '\n')
        for iedge in visitor.edge_list:
            print('   ' + iedge.name + '----------' + str(iedge.compute_complex()) + '\n')
        lock.release()

def do_calculate_from_code(code):
    tree = parser.parse(bytes(code, "utf8"))
    visitor = MccabeFactory()
    visitor.do_visit(tree)
    return [iedge.compute_complex() for iedge in visitor.edge_list]

def do_calculate_from_directory(file_path):
    file_list = []
    for _, _, files in os.walk(file_path):
        for ifile in files:
            if ifile.endswith('.py'):
                file_list.append(os.path.join(file_path, ifile))
    worker_nums = mp.cpu_count()
    p = Pool(worker_nums)
    manager = mp.Manager()
    lock = manager.Lock()
    for ifile in file_list:
        p.apply_async(do_calculate, args=(ifile,lock))
    p.close()
    p.join()


def main(argvs):
    file_path = argvs[0]
    file_list = []
    for _,_,files in os.walk(file_path):
        for ifile in files:
            if ifile.endswith('.py'):
                file_list.append(os.path.join(file_path,ifile))
    worker_nums = mp.cpu_count()
    manager = mp.Manager()
    lock = manager.Lock()
    p = Pool(worker_nums)
    for ifile in file_list:
        p.apply_async(do_calculate, args=(ifile,lock))
    p.close()
    p.join()

if __name__ == '__main__':
    main(sys.argv[1:])