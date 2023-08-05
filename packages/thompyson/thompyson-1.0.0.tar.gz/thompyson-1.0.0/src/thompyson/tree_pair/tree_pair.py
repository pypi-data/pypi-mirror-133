from ..rational.dyadic import Rational, Dyadic, dyadic_gradient, \
                                dyadic_is_power_of_two

# TODO: documentation
USE_RIGHT_ACTIONS = True



def use_right_actions(b: bool) -> bool:
    # TODO: documentation
    if not isinstance(b, bool):
        return False
    global USE_RIGHT_ACTIONS
    USE_RIGHT_ACTIONS = b
    return True


class TreePair():
    # TODO: documentation

    def __init__(self,
                 domain_tree: str,
                 range_tree: str,
                 permutation: int):
        # TODO: documentation
        # TODO: error checking
        self.domain_tree = int(domain_tree, 2)
        self.range_tree = int(range_tree, 2)
        self.permutation = permutation - 1

        # TODO: implement function conversion.
        self.func = None


    @classmethod
    def _internal_init(cls, domain_tree: int, range_tree: int,
                       permutation: int):
        # TODO: documentation
        dom = bin(domain_tree)[2:]
        ran = bin(range_tree)[2:]
        perm = permutation + 1

        return cls(dom, ran, perm)


    def __str__(self):
        # TODO: documentation
        hsb = _bitstring_get_highest_set_bit(self.domain_tree)
        n = _tree_pair_get_number_of_leaves(hsb)
        p = self.permutation

        s = "{" + '{:0b}'.format(self.domain_tree) + ","
        s += '{:0b}'.format(self.range_tree) + ","
        perm = [str(i+1) if i < n else str(i - n + 1) for i in range(p, p+n)]
        s += " ".join(perm) + "}"
        return s


    def __repr__(self):
        # TODO: documentation
        dom = bin(self.domain_tree)[2:]
        ran = bin(self.range_tree)[2:]
        perm = self.permutation + 1

        return f"TreePair(\"{dom}\", \"{ran}\", {perm})"


    def __eq__(self, other):
        # TODO: documentation
        # TODO: note that it compares tree pairs without reducing them.
        if not isinstance(other, TreePair):
            return False
        if not self.permutation == other.permutation:
            return False
        if not self.domain_tree == other.domain_tree:
            return False
        if not self.range_tree == other.range_tree:
            return False
        return True


    def reduce(self):
        # TODO: documentation
        self = _reduce_tree_pair(self)
        return self


    def reduced(self):
        # TODO: documentation
        return _reduce_tree_pair(self)


    def __neg__(self):
        # TODO: documentation
        return self.reduced()


    def invert(self):
        # TODO: documentation
        self = _invert_tree_pair(self)
        return self


    def inverted(self):
        # TODO: documentation
        return _invert_tree_pair(self)


    def __invert__(self):
        # TODO: documentation
        return _invert_tree_pair(self)


    def __mul__(self, other):
        # TODO: documentation
        if not isinstance(other, TreePair):
            return NotImplemented
        return _mult_tree_pairs(self, other)


    def __pow__(self, other):
        # TODO: documentation
        if not isinstance(other, int):
            return NotImplemented

        val = TreePair("0", "0", 1)
        p = other

        if p < 0:
            p = abs(p)
            t = self.inverted()
        else:
            t = self

        for i in range(p):
            val = val * t

        return val


    def __xor__(self, other):
        # TODO: documentation
        # Conjugation
        if not isinstance(other, TreePair):
            return NotImplemented
        if USE_RIGHT_ACTIONS:
            return other.inverted() * self * other
        return other * self * other.inverted()


    def __or__(self, other):
        # TODO: documentation
        # Commutation
        if not isinstance(other, TreePair):
            return NotImplemented
        if USE_RIGHT_ACTIONS:
            return self.inverted() * other.inverted() * self * other
        return self * other * self.inverted() * other.inverted()



def tree_pair_to_hidden_breaks(tree_pair: TreePair) -> ([Dyadic], [Dyadic]):

    hsb = _bitstring_get_highest_set_bit(tree_pair.domain_tree)

    domain_hidden_breaks = _tree_to_hidden_breaks(tree_pair.domain_tree, hsb)
    range_hidden_breaks = _tree_to_hidden_breaks(tree_pair.range_tree, hsb)

    if tree_pair.permutation == 0:
        return domain_hidden_breaks, range_hidden_breaks

    # Rotate the range hidden breaks by the permutation.
    p = tree_pair.permutation
    n = len(range_hidden_breaks)
    range_hidden_breaks = \
        [range_hidden_breaks[(n - p - 1 + i) % n] for i in range(n)]

    if range_hidden_breaks[0] != Dyadic(0, 1):
        del range_hidden_breaks[range_hidden_breaks.index(Dyadic(0, 1))]
        range_hidden_breaks.append(range_hidden_breaks[0])
    return domain_hidden_breaks, range_hidden_breaks



def tree_pair_to_breaks(tree_pair: TreePair) -> ([Dyadic], [Dyadic], Dyadic):
    """
    Idea
    ----
    for elements of T:
    loop_start: for each element in the list of dyadics:
        - calculate the gradient with the element to the left
            - if the previous y co-ordinate is lower, normal procedure
                otherwise, we need to take take the y co-ordinate away from
                0.
            - if the previous x co-ordinate is greater, we need to change it:
                from the current subtract 1 - the previous
        - calculate the gradient with the element to the right
            - if the next y co-ordinate is greater, normal procedure
                othewise, we need to add the y co-ordinate to 1.
            - if the next x co-ordinate is lower, we need to change it:
                simply add the two x co-ordinates together
        - if they are the same, delete the point and go to loop_start
    """

    domain_hidden_breaks, range_hidden_breaks = \
                                tree_pair_to_hidden_breaks(tree_pair)

    y_start = range_hidden_breaks[0]

    if tree_pair.permutation != 0:
        del domain_hidden_breaks[-1]
        del range_hidden_breaks[-1]

    while True: # label: start
        for i in range(len(domain_hidden_breaks)):
            # In F, we skip checking the end-points
            if tree_pair.permutation == 0 and \
                    (domain_hidden_breaks[i] == Dyadic(0, 1) or
                     domain_hidden_breaks[i] == Dyadic(1, 1)):
                continue

            current_point = (domain_hidden_breaks[i], range_hidden_breaks[i])

            p = (i - 1) % len(domain_hidden_breaks)
            previous_point = (domain_hidden_breaks[p], range_hidden_breaks[p])

            n = (i + 1) % len(domain_hidden_breaks)
            next_point = (domain_hidden_breaks[n], range_hidden_breaks[n])

            if current_point == previous_point or current_point == next_point:
                del domain_hidden_breaks[i]
                del range_hidden_breaks[i]
                break # return to start

            if previous_point[0] > current_point[0]:
                previous_point = (previous_point[0] - 1, previous_point[1])
            if previous_point[1] > current_point[1]:
                previous_point = (previous_point[0], previous_point[1] - 1)

            if next_point[0] < current_point[0]:
                previous_point = (1 + next_point[0], previous_point[1])
            if next_point[1] < current_point[1]:
                next_point = (next_point[0], 1 + next_point[1])

            left_gradient = dyadic_gradient(current_point, previous_point)
            right_gradient = dyadic_gradient(current_point, next_point)

            if left_gradient == right_gradient:
                del domain_hidden_breaks[i]
                del range_hidden_breaks[i]
                break # return to start
        else:
            break # quit start

    return domain_hidden_breaks, range_hidden_breaks, y_start



def breaks_to_tree_pair(domain_breaks: [Dyadic], range_breaks: [Dyadic]) -> \
                                                                    TreePair:
    if len(domain_breaks) != len(range_breaks):
        raise ValueError("Domain and range breaks must be the same length.")
    if len(domain_breaks) == 0:
        # TODO: add starting-location to clarify whether this is really the
        # identity.
        return TreePair("0", "0", 1)

    new_tree_pair, rotation_amount = \
        _breaks_to_tree_pair_and_rotation(domain_breaks, range_breaks)

    # Pre-multiply by the rotation: TODO!
    r = _tree_pair_get_rotation_tree(rotation_amount._denominator)
    perm = rotation_amount._denominator - rotation_amount._numerator
    rotation_tree = TreePair._internal_init(r, r, perm)
    global USE_RIGHT_ACTIONS
    current_actions = USE_RIGHT_ACTIONS
    USE_RIGHT_ACTIONS = True
    tree_pair = rotation_tree * new_tree_pair
    USE_RIGHT_ACTIONS = current_actions

    return tree_pair.reduce()



# TODO: implement
"""
def tree_pair_pre_multiplfy_f_by_rotation(f: TreePair,
                                          rot: Dyadic) -> TreePair:
    # Check that this is genuinely an element of F
    if not (isinstance(f, TreePair) and isinstance(rot, Dyadic)):
        raise ValueError
    if not f.permutation == 0:
        raise ValueError

    domain_tree = f.domain_tree
    range_tree = f.range_tree
    rot = rot.simplified()

    perm = rot._denominator - rot._numerator

    if domain_tree == range_tree:
        new_tree = _tree_pair_get_rotation_tree(rot._denominator)
        return TreePair._internal_init(new_tree, new_tree, perm)

    hsb = _bitstring_get_highest_set_bit(domain_tree)
    required_depth = rot._denominator

    # TODO...
"""



# ============================================================================
# |                        Internal Helper Functions                         |
# ============================================================================



def _is_next_break_expected(current: Dyadic, previous: Dyadic,
                            depth: int) -> bool:
    dyadic = current - previous
    dyadic.simplify()
    if dyadic._numerator == 1 and dyadic._denominator >= depth:
        return True
    return False



def _rotate_breaks(domain_breaks: [Dyadic],
                   range_breaks: [Dyadic]) -> ([Dyadic], [Dyadic], Dyadic):
    n = len(range_breaks)
    for i in range(n):
        if range_breaks[i] == 0:
            if i == 0:
                permutation = 0
            else:
                permutation = i - 1
            break

    rotation_amount = Dyadic(0, 1)

    if permutation != 0:
        sorted_breaks = []
        edited_domain = []
        for i in range(n):
            if i < n - permutation - 1:
                sorted_breaks.append(range_breaks[i + permutation + 1])
                dyadic = domain_breaks[i + permutation] -\
                    domain_breaks[permutation]
                dyadic.simplify()
                edited_domain.append(dyadic)
            else:
                sorted_breaks.append(range_breaks[i - n + permutation + 1])
                dyadic = domain_breaks[permutation] - \
                    domain_breaks[i - n + permutation + 1]
                dyadic.simplify()
                dyadic = 1 - dyadic
                dyadic.simplify()
                edited_domain.append(dyadic)
        rotation_amount = 1 - domain_breaks[permutation]
        rotation_amount.simplify()
        range_breaks = sorted_breaks
        domain_breaks = edited_domain

    return domain_breaks, range_breaks, rotation_amount



def _add_break_to_tree(current_break: Dyadic, previous_break: Dyadic,
                       tree: int, current_depth: int,
                       depth_counter: Dyadic) -> (int, int, Dyadic):
    cur_denom = current_break._denominator
    pre_denom = previous_break._denominator

    if cur_denom > pre_denom:
        exponent_difference = 0
        while cur_denom > pre_denom:
            pre_denom <<= 1
            exponent_difference += 1

        tree <<= exponent_difference
        tree += (1 << exponent_difference) - 1
        current_depth <<= exponent_difference

        depth_counter += Dyadic(1, current_depth)
        depth_counter.simplify()
    else:
        depth_counter += Dyadic(1, current_depth)
        depth_counter.simplify()
        current_depth = depth_counter._denominator

    return (tree << 1), current_depth, depth_counter



def _find_next_possible_break(current_break: Dyadic, previous_break: Dyadic,
                              depth: int, gradient: Dyadic,
                              other_tree_previous_break: Dyadic) -> \
                                                            (Dyadic, Dyadic):
    next_possible_break = previous_break + Dyadic(1, depth)
    next_possible_break.simplify()
    while current_break < next_possible_break:
        depth <<= 1
        next_possible_break = previous_break + Dyadic(1, depth)
        next_possible_break.simplify()
    other_tree_current_break = other_tree_previous_break + \
                                                Dyadic(1, depth) * gradient
    other_tree_current_break.simplify()

    return next_possible_break, other_tree_current_break



def _correct_current_break(dom_current: Dyadic, dom_previous: Dyadic,
                           dom_depth: int, ran_current: Dyadic,
                           ran_previous: Dyadic, ran_depth: int) -> \
                                                (Dyadic, Dyadic, bool):
    is_dom_break_expected = _is_next_break_expected(dom_current, dom_previous,
                                                    dom_depth)
    is_ran_break_expected = _is_next_break_expected(ran_current, ran_previous,
                                                    ran_depth)
    to_decrement = False

    if not (is_dom_break_expected and is_ran_break_expected):
        to_decrement = True
        gradient = dyadic_gradient((dom_current, ran_current),
                                   (dom_previous, ran_previous))
        gradient.simplify()
        if not dyadic_is_power_of_two(gradient):
            raise ValueError("The domain breaks do not have power of two "
                             "gradient.")

        if not is_dom_break_expected:
            dom_current, ran_current = \
                _find_next_possible_break(dom_current, dom_previous,
                                          dom_depth, gradient, ran_previous)
            is_ran_break_expected = _is_next_break_expected(ran_current,
                                                            ran_previous,
                                                            ran_depth)

        if not is_ran_break_expected:
            # The inverted gradient is gaurenteed to be a Dyadic as the
            # gradient is a power of two.
            inverted_gradient = ~gradient
            inverted_gradient.simplify()
            ran_current, dom_current = \
                _find_next_possible_break(ran_current, ran_previous,
                                          ran_depth, inverted_gradient,
                                          dom_previous)

    return dom_current, ran_current, to_decrement



def _breaks_to_tree_pair_and_rotation(domain_breaks: [Dyadic],
                                      range_breaks: [Dyadic]) -> \
                                                        (TreePair, Dyadic):
    domain_breaks = [dyadic.simplify() for dyadic in domain_breaks]
    range_breaks = [dyadic.simplify() for dyadic in range_breaks]

    if domain_breaks[0] != 0:
        if domain_breaks[-1] == 1 and range_breaks[-1] ==  1:
            range_breaks = [Dyadic(0, 1)] + range_breaks
        elif domain_breaks[-1] == 1:
            range_breaks = [range_breaks[-1]] + range_breaks
        else:
            gradient = dyadic_gradient(
                (1 + domain_breaks[0], range_breaks[0]),
                (domain_breaks[-1], range_breaks[-1])
            )
            gradient.simplify()
            if dyadic_is_power_of_two(gradient):
                new_range_start = (1 - domain_breaks[-1]) * gradient
                new_range_start.simplify()
                new_range_start += range_breaks[-1]
                new_range_start.simplify()
                range_breaks = [new_range_start] + range_breaks
                range_breaks.append(new_range_start)
                domain_breaks.append(Dyadic(1, 1))
            else:
                range_breaks.append(Dyadic(1, 1))
                range_breaks = [Dyadic(0, 1)] + range_breaks
                domain_breaks.append(Dyadic(1, 1))
        domain_breaks = [Dyadic(0, 1)] + domain_breaks

    if domain_breaks[-1] != 1:
        if domain_breaks[0] == 0 and range_breaks[0] == 0:
            range_breaks.append(Dyadic(1, 1))
        else:
            range_breaks.append(range_breaks[0])
        domain_breaks.append(Dyadic(1, 1))

    if Dyadic(1, 1) not in range_breaks:
        prev = Dyadic(0, 1)
        for i, rbreak in enumerate(range_breaks):
            if rbreak < prev:
                gradient = dyadic_gradient(
                    (domain_breaks[i], 1 + rbreak),
                    (domain_breaks[i - 1], prev)
                )
                gradient.simplify()
                range_breaks = range_breaks[:i] + [Dyadic(1, 1)] + \
                    range_breaks[i:]
                new_domain_break = (1 - prev) * (~gradient).simplified()
                new_domain_break.simplify()
                new_domain_break += domain_breaks[i - 1]
                new_domain_break.simplify()
                domain_breaks = domain_breaks[:i] + [new_domain_break] + \
                    domain_breaks[i:]
                break
            prev = rbreak
        else:
            range_breaks.append(Dyadic(1, 1))
            domain_breaks.append(Dyadic(1, 1))

    if range_breaks[0] != 0 and \
            range_breaks[range_breaks.index(Dyadic(1, 1)) + 1] != 0:
        pos = range_breaks.index(Dyadic(1, 1))
        range_breaks = range_breaks[:pos + 1] + [Dyadic(0, 1)] + \
            range_breaks[pos + 1:-1]

    domain_breaks, range_breaks, rotation_amount = \
                                _rotate_breaks(domain_breaks, range_breaks)

    new_domain_tree = 0
    new_range_tree = 0
    domain_previous_break = Dyadic(0, 1)
    range_previous_break = Dyadic(0, 1)
    domain_depth = 1
    range_depth = 1
    domain_depth_counter = Dyadic(0, 1)
    range_depth_counter = Dyadic(0, 1)

    i = 1
    while i < len(domain_breaks):
        domain_current_break = domain_breaks[i]
        range_current_break = range_breaks[i]

        domain_current_break, range_current_break, to_decrement = \
            _correct_current_break(domain_current_break,
                                   domain_previous_break,
                                   domain_depth,
                                   range_current_break,
                                   range_previous_break,
                                   range_depth)
        i -= to_decrement

        new_domain_tree, domain_depth, domain_depth_counter = \
            _add_break_to_tree(domain_current_break, domain_previous_break,
                               new_domain_tree, domain_depth,
                               domain_depth_counter)
        new_range_tree, range_depth, range_depth_counter = \
            _add_break_to_tree(range_current_break, range_previous_break,
                               new_range_tree, range_depth,
                               range_depth_counter)

        domain_previous_break = domain_current_break
        range_previous_break = range_current_break
        i += 1

    new_tree_pair = \
        TreePair._internal_init(new_domain_tree, new_range_tree, 0)
    return new_tree_pair, rotation_amount



def _tree_to_hidden_breaks(tree: int, hsb: int) -> [Dyadic]:
    breaks = [Dyadic(0, 1)]

    if tree == 0:
        breaks.append(Dyadic(1, 1))
        return breaks

    current_position_in_tree = hsb
    number_of_ones = 0
    dyadic_counter = 1
    last_dyadic = Dyadic(0, 1)

    while current_position_in_tree > 0:
        current_position_in_tree -= 1

        if tree & (1 << current_position_in_tree):
            number_of_ones += 1
        else:
            if number_of_ones > 0:
                dyadic_counter <<= number_of_ones

            new_dyadic = last_dyadic + Dyadic(1, dyadic_counter)
            new_dyadic.simplify()

            breaks.append(new_dyadic)

            last_dyadic = new_dyadic

            if number_of_ones > 0:
                number_of_ones = 0
            else:
                dyadic_counter = new_dyadic._denominator

    return breaks



def _tree_pair_get_rotation_tree(n: int, to_return_length: bool = False):
    if n == 1:
        if to_return_length:
            return (0, 1)
        else:
            return 0

    previous_tree, length = _tree_pair_get_rotation_tree(n >> 1,
                                                    to_return_length = True)
    tree = 1

    tree <<= length
    tree += previous_tree
    tree <<= length
    tree += previous_tree

    if to_return_length:
        return (tree, 2 * length + 1)

    return tree



def _reduce_tree_pair(tree_pair: TreePair) -> TreePair:
    # TODO: documentation

    domain_tree = tree_pair.domain_tree
    range_tree = tree_pair.range_tree
    permutation = tree_pair.permutation

    domain_leaves = _tree_to_leaves(domain_tree)
    range_leaves = _tree_to_leaves(range_tree)

    while True:
        if domain_leaves == [0b10]:
            return TreePair("0", "0", 1)

        for i, leaf in enumerate(domain_leaves):
            if leaf & 0b1:
                continue
            if i + 1 == len(domain_leaves):
                continue
            if (domain_leaves[i + 1] >> 1) ^ (leaf >> 1):
                continue

            next_location = i - permutation

            if next_location < 0:
                next_location += len(range_leaves)
            if range_leaves[next_location] & 0b1:
                continue
            if next_location + 1 == len(range_leaves):
                continue
            if (range_leaves[next_location + 1] >> 1) ^ \
                    (range_leaves[next_location] >> 1):
                continue

            w1 = leaf >> 1
            w2 = range_leaves[next_location] >> 1
            break
        else:
            break

        domain_leaves = domain_leaves[:i] + [w1] + domain_leaves[i + 2:]
        range_leaves = range_leaves[:next_location] + [w2] + \
            range_leaves[next_location + 2:]

        if permutation > i:
            permutation -= 1

    domain_tree = _leaves_to_tree(domain_leaves)
    range_tree = _leaves_to_tree(range_leaves)

    return TreePair._internal_init(domain_tree, range_tree, permutation)



def _invert_tree_pair(tree_pair: TreePair) -> TreePair:
    # TODO: documentation

    hsb = _bitstring_get_highest_set_bit(tree_pair.domain_tree)
    num_leaves = _tree_pair_get_number_of_leaves(hsb)

    if num_leaves == 1:
        return tree_pair
    new_permutation = (num_leaves - tree_pair.permutation) % num_leaves

    domain_tree = tree_pair.domain_tree
    range_tree = tree_pair.range_tree

    return TreePair._internal_init(range_tree, domain_tree, new_permutation)



def _bitstring_get_highest_set_bit(bitstring: int) -> int:
    """Gets the highest set bit of an integer.

    Parameters
    ----------
    bitstring : int
        The integer to find the highest set bit of.

    Returns
    -------
    int
        The highest set bit of `bitstring`.

    Notes
    -----
    The algorithm is implemented as follows:
    TODO
    """
    number_of_shits = 0
    while bitstring != 0:
        bitstring >>= 1
        number_of_shits += 1
    return number_of_shits



def _tree_pair_get_number_of_leaves(highest_set_bit: int) -> int:
    """Gets the number of leaves in a tree pair, from its highest set bit.

    Parameters
    ----------
    highest_set_bit : int
        The highest set bit of the bitstring associated with the tree pair.

    Returns
    -------
    int
        The number of leaves in the tree pair.

    Notes
    -----
    The algorithm is implemented as follows:
    TODO
    """
    return (highest_set_bit >> 1) + 1



def _tree_to_leaves(tree: int) -> [int]:
    # TODO: documentation
    # TODO: disclaimer that this is a slow algorithm
    # TODO: what are leaves???

    current_position_in_tree = _bitstring_get_highest_set_bit(tree) - 1
    leaves = []
    # TODO: this is weird??? -- if this is unused anywhere else, change to
    # "None"?
    if tree == 0:
        return [0b10]

    leaves.append(0b10)
    leaves.append(0b11)

    current_position_in_leaves = 0

    while current_position_in_tree > 0:
        current_position_in_tree -= 1
        if tree & (1 << current_position_in_tree):
            leaves = leaves[:current_position_in_leaves + 1] + [0] + \
                leaves[current_position_in_leaves + 1:]
            leaves[current_position_in_leaves] <<= 1
            new_leaf = leaves[current_position_in_leaves]
            leaves[current_position_in_leaves + 1] = new_leaf + 1
        else:
            current_position_in_leaves += 1

    return leaves



def _leaves_to_breaks(leaves: [int]) -> [Dyadic]:
    # TODO: documentation
    # TODO: what are breaks???

    breaks = []
    for leaf in leaves:
        depth = 1
        hsb = _bitstring_get_highest_set_bit(leaf) - 1
        current_position_in_leaf = hsb
        dyadic_rational = Dyadic(0, 1)
        while current_position_in_leaf > 0:
            current_position_in_leaf -= 1
            depth <<= 1
            if leaf & (1 << current_position_in_leaf):
                dyadic_rational += Dyadic(1, depth)
                dyadic_rational.simplify()

        breaks.append(dyadic_rational)

    breaks.append(Dyadic(1, 1))
    return breaks



def _leaves_to_tree(leaves: [int]) -> int:
    # TODO: documentation
    # TODO: Algorithm...

    if leaves == [0b10]:
        return 0

    breaks = _leaves_to_breaks(leaves)

    return _breaks_to_tree(breaks)



def _breaks_to_tree(breaks: [Dyadic]) -> int:
    # TODO: documentation
    # TODO: Algorithm...

    tree = 0

    for i in range(1, len(breaks) - 1):
        current_rational = breaks[i]
        previous_rational = breaks[i - 1]

        if current_rational._denominator > previous_rational._denominator:
            exponent_difference = 0
            while current_rational._denominator > \
                        previous_rational._denominator:
                previous_rational._denominator <<= 1
                exponent_difference += 1

            tree <<= exponent_difference
            tree += (1 << exponent_difference) - 1

        tree <<= 1

    return tree << 1



"""Summary line.

Extended summary discussing functionality only.

Parameters
----------
x : type
    Description of parameter `x`.
y : optional
    Description of parameter `y` (with type not specified). (The default is..)

Returns
-------
As expected.

Notes
-----

Use Latex here...
:math:`a^2 + b^2 = c^2`
"""

# ============================================================================
# |                             Warning: Hacky!                              |
# ============================================================================

# This section is for multiplication.  This needs to be optimised.  TODO



def _mult_tree_pairs(tree_pair1: TreePair, tree_pair2: TreePair) -> TreePair:

    if tree_pair1 == TreePair("0", "0", 1):
        return tree_pair2
    if tree_pair2 == TreePair("0", "0", 1):
        return tree_pair1

    if USE_RIGHT_ACTIONS:
        lhs = tree_pair2
        rhs = tree_pair1
    else:
        lhs = tree_pair1
        rhs = tree_pair2

    lhs_domain_lines = _mult_get_tree_lines(lhs.domain_tree)
    lhs_range_lines = _mult_get_tree_lines(lhs.range_tree)
    rhs_domain_lines = _mult_get_tree_lines(rhs.domain_tree)
    rhs_range_lines = _mult_get_tree_lines(rhs.range_tree)

    middle_tree_lines = sorted(list(set(lhs_domain_lines).union(
                                                    set(rhs_range_lines))))

    lhs_domain_leaves = _mult_get_leaves_from_lines(lhs_domain_lines)
    lhs_range_leaves = _mult_get_leaves_from_lines(lhs_range_lines)
    rhs_domain_leaves = _mult_get_leaves_from_lines(rhs_domain_lines)
    rhs_range_leaves = _mult_get_leaves_from_lines(rhs_range_lines)

    new_domain = rhs_domain_lines

    for w in set(middle_tree_lines).difference(set(rhs_range_lines)):
        x = w
        while True:
            x = x[:-1]
            if x in rhs_range_lines:
                break
        p = x
        s = w[len(p):]
        pos = rhs_range_leaves.index(p)
        mapping_location = pos + rhs.permutation
        if mapping_location >= len(rhs_domain_leaves):
            mapping_location -= len(rhs_domain_leaves)
        x = rhs_domain_leaves[mapping_location]
        new_domain.append(x + s)

    new_range = lhs_range_lines

    for w in set(middle_tree_lines).difference(set(lhs_domain_lines)):
        x = w
        while True:
            x = x[:-1]
            if x in lhs_domain_lines:
                break
        p = x
        s = w[len(p):]
        pos = lhs_domain_leaves.index(p)
        mapping_location = pos - lhs.permutation
        if mapping_location < 0:
            mapping_location += len(lhs_range_leaves)
        x = lhs_range_leaves[mapping_location]
        new_range.append(x + s)

    new_domain_leaves = _mult_get_leaves_from_lines(new_domain)
    middle_tree_leaves = _mult_get_leaves_from_lines(middle_tree_lines)
    new_range_leaves = _mult_get_leaves_from_lines(new_range)

    if new_domain_leaves[0] == rhs_domain_leaves[0]:
        next_position = (len(rhs_range_leaves) - rhs.permutation) % \
                                                        len(rhs_range_leaves)
        middle_position = middle_tree_leaves.index(
                                            rhs_range_leaves[next_position])
    else:
        spine = new_domain_leaves[0][len(rhs_domain_leaves[0]):]
        next_position = (len(rhs_range_leaves) - rhs.permutation) % \
                                                        len(rhs_range_leaves)
        w = rhs_range_leaves[next_position] + spine
        middle_position = middle_tree_leaves.index(w)

    if middle_tree_leaves[middle_position] in lhs_domain_leaves:
        i = lhs_domain_leaves.index(middle_tree_leaves[middle_position])
        p = i - lhs.permutation
        if p < 0:
            p += len(lhs_range_leaves)
        start_position = new_range_leaves.index(lhs_range_leaves[p])
    else:
        full_word = middle_tree_leaves[middle_position]
        root = full_word
        while root not in lhs_domain_leaves:
            root = root[:-1]
        spine = full_word[len(root):]
        i = lhs_domain_leaves.index(root)
        p = i - lhs.permutation
        if p < 0:
            p += len(lhs_range_leaves)
        start_position = new_range_leaves.index(lhs_range_leaves[p] + spine)

    permutation = (len(new_range_leaves) - start_position) % \
                                                        len(new_range_leaves)
    new_domain = _mult_lines_to_tree(new_domain)
    new_range = _mult_lines_to_tree(new_range)


    return TreePair._internal_init(new_domain, new_range, permutation)



def _mult_get_tree_lines(tree: int) -> [str]:
    if tree == 0:
        return []
    lines = ["0","1"]
    lines_to_check = ["0","1"]
    for b in '{:0b}'.format(tree)[1:]:
        if b == "1":
            previous = lines_to_check[0]
            new = [previous + "0", previous + "1"]
            lines_to_check = new + lines_to_check[1:]
            lines += new
        else:
            lines_to_check = lines_to_check[1:]
    return lines



def _mult_get_leaves_from_lines(lines: [str]) -> [str]:
    l = sorted(lines)
    n = len(lines)
    i = 0
    while i < n:
        w = l[i]
        if w + "0" in l:
            l = l[:i] + l[i+1:]
            n -= 1
        else:
            i += 1
    return l



def _mult_lines_to_tree(lines: [str]) -> int:
    if lines == []:
        return 0
    prefix = "0"
    word = "0b"
    while True:
        if prefix in lines:
            word += "1"
            prefix += "0"
        else:
            word += "0"
            prefix = prefix[:-1]
            while prefix[-1] == "1":
                prefix = prefix[:-1]
                if prefix == "":
                    return int(word, 2)
            if prefix == "":
                return int(word, 2)
            prefix = prefix[:-1] + "10"
    return int(word, 2)

