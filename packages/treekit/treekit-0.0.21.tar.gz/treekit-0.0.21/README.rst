.. -*- mode: rst -*-

|BuildTest|_ |PyPi|_ |License|_ |Downloads|_ |PythonVersion|_

.. |BuildTest| image:: https://travis-ci.com/daniel-yj-yang/treekit.svg?branch=main
.. _BuildTest: https://app.travis-ci.com/github/daniel-yj-yang/treekit

.. |PythonVersion| image:: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue
.. _PythonVersion: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue

.. |PyPi| image:: https://img.shields.io/pypi/v/treekit
.. _PyPi: https://pypi.python.org/pypi/treekit

.. |Downloads| image:: https://pepy.tech/badge/treekit
.. _Downloads: https://pepy.tech/project/treekit

.. |License| image:: https://img.shields.io/pypi/l/treekit
.. _License: https://pypi.python.org/pypi/treekit


=====================================================
Library for Studying and Applying Tree Data Structure
=====================================================

Installation
------------

.. code-block::

   pip install treekit


Sample Usage
------------

>>> from treekit import binarytree
>>> bt1 = binarytree([13, 3, 14, 0, 4, None, None, None, 2, None, 7]) # data array in breadth-first order, see: https://en.wikipedia.org/wiki/Binary_tree#Arrays
>>> bt1.show() # this will create an output.html and open a tab in web browser to view it
>>> bt1.height
3
>>> bt1.inorder # bt.preorder # bt.postorder # bt.levelorder
[0, 2, 3, 4, 7, 13, 14]
>>> bt1.preorder
[13, 3, 0, 2, 4, 7, 14]
>>> bt1.diameter()
The sum of depths from the left and right subtrees of Node(3) is 4
4
>>> bt1.flatten(target="preorder", inplace=True)
>>> bt1.inorder
[13, 3, 0, 2, 4, 7, 14]
>>> bt1.preorder
[13, 3, 0, 2, 4, 7, 14]
>>> bt1.find_maximum_path_sum()
(43, Node(13))

>>> from treekit import binarytree
>>> bt2 = binarytree()
>>> bt2.compact_build([4, -7, -3, None, None, 8, -4, 9, -7, -4, None, 6, None, -1, -6, None, None, 0, 6, 7, None, 11, None, None, -1, -4, None, None, None, -2, None, -3])
>>> bt2.show() # this will create an output.html and open a tab in web browser to view it
>>> bt2.diameter()
The sum of depths from the left and right subtrees of Node(8) is 9
9

>>> from treekit import tree
>>> t1 = tree()
>>> t1.remove_invalid_parenthese('()())a)b()))')
['((ab()))', '((a)b())', '(()ab())', '(()a)b()', '(())ab()', '()(ab())', '()(a)b()', '()()ab()']
>>> t1.Fibonacci_numbers(n=5, a=[0, 1])
>>> t1.Fibonacci_numbers(n=5, a=[0, 1], distinct=True)
>>> t1.Lucas_numbers(n=5)
>>> t1.Fibonacci_numbers_generalized(n=15, a=[0]*7+[1], distinct=True)
>>> t1.word_break_DFS(s = "catsanddog", wordDict = ["cats", "dog", "sand", "and", "cat"])
>>> t1.word_break_BFS(s = "catsanddog", wordDict = ["cats", "dog", "sand", "and", "cat"])

>>> from treekit import tree
>>> t2 = tree()
>>> t2.tree_traversals_summary()
>>> t2.validate_IP_address()

>>> from treekit import bst
>>> bst1 = bst(h=4)
>>> bst1.show()

------------

Screenshot 1: Binary Search Tree, height = 4
--------------------------------------------
|image1|

------------

Screenshot 2: DFS Search Space for Removing Invalid Parentheses
---------------------------------------------------------------
|image2|

------------

Screenshot 3a: Computation Space for Fibonacci Numbers (n=5, order=2)
---------------------------------------------------------------------
|image3a|

------------

Screenshot 3b: Computation Space for Fibonacci Numbers Generalized (n=15, order=8)
----------------------------------------------------------------------------------
|image3b|

------------

Screenshot 4: DFS Search Space for Work Break
---------------------------------------------
|image4|


.. |image1| image:: https://github.com/daniel-yj-yang/treekit/raw/main/treekit/examples/BST_height=4.png
.. |image2| image:: https://github.com/daniel-yj-yang/treekit/raw/main/treekit/examples/Remove_Invalid_Parentheses.png
.. |image3a| image:: https://github.com/daniel-yj-yang/treekit/raw/main/treekit/examples/Fibonacci_Numbers_n=5.png
.. |image3b| image:: https://github.com/daniel-yj-yang/treekit/raw/main/treekit/examples/Fibonacci_Numbers_Generalized_n=15_order=8.png
.. |image4| image:: https://github.com/daniel-yj-yang/treekit/raw/main/treekit/examples/Word_Break_DFS_Search_Space.png

