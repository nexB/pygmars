# Originally based on: Natural Language Toolkit
# substantially modified for use in ScanCode-toolkit
#
# Natural Language Toolkit (NLTK)
# Copyright (C) 2001-2020 NLTK Project
# SPDX-License-Identifier: Apache-2.0
# URL: <http://nltk.org/>
"""
===============================
 Unit tests for pygmars.tree.Tree
===============================

    >>> from pygmars.tree import *

Some trees to run tests on:

    >>> dp1 = Tree('dp', [Tree('d', ['the']), Tree('np', ['dog'])])
    >>> dp2 = Tree('dp', [Tree('d', ['the']), Tree('np', ['cat'])])
    >>> vp = Tree('vp', [Tree('v', ['chased']), dp2])
    >>> tree = Tree('s', [dp1, vp])
    >>> print(tree)
    (s (dp (d the) (np dog)) (vp (v chased) (dp (d the) (np cat))))

The node label is accessed using the `label()` method:

    >>> dp1.label(), dp2.label(), vp.label(), tree.label()
    ('dp', 'dp', 'vp', 's')

    >>> print(tree[1,1,1,0])
    cat

The `treepositions` method returns a list of the tree positions of
subtrees and leaves in a tree.  By default, it gives the position of
every tree, subtree, and leaf, in prefix order:

    >>> print(tree.treepositions())
    [(), (0,), (0, 0), (0, 0, 0), (0, 1), (0, 1, 0), (1,), (1, 0), (1, 0, 0), (1, 1), (1, 1, 0), (1, 1, 0, 0), (1, 1, 1), (1, 1, 1, 0)]


Trees can be initialized from treebank strings:

    >>> tree2 = Tree.fromstring('(S (NP I) (VP (V enjoyed) (NP my cookie)))')
    >>> print(tree2)
    (S (NP I) (VP (V enjoyed) (NP my cookie)))

Trees can be compared for equality:

    >>> tree == Tree.fromstring(str(tree))
    True
    >>> tree2 == Tree.fromstring(str(tree2))
    True
    >>> tree == tree2
    False
    >>> tree == Tree.fromstring(str(tree2))
    False
    >>> tree2 == Tree.fromstring(str(tree))
    False

    >>> tree != Tree.fromstring(str(tree))
    False
    >>> tree2 != Tree.fromstring(str(tree2))
    False
    >>> tree != tree2
    True
    >>> tree != Tree.fromstring(str(tree2))
    True
    >>> tree2 != Tree.fromstring(str(tree))
    True

    >>> tree < tree2 or tree > tree2
    True

Tree Parsing
============

The class method `Tree.fromstring()` can be used to parse trees, and it
provides some additional options.

    >>> tree = Tree.fromstring('(S (NP I) (VP (V enjoyed) (NP my cookie)))')
    >>> print(tree)
    (S (NP I) (VP (V enjoyed) (NP my cookie)))

When called on a subclass of `Tree`, it will create trees of that
type:

    >>> tree = ImmutableTree.fromstring('(VP (V enjoyed) (NP my cookie))')
    >>> print(tree)
    (VP (V enjoyed) (NP my cookie))
    >>> print(type(tree))
    <class 'pygmars.tree.ImmutableTree'>
    >>> tree[1] = 'x'
    Traceback (most recent call last):
      . . .
    ValueError: ImmutableTree may not be modified
    >>> del tree[0]
    Traceback (most recent call last):
      . . .
    ValueError: ImmutableTree may not be modified

The ``brackets`` parameter can be used to specify two characters that
should be used as brackets:

    >>> print(Tree.fromstring('[S [NP I] [VP [V enjoyed] [NP my cookie]]]',
    ...                  brackets='[]'))
    (S (NP I) (VP (V enjoyed) (NP my cookie)))
    >>> print(Tree.fromstring('<S <NP I> <VP <V enjoyed> <NP my cookie>>>',
    ...                  brackets='<>'))
    (S (NP I) (VP (V enjoyed) (NP my cookie)))

If ``brackets`` is not a string, or is not exactly two characters,
then `Tree.fromstring` raises an exception:

    >>> Tree.fromstring('<VP <V enjoyed> <NP my cookie>>', brackets='')
    Traceback (most recent call last):
      . . .
    TypeError: brackets must be a length-2 string
    >>> Tree.fromstring('<VP <V enjoyed> <NP my cookie>>', brackets='<<>>')
    Traceback (most recent call last):
      . . .
    TypeError: brackets must be a length-2 string
    >>> Tree.fromstring('<VP <V enjoyed> <NP my cookie>>', brackets=12)
    Traceback (most recent call last):
      . . .
    TypeError: brackets must be a length-2 string
    >>> Tree.fromstring('<<NP my cookie>>', brackets=('<<','>>'))
    Traceback (most recent call last):
      . . .
    TypeError: brackets must be a length-2 string

We may add support for multi-character brackets in the future, in
which case the ``brackets=('<<','>>')`` example would start working.
Whitespace brackets are not permitted:

    >>> Tree.fromstring('(NP my cookie\\n',brackets='(\\n')
    Traceback (most recent call last):
      . . .
    TypeError: whitespace brackets not allowed

If an invalid tree is given to Tree.fromstring, then it raises a
ValueError, with a description of the problem:

    >>> Tree.fromstring('(NP my cookie) (NP my milk)')
    Traceback (most recent call last):
      . . .
    ValueError: Tree.read(): expected 'end-of-string' but got '(NP'
                at index 15.
                    "...y cookie) (NP my mil..."
                                  ^
    >>> Tree.fromstring(')NP my cookie(')
    Traceback (most recent call last):
      . . .
    ValueError: Tree.read(): expected '(' but got ')'
                at index 0.
                    ")NP my coo..."
                     ^
    >>> Tree.fromstring('(NP my cookie))')
    Traceback (most recent call last):
      . . .
    ValueError: Tree.read(): expected 'end-of-string' but got ')'
                at index 14.
                    "...my cookie))"
                                  ^
    >>> Tree.fromstring('my cookie)')
    Traceback (most recent call last):
      . . .
    ValueError: Tree.read(): expected '(' but got 'my'
                at index 0.
                    "my cookie)"
                     ^
    >>> Tree.fromstring('(NP my cookie')
    Traceback (most recent call last):
      . . .
    ValueError: Tree.read(): expected ')' but got 'end-of-string'
                at index 13.
                    "... my cookie"
                                  ^
    >>> Tree.fromstring('')
    Traceback (most recent call last):
      . . .
    ValueError: Tree.read(): expected '(' but got 'end-of-string'
                at index 0.
                    ""
                     ^

Trees with no children are supported:

    >>> print(Tree.fromstring('(S)'))
    (S )
    >>> print(Tree.fromstring('(X (Y) (Z))'))
    (X (Y ) (Z ))

Trees with an empty node label and no children are supported:

    >>> print(Tree.fromstring('()'))
    ( )
    >>> print(Tree.fromstring('(X () ())'))
    (X ( ) ( ))

Trees with an empty node label and children are supported, but only if the
first child is not a leaf (otherwise, it will be treated as the node label).

    >>> print(Tree.fromstring('((A) (B) (C))'))
    ( (A ) (B ) (C ))
    >>> print(Tree.fromstring('((A) leaf)'))
    ( (A ) leaf)
    >>> print(Tree.fromstring('(((())))'))
    ( ( ( ( ))))

The optional arguments `read_node` and `read_leaf` may be used to
transform the string values of nodes or leaves.

    >>> print(Tree.fromstring('(A b (C d e) (F (G h i)))',
    ...                  read_node=lambda s: '<%s>' % s,
    ...                  read_leaf=lambda s: '"%s"' % s))
    (<A> "b" (<C> "d" "e") (<F> (<G> "h" "i")))


The optional argument ``remove_empty_top_bracketing`` can be used to
remove any top-level empty bracketing that occurs.

    >>> print(Tree.fromstring('((S (NP I) (VP (V enjoyed) (NP my cookie))))',
    ...                  remove_empty_top_bracketing=True))
    (S (NP I) (VP (V enjoyed) (NP my cookie)))

It will not remove a top-level empty bracketing with multiple children:

    >>> print(Tree.fromstring('((A a) (B b))'))
    ( (A a) (B b))

Parented Trees
==============
`ParentedTree` is a subclass of `Tree` that automatically maintains
parent pointers for single-parented trees.  Parented trees can be
created directly from a node label and a list of children:

    >>> ptree = (
    ...     ParentedTree('VP', [
    ...         ParentedTree('VERB', ['saw']),
    ...         ParentedTree('NP', [
    ...             ParentedTree('DET', ['the']),
    ...             ParentedTree('NOUN', ['dog'])])]))
    >>> print(ptree)
    (VP (VERB saw) (NP (DET the) (NOUN dog)))

Parented trees can be created from strings using the classmethod
`ParentedTree.fromstring`:

    >>> ptree = ParentedTree.fromstring('(VP (VERB saw) (NP (DET the) (NOUN dog)))')
    >>> print(ptree)
    (VP (VERB saw) (NP (DET the) (NOUN dog)))
    >>> print(type(ptree))
    <class 'pygmars.tree.ParentedTree'>

Parented trees can also be created by using the classmethod
`ParentedTree.convert` to convert another type of tree to a parented
tree:

    >>> tree = Tree.fromstring('(VP (VERB saw) (NP (DET the) (NOUN dog)))')
    >>> ptree = ParentedTree.convert(tree)
    >>> print(ptree)
    (VP (VERB saw) (NP (DET the) (NOUN dog)))
    >>> print(type(ptree))
    <class 'pygmars.tree.ParentedTree'>

.. clean-up:

    >>> del tree

`ParentedTree`\ s should never be used in the same tree as `Tree`\ s
or `MultiParentedTree`\ s.  Mixing tree implementations may result in
incorrect parent pointers and in `TypeError` exceptions:

    >>> # Inserting a Tree in a ParentedTree gives an exception:
    >>> ParentedTree('NP', [
    ...     Tree('DET', ['the']), Tree('NOUN', ['dog'])])
    Traceback (most recent call last):
      . . .
    TypeError: Can not insert a non-ParentedTree into a ParentedTree

    >>> # inserting a ParentedTree in a Tree gives incorrect parent pointers:
    >>> broken_tree = Tree('NP', [
    ...     ParentedTree('DET', ['the']), ParentedTree('NOUN', ['dog'])])
    >>> print(broken_tree[0].parent())
    None

Parented Tree Methods
------------------------
In addition to all the methods defined by the `Tree` class, the
`ParentedTree` class adds six new methods whose values are
automatically updated whenver a parented tree is modified: `parent()`,
`parent_index()`, `left_sibling()`, `right_sibling()`, `root()`, and
`treeposition()`.

The `parent()` method contains a `ParentedTree`\ 's parent, if it has
one; and ``None`` otherwise.  `ParentedTree`\ s that do not have
parents are known as "root trees."

    >>> for subtree in ptree.subtrees():
    ...     print(subtree)
    ...     print('  Parent = %s' % subtree.parent())
    (VP (VERB saw) (NP (DET the) (NOUN dog)))
      Parent = None
    (VERB saw)
      Parent = (VP (VERB saw) (NP (DET the) (NOUN dog)))
    (NP (DET the) (NOUN dog))
      Parent = (VP (VERB saw) (NP (DET the) (NOUN dog)))
    (DET the)
      Parent = (NP (DET the) (NOUN dog))
    (NOUN dog)
      Parent = (NP (DET the) (NOUN dog))

The `parent_index()` method stores the index of a tree in its parent's
child list.  If a tree does not have a parent, then its `parent_index`
is ``None``.

    >>> for subtree in ptree.subtrees():
    ...     print(subtree)
    ...     print('  Parent Index = %s' % subtree.parent_index())
    ...     assert (subtree.parent() is None or
    ...             subtree.parent()[subtree.parent_index()] is subtree)
    (VP (VERB saw) (NP (DET the) (NOUN dog)))
      Parent Index = None
    (VERB saw)
      Parent Index = 0
    (NP (DET the) (NOUN dog))
      Parent Index = 1
    (DET the)
      Parent Index = 0
    (NOUN dog)
      Parent Index = 1

Note that ``ptree.parent().index(ptree)`` is *not* equivalent to
``ptree.parent_index()``.  In particular, ``ptree.parent().index(ptree)``
will return the index of the first child of ``ptree.parent()`` that is
equal to ``ptree`` (using ``==``); and that child may not be
``ptree``:

    >>> on_and_on = ParentedTree('CONJP', [
    ...     ParentedTree('PREP', ['on']),
    ...     ParentedTree('COJN', ['and']),
    ...     ParentedTree('PREP', ['on'])])
    >>> second_on = on_and_on[2]
    >>> print(second_on.parent_index())
    2
    >>> print(second_on.parent().index(second_on))
    0

The methods `left_sibling()` and `right_sibling()` can be used to get a
parented tree's siblings.  If a tree does not have a left or right
sibling, then the corresponding method's value is ``None``:

    >>> for subtree in ptree.subtrees():
    ...     print(subtree)
    ...     print('  Left Sibling  = %s' % subtree.left_sibling())
    ...     print('  Right Sibling = %s' % subtree.right_sibling())
    (VP (VERB saw) (NP (DET the) (NOUN dog)))
      Left Sibling  = None
      Right Sibling = None
    (VERB saw)
      Left Sibling  = None
      Right Sibling = (NP (DET the) (NOUN dog))
    (NP (DET the) (NOUN dog))
      Left Sibling  = (VERB saw)
      Right Sibling = None
    (DET the)
      Left Sibling  = None
      Right Sibling = (NOUN dog)
    (NOUN dog)
      Left Sibling  = (DET the)
      Right Sibling = None

A parented tree's root tree can be accessed using the `root()`
method.  This method follows the tree's parent pointers until it
finds a tree without a parent.  If a tree does not have a parent, then
it is its own root:

    >>> for subtree in ptree.subtrees():
    ...     print(subtree)
    ...     print('  Root = %s' % subtree.root())
    (VP (VERB saw) (NP (DET the) (NOUN dog)))
      Root = (VP (VERB saw) (NP (DET the) (NOUN dog)))
    (VERB saw)
      Root = (VP (VERB saw) (NP (DET the) (NOUN dog)))
    (NP (DET the) (NOUN dog))
      Root = (VP (VERB saw) (NP (DET the) (NOUN dog)))
    (DET the)
      Root = (VP (VERB saw) (NP (DET the) (NOUN dog)))
    (NOUN dog)
      Root = (VP (VERB saw) (NP (DET the) (NOUN dog)))

The `treeposition()` method can be used to find a tree's treeposition
relative to its root:

    >>> for subtree in ptree.subtrees():
    ...     print(subtree)
    ...     print('  Tree Position = %s' % (subtree.treeposition(),))
    ...     assert subtree.root()[subtree.treeposition()] is subtree
    (VP (VERB saw) (NP (DET the) (NOUN dog)))
      Tree Position = ()
    (VERB saw)
      Tree Position = (0,)
    (NP (DET the) (NOUN dog))
      Tree Position = (1,)
    (DET the)
      Tree Position = (1, 0)
    (NOUN dog)
      Tree Position = (1, 1)

Whenever a parented tree is modified, all of the methods described
above (`parent()`, `parent_index()`, `left_sibling()`, `right_sibling()`,
`root()`, and `treeposition()`) are automatically updated.  For example,
if we replace ``ptree``\ 's subtree for the word "dog" with a new
subtree for "cat," the method values for both the "dog" subtree and the
"cat" subtree get automatically updated:

    >>> # Replace the dog with a cat
    >>> dog = ptree[1,1]
    >>> cat = ParentedTree('NOUN', ['cat'])
    >>> ptree[1,1] = cat

    >>> # the noun phrase is no longer the dog's parent:
    >>> print(dog.parent(), dog.parent_index(), dog.left_sibling())
    None None None
    >>> # dog is now its own root.
    >>> print(dog.root())
    (NOUN dog)
    >>> print(dog.treeposition())
    ()

    >>> # the cat's parent is now the noun phrase:
    >>> print(cat.parent())
    (NP (DET the) (NOUN cat))
    >>> print(cat.parent_index())
    1
    >>> print(cat.left_sibling())
    (DET the)
    >>> print(cat.root())
    (VP (VERB saw) (NP (DET the) (NOUN cat)))
    >>> print(cat.treeposition())
    (1, 1)

ParentedTree Regression Tests
-----------------------------
Keep track of all trees that we create (including subtrees) using this
variable:

    >>> all_ptrees = []

Define a helper funciton to create new parented trees:

    >>> def make_ptree(s):
    ...     ptree = ParentedTree.convert(Tree.fromstring(s))
    ...     all_ptrees.extend(t for t in ptree.subtrees()
    ...                       if isinstance(t, Tree))
    ...     return ptree

Define a test function that examines every subtree in all_ptrees; and
checks that all six of its methods are defined correctly.  If any
ptrees are passed as arguments, then they are printed.

    >>> def pcheck(*print_ptrees):
    ...     for ptree in all_ptrees:
    ...         # Check ptree's methods.
    ...         if ptree.parent() is not None:
    ...             i = ptree.parent_index()
    ...             assert ptree.parent()[i] is ptree
    ...             if i > 0:
    ...                 assert ptree.left_sibling() is ptree.parent()[i-1]
    ...             if i < (len(ptree.parent())-1):
    ...                 assert ptree.right_sibling() is ptree.parent()[i+1]
    ...             assert len(ptree.treeposition()) > 0
    ...             assert (ptree.treeposition() ==
    ...                     ptree.parent().treeposition() + (ptree.parent_index(),))
    ...             assert ptree.root() is not ptree
    ...             assert ptree.root() is not None
    ...             assert ptree.root() is ptree.parent().root()
    ...             assert ptree.root()[ptree.treeposition()] is ptree
    ...         else:
    ...             assert ptree.parent_index() is None
    ...             assert ptree.left_sibling() is None
    ...             assert ptree.right_sibling() is None
    ...             assert ptree.root() is ptree
    ...             assert ptree.treeposition() == ()
    ...         # Check ptree's children's methods:
    ...         for i, child in enumerate(ptree):
    ...             if isinstance(child, Tree):
    ...                 # pcheck parent() & parent_index() methods
    ...                 assert child.parent() is ptree
    ...                 assert child.parent_index() == i
    ...                 # pcheck sibling methods
    ...                 if i == 0:
    ...                     assert child.left_sibling() is None
    ...                 else:
    ...                     assert child.left_sibling() is ptree[i-1]
    ...                 if i == len(ptree)-1:
    ...                     assert child.right_sibling() is None
    ...                 else:
    ...                     assert child.right_sibling() is ptree[i+1]
    ...     if print_ptrees:
    ...         print('ok!', end=' ')
    ...         for ptree in print_ptrees: print(ptree)
    ...     else:
    ...         print('ok!')

Run our test function on a variety of newly-created trees:

    >>> pcheck(make_ptree('(A)'))
    ok! (A )
    >>> pcheck(make_ptree('(A (B (C (D) (E f)) g) h)'))
    ok! (A (B (C (D ) (E f)) g) h)
    >>> pcheck(make_ptree('(A (B) (C c) (D d d) (E e e e))'))
    ok! (A (B ) (C c) (D d d) (E e e e))
    >>> pcheck(make_ptree('(A (B) (C (c)) (D (d) (d)) (E (e) (e) (e)))'))
    ok! (A (B ) (C (c )) (D (d ) (d )) (E (e ) (e ) (e )))

Run our test function after performing various tree-modification
operations:

**__delitem__()**

    >>> ptree = make_ptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> e = ptree[0,0,1]
    >>> del ptree[0,0,1]; pcheck(ptree); pcheck(e)
    ok! (A (B (C (D ) (Q p)) g) h)
    ok! (E f)
    >>> del ptree[0,0,0]; pcheck(ptree)
    ok! (A (B (C (Q p)) g) h)
    >>> del ptree[0,1]; pcheck(ptree)
    ok! (A (B (C (Q p))) h)
    >>> del ptree[-1]; pcheck(ptree)
    ok! (A (B (C (Q p))))
    >>> del ptree[-100]
    Traceback (most recent call last):
      . . .
    IndexError: index out of range
    >>> del ptree[()]
    Traceback (most recent call last):
      . . .
    IndexError: The tree position () may not be deleted.

    >>> # With slices:
    >>> ptree = make_ptree('(A (B c) (D e) f g (H i) j (K l))')
    >>> b = ptree[0]
    >>> del ptree[0:0]; pcheck(ptree)
    ok! (A (B c) (D e) f g (H i) j (K l))
    >>> del ptree[:1]; pcheck(ptree); pcheck(b)
    ok! (A (D e) f g (H i) j (K l))
    ok! (B c)
    >>> del ptree[-2:]; pcheck(ptree)
    ok! (A (D e) f g (H i))
    >>> del ptree[1:3]; pcheck(ptree)
    ok! (A (D e) (H i))
    >>> ptree = make_ptree('(A (B c) (D e) f g (H i) j (K l))')
    >>> del ptree[5:1000]; pcheck(ptree)
    ok! (A (B c) (D e) f g (H i))
    >>> del ptree[-2:1000]; pcheck(ptree)
    ok! (A (B c) (D e) f)
    >>> del ptree[-100:1]; pcheck(ptree)
    ok! (A (D e) f)
    >>> ptree = make_ptree('(A (B c) (D e) f g (H i) j (K l))')
    >>> del ptree[1:-2:2]; pcheck(ptree)
    ok! (A (B c) f (H i) j (K l))

**__setitem__()**

    >>> ptree = make_ptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> d, e, q = ptree[0,0]
    >>> ptree[0,0,0] = 'x'; pcheck(ptree); pcheck(d)
    ok! (A (B (C x (E f) (Q p)) g) h)
    ok! (D )
    >>> ptree[0,0,1] = make_ptree('(X (Y z))'); pcheck(ptree); pcheck(e)
    ok! (A (B (C x (X (Y z)) (Q p)) g) h)
    ok! (E f)
    >>> ptree[1] = d; pcheck(ptree)
    ok! (A (B (C x (X (Y z)) (Q p)) g) (D ))
    >>> ptree[-1] = 'x'; pcheck(ptree)
    ok! (A (B (C x (X (Y z)) (Q p)) g) x)
    >>> ptree[-100] = 'y'
    Traceback (most recent call last):
      . . .
    IndexError: index out of range
    >>> ptree[()] = make_ptree('(X y)')
    Traceback (most recent call last):
      . . .
    IndexError: The tree position () may not be assigned to.

    >>> # With slices:
    >>> ptree = make_ptree('(A (B c) (D e) f g (H i) j (K l))')
    >>> b = ptree[0]
    >>> ptree[0:0] = ('x', make_ptree('(Y)')); pcheck(ptree)
    ok! (A x (Y ) (B c) (D e) f g (H i) j (K l))
    >>> ptree[2:6] = (); pcheck(ptree); pcheck(b)
    ok! (A x (Y ) (H i) j (K l))
    ok! (B c)
    >>> ptree[-2:] = ('z', 'p'); pcheck(ptree)
    ok! (A x (Y ) (H i) z p)
    >>> ptree[1:3] = [make_ptree('(X)') for x in range(10)]; pcheck(ptree)
    ok! (A x (X ) (X ) (X ) (X ) (X ) (X ) (X ) (X ) (X ) (X ) z p)
    >>> ptree[5:1000] = []; pcheck(ptree)
    ok! (A x (X ) (X ) (X ) (X ))
    >>> ptree[-2:1000] = ['n']; pcheck(ptree)
    ok! (A x (X ) (X ) n)
    >>> ptree[-100:1] = [make_ptree('(U v)')]; pcheck(ptree)
    ok! (A (U v) (X ) (X ) n)
    >>> ptree[-1:] = (make_ptree('(X)') for x in range(3)); pcheck(ptree)
    ok! (A (U v) (X ) (X ) (X ) (X ) (X ))
    >>> ptree[1:-2:2] = ['x', 'y']; pcheck(ptree)
    ok! (A (U v) x (X ) y (X ) (X ))

**append()**

    >>> ptree = make_ptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> ptree.append('x'); pcheck(ptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x)
    >>> ptree.append(make_ptree('(X (Y z))')); pcheck(ptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x (X (Y z)))

**extend()**

    >>> ptree = make_ptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> ptree.extend(['x', 'y', make_ptree('(X (Y z))')]); pcheck(ptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x y (X (Y z)))
    >>> ptree.extend([]); pcheck(ptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x y (X (Y z)))
    >>> ptree.extend(make_ptree('(X)') for x in range(3)); pcheck(ptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x y (X (Y z)) (X ) (X ) (X ))

**insert()**

    >>> ptree = make_ptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> ptree.insert(0, make_ptree('(X (Y z))')); pcheck(ptree)
    ok! (A (X (Y z)) (B (C (D ) (E f) (Q p)) g) h)
    >>> ptree.insert(-1, make_ptree('(X (Y z))')); pcheck(ptree)
    ok! (A (X (Y z)) (B (C (D ) (E f) (Q p)) g) (X (Y z)) h)
    >>> ptree.insert(-4, make_ptree('(X (Y z))')); pcheck(ptree)
    ok! (A (X (Y z)) (X (Y z)) (B (C (D ) (E f) (Q p)) g) (X (Y z)) h)
    >>> # Note: as with ``list``, inserting at a negative index that
    >>> # gives a position before the start of the list does *not*
    >>> # raise an IndexError exception; it just inserts at 0.
    >>> ptree.insert(-400, make_ptree('(X (Y z))')); pcheck(ptree)
    ok! (A
      (X (Y z))
      (X (Y z))
      (X (Y z))
      (B (C (D ) (E f) (Q p)) g)
      (X (Y z))
      h)

**pop()**

    >>> ptree = make_ptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> ptree[0,0].pop(1); pcheck(ptree)
    ParentedTree('E', ['f'])
    ok! (A (B (C (D ) (Q p)) g) h)
    >>> ptree[0].pop(-1); pcheck(ptree)
    'g'
    ok! (A (B (C (D ) (Q p))) h)
    >>> ptree.pop(); pcheck(ptree)
    'h'
    ok! (A (B (C (D ) (Q p))))
    >>> ptree.pop(-100)
    Traceback (most recent call last):
      . . .
    IndexError: index out of range

**remove()**

    >>> ptree = make_ptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> e = ptree[0,0,1]
    >>> ptree[0,0].remove(ptree[0,0,1]); pcheck(ptree); pcheck(e)
    ok! (A (B (C (D ) (Q p)) g) h)
    ok! (E f)
    >>> ptree[0,0].remove(make_ptree('(Q p)')); pcheck(ptree)
    ok! (A (B (C (D )) g) h)
    >>> ptree[0,0].remove(make_ptree('(Q p)'))
    Traceback (most recent call last):
      . . .
    ValueError: ParentedTree('Q', ['p']) is not in list
    >>> ptree.remove('h'); pcheck(ptree)
    ok! (A (B (C (D )) g))
    >>> ptree.remove('h');
    Traceback (most recent call last):
      . . .
    ValueError: 'h' is not in list
    >>> # remove() removes the first subtree that is equal (==) to the
    >>> # given tree, which may not be the identical tree we give it:
    >>> ptree = make_ptree('(A (X x) (Y y) (X x))')
    >>> x1, y, x2 = ptree
    >>> ptree.remove(ptree[-1]); pcheck(ptree)
    ok! (A (Y y) (X x))
    >>> print(x1.parent()); pcheck(x1)
    None
    ok! (X x)
    >>> print(x2.parent())
    (A (Y y) (X x))

Test that a tree can not be given multiple parents:

    >>> ptree = make_ptree('(A (X x) (Y y) (Z z))')
    >>> ptree[0] = ptree[1]
    Traceback (most recent call last):
      . . .
    ValueError: Can not insert a subtree that already has a parent.
    >>> pcheck()
    ok!

[more to be written]


ImmutableParentedTree Regression Tests
--------------------------------------

    >>> iptree = ImmutableParentedTree.convert(ptree)
    >>> type(iptree)
    <class 'pygmars.tree.ImmutableParentedTree'>
    >>> del iptree[0]
    Traceback (most recent call last):
      . . .
    ValueError: ImmutableParentedTree may not be modified
    >>> iptree.set_label('newnode')
    Traceback (most recent call last):
      . . .
    ValueError: ImmutableParentedTree may not be modified


MultiParentedTree Regression Tests
----------------------------------
Keep track of all trees that we create (including subtrees) using this
variable:

    >>> all_mptrees = []

Define a helper funciton to create new parented trees:

    >>> def make_mptree(s):
    ...     mptree = MultiParentedTree.convert(Tree.fromstring(s))
    ...     all_mptrees.extend(t for t in mptree.subtrees()
    ...                       if isinstance(t, Tree))
    ...     return mptree

Define a test function that examines every subtree in all_mptrees; and
checks that all six of its methods are defined correctly.  If any
mptrees are passed as arguments, then they are printed.

    >>> def mpcheck(*print_mptrees):
    ...     def has(seq, val): # uses identity comparison
    ...         for item in seq:
    ...             if item is val: return True
    ...         return False
    ...     for mptree in all_mptrees:
    ...         # Check mptree's methods.
    ...         if len(mptree.parents()) == 0:
    ...             assert len(mptree.left_siblings()) == 0
    ...             assert len(mptree.right_siblings()) == 0
    ...             assert len(mptree.roots()) == 1
    ...             assert mptree.roots()[0] is mptree
    ...             assert mptree.treepositions(mptree) == [()]
    ...             left_siblings = right_siblings = ()
    ...             roots = {id(mptree): 1}
    ...         else:
    ...             roots = dict((id(r), 0) for r in mptree.roots())
    ...             left_siblings = mptree.left_siblings()
    ...             right_siblings = mptree.right_siblings()
    ...         for parent in mptree.parents():
    ...             for i in mptree.parent_indices(parent):
    ...                 assert parent[i] is mptree
    ...                 # check left siblings
    ...                 if i > 0:
    ...                     for j in range(len(left_siblings)):
    ...                         if left_siblings[j] is parent[i-1]:
    ...                             del left_siblings[j]
    ...                             break
    ...                     else:
    ...                         assert 0, 'sibling not found!'
    ...                 # check ight siblings
    ...                 if i < (len(parent)-1):
    ...                     for j in range(len(right_siblings)):
    ...                         if right_siblings[j] is parent[i+1]:
    ...                             del right_siblings[j]
    ...                             break
    ...                     else:
    ...                         assert 0, 'sibling not found!'
    ...             # check roots
    ...             for root in parent.roots():
    ...                 assert id(root) in roots, 'missing root'
    ...                 roots[id(root)] += 1
    ...         # check that we don't have any unexplained values
    ...         assert len(left_siblings)==0, 'unexpected sibling'
    ...         assert len(right_siblings)==0, 'unexpected sibling'
    ...         for v in roots.values(): assert v>0, roots #'unexpected root'
    ...         # check treepositions
    ...         for root in mptree.roots():
    ...             for treepos in mptree.treepositions(root):
    ...                 assert root[treepos] is mptree
    ...         # Check mptree's children's methods:
    ...         for i, child in enumerate(mptree):
    ...             if isinstance(child, Tree):
    ...                 # mpcheck parent() & parent_index() methods
    ...                 assert has(child.parents(), mptree)
    ...                 assert i in child.parent_indices(mptree)
    ...                 # mpcheck sibling methods
    ...                 if i > 0:
    ...                     assert has(child.left_siblings(), mptree[i-1])
    ...                 if i < len(mptree)-1:
    ...                     assert has(child.right_siblings(), mptree[i+1])
    ...     if print_mptrees:
    ...         print('ok!', end=' ')
    ...         for mptree in print_mptrees: print(mptree)
    ...     else:
    ...         print('ok!')

Run our test function on a variety of newly-created trees:

    >>> mpcheck(make_mptree('(A)'))
    ok! (A )
    >>> mpcheck(make_mptree('(A (B (C (D) (E f)) g) h)'))
    ok! (A (B (C (D ) (E f)) g) h)
    >>> mpcheck(make_mptree('(A (B) (C c) (D d d) (E e e e))'))
    ok! (A (B ) (C c) (D d d) (E e e e))
    >>> mpcheck(make_mptree('(A (B) (C (c)) (D (d) (d)) (E (e) (e) (e)))'))
    ok! (A (B ) (C (c )) (D (d ) (d )) (E (e ) (e ) (e )))
    >>> subtree = make_mptree('(A (B (C (D) (E f)) g) h)')

Including some trees that contain multiple parents:

    >>> mpcheck(MultiParentedTree('Z', [subtree, subtree]))
    ok! (Z (A (B (C (D ) (E f)) g) h) (A (B (C (D ) (E f)) g) h))

Run our test function after performing various tree-modification
operations (n.b., these are the same tests that we ran for
`ParentedTree`, above; thus, none of these trees actually *uses*
multiple parents.)

**__delitem__()**

    >>> mptree = make_mptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> e = mptree[0,0,1]
    >>> del mptree[0,0,1]; mpcheck(mptree); mpcheck(e)
    ok! (A (B (C (D ) (Q p)) g) h)
    ok! (E f)
    >>> del mptree[0,0,0]; mpcheck(mptree)
    ok! (A (B (C (Q p)) g) h)
    >>> del mptree[0,1]; mpcheck(mptree)
    ok! (A (B (C (Q p))) h)
    >>> del mptree[-1]; mpcheck(mptree)
    ok! (A (B (C (Q p))))
    >>> del mptree[-100]
    Traceback (most recent call last):
      . . .
    IndexError: index out of range
    >>> del mptree[()]
    Traceback (most recent call last):
      . . .
    IndexError: The tree position () may not be deleted.

    >>> # With slices:
    >>> mptree = make_mptree('(A (B c) (D e) f g (H i) j (K l))')
    >>> b = mptree[0]
    >>> del mptree[0:0]; mpcheck(mptree)
    ok! (A (B c) (D e) f g (H i) j (K l))
    >>> del mptree[:1]; mpcheck(mptree); mpcheck(b)
    ok! (A (D e) f g (H i) j (K l))
    ok! (B c)
    >>> del mptree[-2:]; mpcheck(mptree)
    ok! (A (D e) f g (H i))
    >>> del mptree[1:3]; mpcheck(mptree)
    ok! (A (D e) (H i))
    >>> mptree = make_mptree('(A (B c) (D e) f g (H i) j (K l))')
    >>> del mptree[5:1000]; mpcheck(mptree)
    ok! (A (B c) (D e) f g (H i))
    >>> del mptree[-2:1000]; mpcheck(mptree)
    ok! (A (B c) (D e) f)
    >>> del mptree[-100:1]; mpcheck(mptree)
    ok! (A (D e) f)
    >>> mptree = make_mptree('(A (B c) (D e) f g (H i) j (K l))')
    >>> del mptree[1:-2:2]; mpcheck(mptree)
    ok! (A (B c) f (H i) j (K l))

**__setitem__()**

    >>> mptree = make_mptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> d, e, q = mptree[0,0]
    >>> mptree[0,0,0] = 'x'; mpcheck(mptree); mpcheck(d)
    ok! (A (B (C x (E f) (Q p)) g) h)
    ok! (D )
    >>> mptree[0,0,1] = make_mptree('(X (Y z))'); mpcheck(mptree); mpcheck(e)
    ok! (A (B (C x (X (Y z)) (Q p)) g) h)
    ok! (E f)
    >>> mptree[1] = d; mpcheck(mptree)
    ok! (A (B (C x (X (Y z)) (Q p)) g) (D ))
    >>> mptree[-1] = 'x'; mpcheck(mptree)
    ok! (A (B (C x (X (Y z)) (Q p)) g) x)
    >>> mptree[-100] = 'y'
    Traceback (most recent call last):
      . . .
    IndexError: index out of range
    >>> mptree[()] = make_mptree('(X y)')
    Traceback (most recent call last):
      . . .
    IndexError: The tree position () may not be assigned to.

    >>> # With slices:
    >>> mptree = make_mptree('(A (B c) (D e) f g (H i) j (K l))')
    >>> b = mptree[0]
    >>> mptree[0:0] = ('x', make_mptree('(Y)')); mpcheck(mptree)
    ok! (A x (Y ) (B c) (D e) f g (H i) j (K l))
    >>> mptree[2:6] = (); mpcheck(mptree); mpcheck(b)
    ok! (A x (Y ) (H i) j (K l))
    ok! (B c)
    >>> mptree[-2:] = ('z', 'p'); mpcheck(mptree)
    ok! (A x (Y ) (H i) z p)
    >>> mptree[1:3] = [make_mptree('(X)') for x in range(10)]; mpcheck(mptree)
    ok! (A x (X ) (X ) (X ) (X ) (X ) (X ) (X ) (X ) (X ) (X ) z p)
    >>> mptree[5:1000] = []; mpcheck(mptree)
    ok! (A x (X ) (X ) (X ) (X ))
    >>> mptree[-2:1000] = ['n']; mpcheck(mptree)
    ok! (A x (X ) (X ) n)
    >>> mptree[-100:1] = [make_mptree('(U v)')]; mpcheck(mptree)
    ok! (A (U v) (X ) (X ) n)
    >>> mptree[-1:] = (make_mptree('(X)') for x in range(3)); mpcheck(mptree)
    ok! (A (U v) (X ) (X ) (X ) (X ) (X ))
    >>> mptree[1:-2:2] = ['x', 'y']; mpcheck(mptree)
    ok! (A (U v) x (X ) y (X ) (X ))

**append()**

    >>> mptree = make_mptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> mptree.append('x'); mpcheck(mptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x)
    >>> mptree.append(make_mptree('(X (Y z))')); mpcheck(mptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x (X (Y z)))

**extend()**

    >>> mptree = make_mptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> mptree.extend(['x', 'y', make_mptree('(X (Y z))')]); mpcheck(mptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x y (X (Y z)))
    >>> mptree.extend([]); mpcheck(mptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x y (X (Y z)))
    >>> mptree.extend(make_mptree('(X)') for x in range(3)); mpcheck(mptree)
    ok! (A (B (C (D ) (E f) (Q p)) g) h x y (X (Y z)) (X ) (X ) (X ))

**insert()**

    >>> mptree = make_mptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> mptree.insert(0, make_mptree('(X (Y z))')); mpcheck(mptree)
    ok! (A (X (Y z)) (B (C (D ) (E f) (Q p)) g) h)
    >>> mptree.insert(-1, make_mptree('(X (Y z))')); mpcheck(mptree)
    ok! (A (X (Y z)) (B (C (D ) (E f) (Q p)) g) (X (Y z)) h)
    >>> mptree.insert(-4, make_mptree('(X (Y z))')); mpcheck(mptree)
    ok! (A (X (Y z)) (X (Y z)) (B (C (D ) (E f) (Q p)) g) (X (Y z)) h)
    >>> # Note: as with ``list``, inserting at a negative index that
    >>> # gives a position before the start of the list does *not*
    >>> # raise an IndexError exception; it just inserts at 0.
    >>> mptree.insert(-400, make_mptree('(X (Y z))')); mpcheck(mptree)
    ok! (A
      (X (Y z))
      (X (Y z))
      (X (Y z))
      (B (C (D ) (E f) (Q p)) g)
      (X (Y z))
      h)

**pop()**

    >>> mptree = make_mptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> mptree[0,0].pop(1); mpcheck(mptree)
    MultiParentedTree('E', ['f'])
    ok! (A (B (C (D ) (Q p)) g) h)
    >>> mptree[0].pop(-1); mpcheck(mptree)
    'g'
    ok! (A (B (C (D ) (Q p))) h)
    >>> mptree.pop(); mpcheck(mptree)
    'h'
    ok! (A (B (C (D ) (Q p))))
    >>> mptree.pop(-100)
    Traceback (most recent call last):
      . . .
    IndexError: index out of range

**remove()**

    >>> mptree = make_mptree('(A (B (C (D) (E f) (Q p)) g) h)')
    >>> e = mptree[0,0,1]
    >>> mptree[0,0].remove(mptree[0,0,1]); mpcheck(mptree); mpcheck(e)
    ok! (A (B (C (D ) (Q p)) g) h)
    ok! (E f)
    >>> mptree[0,0].remove(make_mptree('(Q p)')); mpcheck(mptree)
    ok! (A (B (C (D )) g) h)
    >>> mptree[0,0].remove(make_mptree('(Q p)'))
    Traceback (most recent call last):
      . . .
    ValueError: MultiParentedTree('Q', ['p']) is not in list
    >>> mptree.remove('h'); mpcheck(mptree)
    ok! (A (B (C (D )) g))
    >>> mptree.remove('h');
    Traceback (most recent call last):
      . . .
    ValueError: 'h' is not in list
    >>> # remove() removes the first subtree that is equal (==) to the
    >>> # given tree, which may not be the identical tree we give it:
    >>> mptree = make_mptree('(A (X x) (Y y) (X x))')
    >>> x1, y, x2 = mptree
    >>> mptree.remove(mptree[-1]); mpcheck(mptree)
    ok! (A (Y y) (X x))
    >>> print([str(p) for p in x1.parents()])
    []
    >>> print([str(p) for p in x2.parents()])
    ['(A (Y y) (X x))']


ImmutableMultiParentedTree Regression Tests
-------------------------------------------

    >>> imptree = ImmutableMultiParentedTree.convert(mptree)
    >>> type(imptree)
    <class 'pygmars.tree.ImmutableMultiParentedTree'>
    >>> del imptree[0]
    Traceback (most recent call last):
      . . .
    ValueError: ImmutableMultiParentedTree may not be modified
    >>> imptree.set_label('newnode')
    Traceback (most recent call last):
      . . .
    ValueError: ImmutableMultiParentedTree may not be modified


Squashed Bugs
=============

This used to discard the ``(B b)`` subtree (fixed in svn 6270):

    >>> print(Tree.fromstring('((A a) (B b))'))
    ( (A a) (B b))

"""