# thompyson

## Installation

Use `pip` to install the `thompyson` package.

To import the package, run
```python
import thompyson
```

## Current Functionality

### Rationals and Dyadics

The `thompyson` package provides utilities for infinite-precision calculations on dyadic rationals (soon to be upgraded to rationals).

#### Creation and Operation

To create a rational or a dyadic, simply run
```python
dyadic = thompyson.Dyadic(7, 32)
```
Or
```python
rational = thompyson.Rational(3, 55)
```

`Dyadic`s support the following operations: negation, absolute value, addition, multiplication, subtraction, equality checking, less than (and less than or equal to), greater than (and greater than or equal to), `__repr__`, and simplification.
Simplifying a `Dyadic` puts it in its canonical form.  There are two different ways to simplify a `Dyadic`.  If `dyadic` is a `Dyadic`, then the first is `dyadic.simplify()`: this simplifies `dyadic` in-place; the second is `dyadic.simplified()`: this returns the canonical form of `dyadic`, but leaves the variable `dyadic` unchanged.
`Dyadic`s support the following operations with `int`s (each still returns a `Dyadic` or `bool` -- the same as whichever it returned before): addition, multiplication, subtraction, equality checking, `<`, `>`, `<=`, `>=`.
`Dyadic`s support the following operations with `float`s, where each returns a `float`: addition, subtraction, multiplication.
`Dyadic`s support the following operations with `float`s, which each returns a `bool`: `==`, `<`, `>`, `<=`, `>=`.


`Dyadic`s are a sub-class of `Rational`.  Therefore, `Dyadic`s inherit all the methods of `Rational`s.
Currently, `Rational`s support the following operations (where an operation is listed for `Dyadic` above, `Dyadic` has its own implementation of the operation): conversion to `float`, conversion to `int`, negation, taking the absolute value, inversion, simplification, producing a `TeX` string (`.to_tex`), conversion to `str`.
Inversion is carried out in three ways: the unary operation `~`, which is not in-place, and does not modify the `Rational`; the in-place `.invert()`; and the non in-place `.inverted()`.
Simplification is the same as for `Dyadic`s: `.simplify()` is in-place; `.simplified()` is not.  Note that both of these operations will change the `Rational` to a `Dyadic` if that is possible.

These operations do not simplify the `Dyadic` or `Rational` after running (except, of course, the `.simplify` methods).

Unless explicitly specified, these operations are all implemented with the default Python methods, meaning that they can all be calculated by running the in-built functions (like `abs`, `int`, `float`, etc.) or by the in-built operations (like the unary `-`, `*`, `+`, etc).

#### Related Functions

There are two functions offered by the `thompyson` package to aid in `Dyadic` computations.  The first is `dyadic_is_power_of_two`, which takes in a `Dyadic` and checks whether it is a power of two or not: it returns `True` if it is, and `False` otherwise.  The second is `dyadic_gradient`, which takes in two pairs of `Dyadic`s, representing two co-ordinates in the cartesian plane, and then calculates the gradient of the line between those two points: this value will be a `Dyadic` if the result is a dyadic rational, and will be a `Rational` otherwise.  In either case, the result will be simplified.



### Tree Pairs

The `thompyson` package provides utilities for computations in the groups F and T.

#### Creation

Tree pairs are written in depth-first search notation.  The third argument is the 1-indexed permutation of the tree pair; that is, it says which leaf in the range tree corresponds to the first leaf in the domain tree.  Note that we can describe this by one-variable as we are working in F and T.  Elements of F have permutation of `1`, and if a tree pair has a permutation not equal to `1`, it is an element of T.


```python
tree_pair = thompyson.TreePair("10100", "11000", 1)
```

This stores a tree pair representing `{10100,11000,1 2 3}` (in nvTrees-notation) into the variable `tree_pair`.

We can run
```python
print(tree_pair)
```
to get an nvTrees-compatible string, describing the element (in particular, this would return the string `{10100,11000,1 2 3}`).


#### Right Actions

By default, `thompyson` uses right actions.  To change to left actions, run
```python
thompyson.use_right_actions(False)
```

#### Computations

- Multiplication is invoked by `*` (currently, we use left-actions).  Multiplication does not return a reduced tree pair.
- Exponentiation is invoked by `**`, and negative powers work as expected.  Exponentiation does not return a reduced tree pair.
- Conjugation is invoked by `^`.  Conjugation does not return a reduced tree pair.
- Commutation is invoked by `|`.  Commutation does not return a reduced tree pair.
- Inversion is invoked by `~` and does not modify the tree pair in question.  Inversion does not return a reduced tree pair. To invert the tree pair `tree_pair` in place, call `tree_pair.invert()`.  We can also run `tree_pair.inverted()`, which returns the inverse of `tree_pair` without modifying `tree_pair`.
- Equality checking is invoked by `==`.  Checking for equality does not reduce the tree pairs first; so, an unreduced tree pair, and a reduced tree pair representing the same element would not be classed as being equal.
- To return a reduced tree pair, without modifying said tree pair, we use that unary `-`.  To reduce a tree pair `tree_pair` in place, we run `tree_pair.reduce()`.  Similar to the unary `-`, `tree_pair.reduced()` returns a reduced representation of `tree_pair`, but does not modify the variable `tree_pair`.


#### Related Functions

We have already seen `use_right_actions`. But, `thompyson` also provides `tree_pair_to_hidden_breaks`, `tree_pair_to_breaks`, and `breaks_to_tree_pair`.

First, `tree_pair_to_hidden_breaks` takes in a `TreePair`, and then outputs a pair of two equal-length lists of `Dyadic`s. The two lists represent the hidden breaks of the given `TreePair`: the first list of those of the domain, in standard increasing order, and the second list is those of the range, where the value of the break in the `i`th position of the range breaks corresponds to the leaf mapped onto by the `i`th leaf/break in the domain.

Second, `tree_pair_to_breaks` takes in a `TreePair`, and then outputs a triple of two equal-length lists of `Dyadic`s and a single `Dyadic`.  The two lists represent the true breaks of the given `TreePair` (that is, pairing the elements of the two lists in order provides the co-ordinates of each of the positions at which the gradient changes -- where the function is non-differentiable). The final value is a `Dyadic` representing the value of the `TreePair` applied to the number 0.

Third, `breaks_to_tree_pair` takes in two lists of `Dyadic`s, corresponding to positions of the breaks in the domain and the range (the `i`th break in the domain break list must be mapped to the `i`th break in the range break list).  This list must contain all the true breaks of the corresponding tree pair, but it may contain any other hidden breaks that the user wishes to include.  The result is the unique (except no breaks maps to all the rotations in T, -- but is unique when the value of the tree pair applied to 0 is specified -- this will be added soon) tree pair described by this set of break points.

