# Natural Language Toolkit: Models
#
# Copyright (C) 2001-2006 University of Pennsylvania
# Author: Ewan Klein <ewan@inf.ed.ac.uk>,
# URL: <http://nltk.sourceforge.net>
# For license information, see LICENSE.TXT
#
# $Id:$

"""
Overview
========

This module provides data structures for representing first-order
models. A model is a pair M{<D,V>}, where M{D} is a domain of discourse and
M{V} is a valuation function for the non-logical constants of a
first-order language. We assume that the language is based on the
lambda calculus, in the style of Montague grammar.


We assume that non-logical constants are either individual constants
or functors. In particular, rather than interpreting a one-place
predicate M{P} as a set M{S}, we interpret it as the corresponding
characteristic function M{f}, where M{f(a) = True} iff M{a} is in
M{S}. For example, instead of interpreting 'dog' as the set of
individuals M{{'d1', 'd2', 'd3'}}, we interpret it as the function
which maps 'd1', 'd2' and 'd3' to M{True} and every other entity to
M{False}.

Thus, as a first approximation, non-logical constants are interpreted as
follows (note that M{e} is the type of I{entities} and M{t} is the
type of truth values):

  - if M{alpha} is an individual constant, then M{V(alpha)}
    is an element of M{D}.
  - If M{gamma} is a functor of type (M{e} x ... x M{e}) -> M{t}, then
    M{V(gamma)} is a function M{f} from  M{D} x ... x M{D} to M{{True, False}}.

However, since we are basing our language on the lambda calculus (see
L{logic}), a binary relation such as 'like' will not in fact be
associated with the type (M{e} x M{e}) -> M{t}, but rather the type
(M{e} -> (M{e} -> M{t}); i.e., a function from entities to a function
from entities to truth values. In other words, functors are assigned
'Curried' functions as their values. We should also point out that
expressions of our languge are not explicitly typed.  We leave it to
the grammar writer to assign 'sensible' values to expressions rather
than enforcing any type-to-denotation consistency.

Characteristic Functions
========================

Within C{models}, Curried characteristic functions are implemented as
a subclass of dictionaries, using the C{CharFun()} constructor.

   >>> cf = CharFun({'d1' : {'d2': True}, 'd2' : {'d1': True}})
   >>> cf['d1']
   {'d2': True}

Values of a C{CharFun} are accessed by indexing in the usual way:

   >>> cf['d1']['d2']
   True
   >>> cf['not in domain']
   False

In practise, it may be more convenient to specify interpretations as
n-ary relations (i.e., sets of n-tuples) rather than as n-ary
functions. C{CharFun} provides a C{parse()} method which will convert
such relations into Curried characteristic functions:

   >>> s = set([('d1', 'd2'), ('d2', 'd1')])
   >>> cf = CharFun()
   >>> cf.parse(s)
   >>> cf
   {'d2': {'d1': True}, 'd1': {'d2': True}}

C{parse()} will raise an exception if the set is not in fact a
relation (i.e., contains tuples of different lengths:

  >>> wrong = set([('d1', 'd2'), ('d2', 'd1', 'd3')])
  >>> cf.parse(wrong)
  Traceback (most recent call last):
  ...
  ValueError: Set contains sequences of different lengths

However, unary relations can be parsed to characteristic functions.

  >>> unary = set(['d1', 'd2'])
  >>> cf.parse(unary)
  >>> cf
  {'d2': True, 'd1': True}

The function C{flatten} returns a set of the entities used as keys in
a C{CharFun} instance. The same information can be accessed via the
C{domain} attribute of C{CharFun}.

   >>> cf = CharFun({'d1' : {'d2': True}, 'd2' : {'d1': True}})
   >>> flatten(cf)
   set(['d2', 'd1'])
   >>> cf.domain
   set(['d2', 'd1'])

Valuations and Models
=====================

A I{Valuation} is a mapping from non-logical constants to appropriate semantic
values in the model. Valuations are created using the C{Valuation} constructor.

   >>> val = Valuation({'Fido' : 'd1', 'dog' : {'d1' : True, 'd2' : True}})
   >>> val
   {'Fido': 'd1', 'dog': {'d2': True, 'd1': True}}

As with C{CharFun}, C{Valuation} will also parse valuations using
relations rather than characteristic functions as interpretations.

   >>> setval = [('adam', 'b1'), ('betty', 'g1'),\
   ('girl', set(['g2', 'g1'])), ('boy', set(['b1', 'b2'])),\
   ('love', set([('b1', 'g1'), ('b2', 'g2'), ('g1', 'b1'), ('g2', 'b1')]))]
   >>> val = Valuation()
   >>> val.parse(setval)
   >>> print val
   {'adam': 'b1',
   'betty': 'g1',
   'boy': {'b1': True, 'b2': True},
   'girl': {'g2': True, 'g1': True},
   'love': {'b1': {'g1': True},
            'b2': {'g2': True},
            'g1': {'b1': True},
            'g2': {'b1': True}}}


Valuations have a C{domain} attribute, like C{CharFun}, and also a C{symbols}
attribute.

   >>> val.domain
   set(['g1', 'g2', 'b2', 'b1'])
   >>> val.symbols
   ['boy', 'girl', 'love', 'adam', 'betty']   

The C{Model} constructor takes two parameters, a C{set} and a C{Valuation}.

   >>> m = Model(val.domain, val)


"""

from nltk_lite.contrib import logic
from random import choice
from pprint import pformat

class Error(Exception): pass

class CharFun(dict):
    """
    A dictionary which represents a Curried characteristic function.
    """

    def __init__(self, charfun=None):
        dict.__init__(self)
        if charfun:
            self.update(charfun)
 
        
    def _isrel(self, s):
        """check whether a set represents a relation (of any arity)"""
        
        assert isinstance(s, set), "Argument is not a set"
        if not isinstance(max(s),tuple) or len(max(s))==len(min(s)):
            return True
        else:
            raise ValueError, "Set contains sequences of different lengths"

    def _item2dict(self, item):
        """
        @return: A characteristic function corresponding to the input.
        @rtype: C{CharFun}
        @param item: a literal or a tuple
        """
        
        chf = {}
        if isinstance(item, tuple):
            if len(item)==1:
                chf[item[0]] = True
            elif len(item) > 1:
                chf[item[0]] = self._item2dict(item[1:])
        else:
            chf[item] = True
        return chf


    def _merge(self, chf1, chf2):
        k = chf2.keys()[0]
        if k not in chf1:
            chf1.update(chf2)
        else:
            self._merge(chf1[k], chf2[k])
        return chf1

    def parse(self, s):
        """
        Convert an n-ary relation into its corresponding characteristic function.
        @rtype: C{CharFun}
        @type s: set
        """

        assert self._isrel(s)

        charfuns = []
        for item in s:
            charfuns.append(self._item2dict(item))
            
        chf = reduce(self._merge, charfuns)
        self.update(chf)

        
    def _getDomain(self):
        return flatten(self)

    domain = property(_getDomain, doc='Set-theoretic domain of a curried function')



def flatten(d):
    """
    @return: The set of keys of a C{CharFun} instance.
    @rtype: set
    @type d: dict
    """
    
    flat = []
    try:
        flat.extend(d.keys())
        for v in d.values():
            if isinstance(v, dict):
                flat.extend(flatten(v))
            else:
                flat.append(v)
    except AttributeError:
        flat.append(d)
    result = set(flat)
    result.discard(True)
    return result

class Valuation(dict):
    """
    A dictionary which represents a model-theoretic Valuation of non-logical constants.

    C{Valuation} will just raise a KeyError exception if indexed with an expression that
    is not in its list of symbols.
    """

    def __init__(self, valuation=None):
        dict.__init__(self)
        if valuation:
            self.update(valuation)

    def parse(self, seq):
        """
        Parse a list such as  C{[('j', 'b1'), ('girl', set(['g1', 'g2']))]} into a C{Valuation}.
        @rtype: C{Valuation}
        @param seq: A list of tuples of the form (I{constant}, I{relation}), where I{relation} is a set of tuples.
        """
        d = dict(seq)
        for k in d.keys():
            val = d[k]
            if isinstance(val, str):
                pass
            else:
                cf = CharFun()
                cf.parse(d[k])        
                d[k] = cf
        self.update(d)

    def __str__(self):
        return pformat(self)
        
    def _getDomain(self):
        dom = set()
        for v in self.values():
            flat = flatten(v)
            dom = dom.union(flat)
        return dom

    domain = property(_getDomain,
             doc='Set-theoretic domain of the value-space of a Valuation.')

    def _getSymbols(self):
        return self.keys()

    symbols = property(_getSymbols,
              doc='The non-logical constants which the Valuation recognizes.')


class Assignment(dict):
    """
    A dictionary which represents an assignment of values to variables.

    An assigment can only assign values from its domain.

    Although an assignment M{g} is finite, it is not I{partial}, in the following sense:
    if a variable M{x} is not one of M{g}'s keys, M{g} will choose an arbitrary member of
    the model's domain and use that as the value of M{x}. A downside of this approach
    is that if a unknown expression M{a} is passed to a model M{M}'s interpretation function M{i},
    M{i} will first check whether M{M}'s valuation assigns an interpretation to M{a} as a constant,
    and if this fails, M{i} will delegate the interpretation of M{a} to M{g}. Since we have no way at
    present of telling whether M{a} is in fact an individual variable, the behaviour of M{g} just
    described will by default treat it as one.
    An alternative would be to raise an exception in this case.
    
    """

    def __init__(self, domain, assignment=None):
        dict.__init__(self)
        self.domain = domain
        if assignment:
            self.update(assignment)
        self.variant = []

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            return self.choose()

    def purge(self, var=None):
        """
        Remove one or all keys (i.e. logic variables) from an assignment, and update C{self.variant}.

        @param var: a Variable acting as a key for the assignment.
        """
        if var:
            val = self[var]
            del self[var]
        else:
            self.clear()
        self._addvariant()
        return None

    def __str__(self):
        """
        Pretty printing for assignments. {'x', 'u'} appears as 'g[u/x]'
        """
        gstring = "g"
        for (val, var) in self.variant:
            gstring = gstring + "[" + str(val) + "/" + str(var) + "]"
        return gstring

    def _addvariant(self):
        """
        Create a more pretty-printable version of the assignment.
        """
        list = []
        for item in self.items():
            pair = (item[1], item[0])
            list.append(pair)
        self.variant = list
        return None
        
    def add(self, val, var):
        """
        Add a new variable-value pair to the assignment, and update C{self.variant}.

        We write the arguments in the order 'val, var' by analogy with the
        notation 'g[u/x]'.
        """
        assert val in self.domain
        self[var] = val
        self._addvariant()
        return self

    def choose(self):
        """
        Choose a member of C{self.domain} as a value for variables we don't know about.
        """
        seq = [x for x in self.domain]
        chosen = choice(seq)
        return chosen
    
    
class Model:
    """
    A first order model is a domain M{D} of discourse and a valuation M{V}.

    A domain M{D} is a set, and a valuation M{V} is a map that associates
    expressions with values in the model.
    The domain of M{V} should be a subset of M{D}.
    """
    
    def __init__(self, domain, valuation, prop=None):
        assert isinstance(domain, set)
        self.domain = domain
        self.valuation = valuation
        if prop is None:
            if not domain.issuperset(valuation.domain):
                raise Error,\
                "The valuation domain, %s, must be a subset of the model's domain, %s"\
                % (valuation.domain, domain)

        
    def __repr__(self):
        return "(%r, %r)" % (self.domain, self.valuation)

    def __str__(self):
        return "Domain = %s,\nValuation = \n%s" % (self.domain, self.valuation)

    def app(self, fun, arg):
        """
        Wrapper for handling KeyErrors raised by function application.
        
        This constrains instances of C{CharFun} to return C{False} in
        the right circumstances.

        @param fun: an instance of CharFun
        @param arg: an arbitrary object
        @return: If C{arg} is in C{fun}'s domain, then returns C{fun[arg]},\
                 else if C{arg} is in C{self.domain}, returns C{False}, else raises\
                 KeyError.
        """
        #assert isinstance(fun, dict)
        
        try:
            return fun[arg]
        except KeyError:
            if arg in self.domain:
                return False
        except TypeError:
            if fun == False:
                return False
            else:
                print "%s can't be applied as a function to %s" % (fun, arg)
                raise


    NOT =      {True: False, False: True}
    AND =      {True: {True: True, False: False},
                False: {True: False, False: False}}
    OR =       {True: {True: True, False: True},
                False: {True: True, False: False}}
    IMPLIES =  {True: {True: True, False: False},
                False: {True: True, False: True}}
    IFF =      {True: {True: True, False: False},
                False: {True: False, False: True}}


    def evaluate(self, expr, g, trace=False):
        """
        Recursive interpretation function for a formula of first-order logic.

        @return: Returns a truth value
        @param expr: An expression of L{logic}. 
        
        """

        OPS = {'and': Model.AND,
               'or': Model.OR,
               'implies': Model.IMPLIES,
               'iff': Model.IFF}

        try:
            first, second = self.decompose(expr)
            phi = second[0]
            try:
                psi = second[1]
            except IndexError:
                pass
            

            if first == 'not':
                if trace:
                    print "'%s' evaluates to %s under M, %s" %  (expr, self.evaluate(expr, g), g)
                    print "since '%s' evaluates to %s under M, %s." % (phi, self.evaluate(phi, g), g)
                return not self.evaluate(phi, g, trace)

            elif first in OPS:
                value = OPS[first][self.evaluate(phi, g, trace)][self.evaluate(psi, g, trace)]
                if trace:
                    print "'%s' evaluates to %s under M, %s" %  (expr, value, g)
                    print "   since '%s' evaluates to %s under M, %s %s" %  (phi, self.evaluate(phi, g), g, first)
                    print "   '%s' evaluates to %s under M, %s" %  (psi, self.evaluate(psi, g), g)
                return value
            

            elif first[0] == 'some':
                var = first[1]
                phi = second
#                 if trace:
#                     if self.evaluate(expr, g):
#                         print "'%s' evaluates to True under M, g" % expr
#                         print "since there is some u in M's domain such that '%s'\nevaluates to True under M, %s."\
#                         % (phi, g.add('u', var))
#                     else:
#                         print "'%s' evaluates to False under M, g" % expr
#                         print "since  is no u in M's domain such that '%s'\nevaluates to True under M, %s."\
#                               % (phi, g.add('u', var))
                return len(self.satisfiers(phi, var, g)) > 1

            elif first[0] == 'all':
                var = first[1]
                phi = second
#                 if trace:
#                    print "'%s' evaluates to %s under M, %s" % (expr, self.evaluate(expr, g), g)
#                     if self.evaluate(expr, g):
#                         print "'%s' evaluates to True under M, g" % expr
#                         print "since for every u in M's domain, '%s'\nevaluates to True under M, %s."\
#                         % (phi, g.add('u', var))
#                     else:
#                         print "'%s' evaluates to False under M, g" % expr
#                         print "since there is some u in M's domain such that '%s'\nevaluates to False under M, %s."\
#                               % (phi, g.add('u', var))
                return self.domain.issubset(self.satisfiers(phi, var, g))
            
            else:
                try:
                    funval = self.evaluate(first, g, trace)
                    argval =  self.evaluate(second, g, trace)
                    app = self.app(funval, argval)
                    if trace > 1:
                        print "'%s': %s applied to %s yields %s"\
                        %  (expr, funval, argval, app)
#                     elif trace:
#                         print "'%s': %s" % (expr, app)
                    return app
                except TypeError:
                    print "The interpretation of %s cannot be applied to the interpretation of %s"\
                          % (first, second)
                    raise

        except ValueError:
            # expr is an atomic expression
            return self.i(expr, g, trace)


    def i(self, expr, g, trace=False):
        """
        An interpretation function.

        Assuming that C{expr} is atomic, M{i} calls the valuation M{V} if
        C{expr} is a non-logical constant, and assignment M{g} if C{expr}
        is a free variable.

        
        @param expr: C{Expression} from L{logic}
        @param g: C{Assignment}
        @return: a semantic value
        """
        try:
            if trace > 1:
                print "   i, g('%s') = %s" % (expr, self.valuation[expr])
            # expr is a non-logical constant, i.e. in self.valuation.symbols
            return self.valuation[expr]
        except KeyError:
            if trace > 1:
                print "   ... assuming that '%s' is an individual variable" % expr
            pass
        try:
            if trace > 1:
                print "   i, g('%s') = %s" % (expr, g[expr])
            # expr wasn't a constant; maybe a variable that g knows about?
            return g[expr]
        # Currently, we never get to this point.
        except KeyError:
            print "Expression '%s' can't be evaluated by i." % expr


    def freevar(self, var, expr):
        """
        Is C{var} one of the free variables in C{expr}?

        @return: Boolean
        """
        parsed = logic.Parser().parse(expr)
        variable = logic.Variable(var)
        return variable in parsed.free()
        
    def satisfiers(self, expr, var, g, trace=False):
        """
        List the entities from the model's domain that satisfy an open formula.
        """
        list = []
        if self.freevar(var, expr):
            if trace:
                print "Open formula is '%s'" % expr
            for u in self.domain:
                g.add(u, var)
                if trace:
                    print "   ...trying assignment %s" % g
                    print "   value of '%s' under %s is %s" % (expr, g, self.evaluate(expr, g))
                # is expr == True under g[u/var]?
                # if not, throw away this variant
                if not self.evaluate(expr, g):
                    #g.purge(var)
                    pass
                    
                # so g[u/var] is a satisfying assignment
                else:
                    if trace:
                         self.evaluate(expr, g, trace)
                    list.append(u)
            result = set(list)
        # var isn't free in expr
        else:
            # so expr is true whatever the assigment
            if self.evaluate(expr, g):
                result = self.domain
            # some kind of error?
            else:
                result = None
        return result


    def decompose(self, expr):
        """
        Function to communicate with a first-order functional language.

        This function tries to make weak assumptions about the parse structure
        provided by the logic module.

        The (binder, body) pair is for decomposing quantifier formulae.
        The (op, args) pair is for decomposing formulae with a boolean operator.
        The (fun, args) pair should catch other relevant cases.

        @param expr: A string representation of a first-order formula.
        """

        parsed = logic.Parser(constants=self.valuation.symbols).parse(expr)
        try:
            first, second = parsed.binder, parsed.body
            #print 'first is %s, second is %s' % (first, second)
            return (first, second)
        except AttributeError:
            pass
        try: 
            first, second = parsed.op, parsed.args
            #print 'first is %s, second is %s' % (first, second)
            return (first, second)
        except AttributeError:
            pass
        try: 
            first, second = str(parsed.first), str(parsed.second)
            #print 'first is %s, second is %s' % (first, second)
            return (first, second)
        except (AttributeError, TypeError):
            return expr

#//////////////////////////////////////////////////////////////////////
# TESTING
#//////////////////////////////////////////////////////////////////////

import unittest

class TestModels(unittest.TestCase):

    def testLogicSelectors(self):
        "Tests for properties of formulae from 'logic' module."
        v = Valuation()
        m = Model(set([]), v)

        # Existential quantification
        pair = m.decompose('some x.(M N)')
        self.assertEqual(pair[0], ('some', 'x'))
        self.assertEqual(pair[1], '(M N)')

        # Universal quantification
        pair = m.decompose('all x.(M N)')
        self.assertEqual(pair[0], ('all', 'x'))
        self.assertEqual(pair[1], '(M N)')

        # Boolean operators
        pair = m.decompose('(and (M N) (P Q))')
        self.assertEqual(pair[0], 'and')
        self.assertEqual(pair[1], ['(M N)', '(P Q)'])

        pair = m.decompose('(not M N P Q)')
        self.assertEqual(pair[0], 'not')
        self.assertEqual(pair[1], ['M', 'N', 'P', 'Q'])

        # Just an application expression
        pair = m.decompose('(M N P)')
        self.assertEqual(pair[0], '(M N)')
        self.assertEqual(pair[1], 'P')
        

    def testValuations(self):
        "Tests for characteristic functions and valuations."
        cf = CharFun({'d1' : {'d1': True, 'd2': True}, 'd2' : {'d1': True}})
 

        self.assertEqual(cf['d1'], {'d1': True, 'd2': True})
        self.assertEqual(cf['d1']['d2'], True)
#        self.assertEqual(cf['not in domain'], False)
#        self.assertEqual(cf['d1']['not in domain'], False)

        self.assertEqual(flatten(cf), set(['d1', 'd2']))
        self.assertEqual(flatten(cf), cf.domain)

        s1 = set([('d1', 'd2'), ('d1', 'd1'), ('d2', 'd1')])
        cf1 = CharFun()
        cf1.parse(s1)
        self.assertEqual(cf, cf1)
        s2 = set([('d1', 'd2'), ('d1', 'd2'), ('d1', 'd1'), ('d2', 'd1')])
        cf2 = CharFun()
        cf2.parse(s2)
        self.assertEqual(cf1, cf2)

        unary = set(['d1', 'd2'])
        cf.parse(unary)
        self.assertEqual(cf, {'d2': True, 'd1': True})

        wrong = set([('d1', 'd2'), ('d2', 'd1', 'd3')])
        self.assertRaises(ValueError, cf.parse, wrong)

        val = Valuation({'Fido' : 'd1', 'dog' : {'d1' : True, 'd2' : True}})
        self.assertEqual(val['dog'], cf)
        self.assertEqual(val['dog'][val['Fido']], True)
        self.assertEqual(val.domain, set(['d1', 'd2']))
        self.assertEqual(val.symbols, ['Fido', 'dog'])
        
        setval = [('Fido', 'd1'), ('dog', set(['d1', 'd2']))]
        val1 = Valuation()
        val1.parse(setval)
        self.assertEqual(val, val1)

    def testFunArgApp(self):
        "Tests for function argument application in a Model"
        cf = CharFun({'d1' : {'d1': True, 'd2': True}, 'd2' : {'d1': True}})        
        
        
def testsuite():
    suite = unittest.makeSuite(TestModels)
    return unittest.TestSuite(suite)

def test(verbosity):
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(testsuite())
        
       
        
#//////////////////////////////////////////////////////////////////////
# Demo..
#//////////////////////////////////////////////////////////////////////        

    
def propdemo(trace=None):
    """Example of a propositional model."""
    
    global val1, dom1, m1, g1
    val1 = Valuation({'p': True, 'q': True, 'r': False})
    dom1 = set([])
    m1 = Model(dom1, val1, prop=True)
    g1 = Assignment(dom1)
    
    print "*****************************"
    print "Model m1:\n", m1
    print "*****************************"

    sentences = [
    '(p and q)',
    '(p and r)',
    '(not p)',
    '(not r)',
    '(not (not p))',
    '(not (p and r))',
    '(p or r)',
    '(r or p)',
    '(r or r)',
    '((not p) or r))',
    '(p or (not p))',
    '(p implies q)',
    '(p implies r)',
    '(r implies p)',
    '(p iff p)',
    '(r iff r)',
    '(p iff r)',
    ]

    for sent in sentences:
        if trace:
            print
            m1.evaluate(sent, g1, trace)
        else:
            print "The value of '%s' is: %s" % (sent, m1.evaluate(sent, g1))

def folmodel(trace=None):
    """Example of a first-order model."""

    global val2, v2, dom2, m2, g2
    val2 = Valuation()
    v2 = [('adam', 'b1'), ('betty', 'g1'), ('fido', 'd1'),\
         ('girl', set(['g1', 'g2'])), ('boy', set(['b1', 'b2'])),\
         ('love', set([('b1', 'g1'), ('b2', 'g2'), ('g1', 'b1'), ('g2', 'b1')]))]
    val2.parse(v2)
    dom2 = val2.domain
    m2 = Model(dom2, val2)
    g2 = Assignment(dom2)

    if trace:
        print "*****************************"
        print "Model m2\n", m2
        print "*****************************"
        
    symbols = ['adam', 'girl', 'love', 'walks', 'x', 'y', 'z']

    if trace:
        for s in symbols:
            print "The interpretation of '%s' in m2 is %s" % (s, m2.i(s, g2))
    
def foldemo(trace=None):

    folmodel()

    sentences = [
    '(love adam betty)',
    'some z. (boy z)',
    'all x. ((boy x) or (girl x))',
    'all x. ((boy x) implies some y. (girl y) and (love x y))',
    'some y. ((girl y) and all x. ((boy x) implies (love x y)))',
    'all x. some y . (love x y)',
    'all x. all y. ((love x y) implies (love y x))'
    ]

    print "*****************************"

    for sent in sentences:
        g.purge()
        if trace:
            print
            m2.evaluate(sent, g, trace)
        else:
            print "The value of '%s' is: %s" % (sent, m2.evaluate(sent, g))


def satdemo(trace=None):

    folmodel()
    
    clauses = [
               '(boy x)',
               '((boy x) or (girl x))',
               '((boy x) and (girl x))',
               '(love x adam)',
               '(love adam x)',
               'some y. (love y x)'
               ]

    for clause in clauses:
        g2.purge()
        print 
        print "***> The satisfiers of '%s' are: %s" % (clause, m2.satisfiers(clause, 'x', g2, trace))
        
        
def demo(trace=None):
    propdemo(trace=trace)
    foldemo(trace=trace)
    satdemo(trace=trace)


if __name__ == "__main__":
    satdemo(trace=1)
    #propdemo(1)
    #test(verbosity=2) 
        
        
        
