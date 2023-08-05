# -*- coding: utf-8 -*-

# Author: Daniel Yang <daniel.yj.yang@gmail.com>
#
# License: MIT


from functools import lru_cache
from typing import List, Union
from pyvis.network import Network # see also https://visjs.org/
from pathlib import Path
import webbrowser
from collections import deque


class TreeNode:
    def __init__(self, val: Union[float, int, str] = None, shape: str = "ellipse", color: str = None):
        self.val = val
        self.children = []
        self.grandchildren = []
        self.shape = shape
        self.color = color

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


class tree(object):
    def __init__(self, data: List[Union[float, int, str]] = [], *args, **kwargs):
        """
        https://en.wikipedia.org/wiki/Binary_tree#Arrays
        "Binary trees can also be stored in breadth-first order as an implicit data structure in arrays"
        """
        super().__init__(*args, **kwargs)
        self.treetype = 'Tree'
        self.root = None
        
    def __repr__(self) -> str:
        if self.root:
            return f"TreeNode({self.root.val})"

    def tree_traversals_summary(self):
      self.root = TreeNode('Tree Traversals')
      node_DFS = TreeNode('Depth-First Search\n(DFS)')
      node_BFS = TreeNode('Breadth-First Search\n(BFS)')
      node_BFS_iteration = TreeNode('BFS\nIteration w/ queue')
      node_BFS.children.extend([node_BFS_iteration,])
      node_preorder = TreeNode('Preorder')
      node_inorder = TreeNode('Inorder')
      node_postorder = TreeNode('Postorder')
      node_preorder_iteration = TreeNode('Preorder\nIteration w/ stack')
      node_preorder_recursion = TreeNode('Preorder\nRecursion')
      node_preorder_morris = TreeNode('Preorder\nMorris')
      node_inorder_iteration = TreeNode('Inorder\nIteration w/ stack')
      node_inorder_recursion = TreeNode('Inorder\nRecursion')
      node_inorder_morris = TreeNode('Inorder\nMorris')
      node_postorder_iteration = TreeNode('Postorder\nIteration w/ stack')
      node_postorder_recursion = TreeNode('Postorder\nRecursion')
      node_postorder_morris = TreeNode('Postorder\nMorris')
      node_preorder.children.extend([node_preorder_iteration, node_preorder_recursion, node_preorder_morris])
      node_inorder.children.extend([node_inorder_iteration, node_inorder_recursion, node_inorder_morris])
      node_postorder.children.extend([node_postorder_iteration, node_postorder_recursion, node_postorder_morris])
      node_DFS.children.extend([node_preorder, node_inorder, node_postorder])
      self.root.children.extend([node_DFS, node_BFS])
      self.show(heading='Tree Traversals')

    def validate_IP_address(self):
      self.root = TreeNode('IP string', shape = 'text')
      level1_three_dots = TreeNode('Contains 3 dots', shape='text')
      level1_seven_colons = TreeNode('Contains 7 colons', shape='text')
      level1_neither = TreeNode('Otherwise, return \"Neither\"', shape='text')
      level2_ip4_validate = TreeNode('Validate each \"IPv4\" chunk', shape='text')
      level3_ip4_valid = TreeNode('Valid, return \"IPv4\"', shape='text')
      level3_ip4_invalid = TreeNode('Invalid, return \"Neither\"', shape='text')
      level2_ip6_validate = TreeNode('Validate each \"IPv6\" chunk', shape='text')
      level3_ip6_valid = TreeNode('Valid, return \"IPv6\"', shape='text')
      level3_ip6_invalid = TreeNode('Invalid, return \"Neither\"', shape='text')
      level2_ip4_validate.children.extend([level3_ip4_valid, level3_ip4_invalid])
      level2_ip6_validate.children.extend([level3_ip6_valid, level3_ip6_invalid])
      level1_three_dots.children.extend([level2_ip4_validate])
      level1_seven_colons.children.extend([level2_ip6_validate])
      self.root.children.extend([level1_three_dots, level1_seven_colons, level1_neither])
      self.show(heading='Validate IP Address')

    def word_break_DFS(self, s: str = "catsandog", wordDict: List[str] = ["cats", "dog", "sand", "and", "cat"]) -> bool:
      """
      https://leetcode.com/problems/word-break/
      """
      def is_breakable_DFS(start: int = 0, parent: TreeNode = None):
        nonlocal count
        if start == n:
          curr_node = TreeNode(val=f"#{count}. True", color='lightgreen')
          parent.children.append(curr_node)
          return True
        for end in range(start, n):
            substring = s[start:end+1]
            curr_node = TreeNode(val=f"#{count}. {substring}")
            count += 1
            parent.children.append(curr_node)
            if s[start:end+1] in wordset and is_breakable_DFS(end+1, parent=curr_node):
              return True
        return False
      n = len(s)
      wordset = set(wordDict)
      count = 0
      self.root = TreeNode(val=f"#{count}. {s}")
      count += 1
      res = is_breakable_DFS(start = 0, parent = self.root)
      self.show(heading='DFS Search Space for Word Break')
      return res

    def word_break_BFS(self, s: str = "catsandog", wordDict: List[str] = ["cats", "dog", "sand", "and", "cat"]) -> bool:
      """
      https://leetcode.com/problems/word-break/
      """
      count = 0
      self.root = TreeNode(val=f"#{count}.")
      count += 1
      n = len(s)
      word_set = set(wordDict)
      start_idx_queue = deque()
      start_idx_visited = set()
      start_idx_queue.append((0, self.root))
      res = False
      while start_idx_queue:
        (start, parent_node) = start_idx_queue.popleft()
        if start in start_idx_visited:
          continue
        for end in range(start, n):
          if s[start:end+1] in word_set:
            curr_node = TreeNode(val=f"#{count}. {s[start:end+1]}")
            count += 1
            parent_node.children.append(curr_node)
            start_idx_queue.append((end+1, curr_node))
            if end == n-1:
              leaf_node = TreeNode(val=f"#{count}. True", color='lightgreen')
              curr_node.children.append(leaf_node)
              res = True
              break
        start_idx_visited.add(start)
      self.show(heading='BFS Search Space for Word Break')
      return res

    def Fibonacci_numbers(self, n=5, a=[0, 1], symbol="F", heading="Fibonacci Numbers", distinct=False):
      self.Fibonacci_numbers_generalized(n=n, a=a, symbol=symbol, heading=heading, distinct=distinct)

    def Lucas_numbers(self, n=5, a=[2, 1], symbol="L", heading="Lucas Numbers", distinct=False):
      self.Fibonacci_numbers_generalized(n=n, a=a, symbol=symbol, heading=heading, distinct=distinct)
    
    def Tribonacci_numbers(self, n=5, a=[0, 1, 1], symbol="F", heading="Tribonacci Numbers", distinct=False):
      self.Fibonacci_numbers_generalized(n=n, a=a, symbol=symbol, heading=heading, distinct=distinct)

    def Fibonacci_numbers_generalized(self, n=6, a=[0, 0, 0, 1], symbol="F", heading="Fibonacci Numbers Generalized", distinct=False):
      order = len(a)
      def fib_generalized(n, order=order):
        F = a[:order]
        if n < order:
          return F[n]
        else:
          for i in range(order, n+1):
            F_i = sum(F)
            F[:] = F[1:] + [F_i]
          return F_i
      if distinct:
        child_nodes = [TreeNode(val=f"{symbol}{child_i}={fib_generalized(n=child_i)}") for child_i in range(order)]
        hidden_edges_set = set()
        for child_i in range(order-1, 0, -1):
          child_nodes[child_i].children.append(child_nodes[child_i-1])
          for grandchild_i in range(child_i-1, -1, -1):
            hidden_edges_set.add((id(child_nodes[child_i]), id(child_nodes[grandchild_i])))
        if n >= order:
          for i in range(order, n+1):
            parent_node = TreeNode(val=f"{symbol}{i}={fib_generalized(n=i)}")
            parent_node.children.append(child_nodes[order-1])
            for j in range(order-2, -1, -1):
              parent_node.grandchildren.append(child_nodes[j])
            child_nodes[:] = child_nodes[1:] + [parent_node]
          self.root = parent_node
          self.show(heading=f'Computation Space for {heading} (order={order}), Distinct (n={n})', direction="RL", edge_smooth_type = "curvedCCW", hidden_edges_set = hidden_edges_set)
        else:
          print(f"n={n} should be >= order={order}")
      else:
        self.root = TreeNode(val=f"{symbol}{n}={fib_generalized(n=n)}")
        queue = [(self.root,n),]
        while queue:
          (curr_node, curr_n) = queue.pop()
          for i in range(1, order+1):
            child_n = curr_n - i
            if child_n >= 0:
              child_node = TreeNode(val=f"{symbol}{child_n}={fib_generalized(n=child_n)}")
              curr_node.children.append(child_node)
              if child_n > (order-1):
                queue.append((child_node, child_n))
        self.show(heading=f'{heading} (order={order}) (n={n})')

    def remove_invalid_parenthese(self, s: str = '()())a)b()))'):
      """
      https://leetcode.com/problems/remove-invalid-parentheses/
      """
      def DFS(s='', pair=('(', ')'), anomaly_scan_left_range=0, removal_scan_left_range=0, depth=0, parent: TreeNode = None):
        # phase 1: scanning for anomaly
        stack_size = 0
        for index_i in range(anomaly_scan_left_range, len(s)):
            if s[index_i] == pair[0]:
                stack_size += 1
            elif s[index_i] == pair[1]:
                stack_size -= 1
                if stack_size == -1:
                    break
        if stack_size < 0:
            # phase 2: scanning for removal
            for index_j in range(removal_scan_left_range, index_i+1):
                if s[index_j] == pair[1]:
                    if index_j == removal_scan_left_range or s[index_j-1] != pair[1]:
                        new_s = s[:index_j] + s[(index_j+1):len(s)]
                        # add the node - start
                        if pair[0] == '(':
                          curr_node = TreeNode(val=new_s)
                        else:
                          curr_node = TreeNode(val=new_s[::-1])
                        parent.children.append(curr_node)
                        # add the node - end
                        DFS(s=new_s, pair=pair, anomaly_scan_left_range=index_i, removal_scan_left_range=index_j, depth=depth+1, parent=curr_node)
        elif stack_size > 0:
            # phase 3: reverse scanning
            DFS(s=s[::-1], pair=(')', '('), depth=depth, parent=parent)
        else:
          if pair[0] == '(':
              res.append(s)
          else:
              res.append(s[::-1])
      res = []
      self.root = TreeNode(val=s)
      DFS(s=s, pair=('(', ')'), depth=0, parent=self.root)
      self.show(heading='DFS Search Space for Removing Invalid Parentheses')
      return res

    def show(self, filename: str = 'output.html', heading: str = None, direction: str = "UD", edge_smooth_type: str = False, hidden_edges_set: set = set()):
        if not self.root:
            return
        def dfs_add_child(parent, level=0):
          if parent.children:
            for child in parent.children:
              if child.color:
                g.add_node(n_id=id(child), label=child.val, shape=child.shape, color=child.color, level=level+1, title=f"child node of Node({parent.val}), level={level+1}")
              else:
                g.add_node(n_id=id(child), label=child.val, shape=child.shape,                    level=level+1, title=f"child node of Node({parent.val}), level={level+1}")
              if (id(parent), id(child)) in hidden_edges_set:
                g.add_edge(source=id(parent), to=id(child), hidden = True)
              else:
                g.add_edge(source=id(parent), to=id(child))
              dfs_add_child(child, level=level+1)
        def dfs_add_grandchildren_edge(parent):
          if parent.grandchildren:
            for grandchild in parent.grandchildren:
              if (id(parent), id(grandchild)) in hidden_edges_set:
                g.add_edge(source=id(parent), to=id(grandchild), hidden=True)
              else:
                g.add_edge(source=id(parent), to=id(grandchild))
          if parent.children:
            for child in parent.children:
              dfs_add_grandchildren_edge(child)
        g = Network(width='100%', height='60%')
        g.set_edge_smooth(smooth_type = edge_smooth_type)
        if self.root.color:
          g.add_node(n_id=id(self.root), label=self.root.val, shape=self.root.shape, color=self.root.color, level=0, title=f"root node of the tree, level=0")
        else:
          g.add_node(n_id=id(self.root), label=self.root.val, shape=self.root.shape,                        level=0, title=f"root node of the tree, level=0")
        dfs_add_child(parent=self.root)
        dfs_add_grandchildren_edge(parent=self.root)
        if not heading:
          g.heading = f"{self.treetype}"
        else:
          g.heading = heading
        options = """
var options = {
  "nodes": {
    "font": {
      "size": 20
    }
  },
  "edges": {
    "arrows": {
      "to": {
        "enabled": true
      }
    },
    "color": {
      "inherit": true
    },"""
        if edge_smooth_type:
          options += f"""
    "smooth": {{
        "type": "{edge_smooth_type}",
        "forceDirection": "none"
        }}"""
        else:
          options += """
    "smooth": false"""
        options += """
  },
  "layout": {
    "hierarchical": {
      "enabled": true,"""
        options += f"""
      "direction": "{direction}","""
        options += """
      "sortMethod": "directed"
    }
  },
  "physics": {
    "hierarchicalRepulsion": {
      "centralGravity": 0,
      "springConstant": 0.2,
      "nodeDistance": 150
    },
    "minVelocity": 0.75,
    "solver": "hierarchicalRepulsion"
  },
  "configure": {
      "enabled": true,
      "filter": "layout,physics" 
  }
}"""
        g.set_options(options)
        full_filename = Path.cwd() / filename
        g.write_html(full_filename.as_posix())
        webbrowser.open(full_filename.as_uri(), new = 2)
        return g
