from math import gcd

# TODO: Documentation. (Change name to "Rational?")

class Rational():

    def __init__(self, numerator: int, denominator: int):
        if not (isinstance(numerator, int) and isinstance(denominator, int)):
            raise ValueError("Rationals have integral parts")
        if denominator == 0:
            raise ValueError("Rationals have non-zero denominators")

        self._numerator = abs(numerator)
        self._denominator = abs(denominator)
        self._is_negative = (numerator < 0) ^ (denominator < 0)


    def __float__(self):
        num = self._numerator / self._denominator
        if self._is_negative:
            return -num
        return num


    def __int__(self):
        num = self._numerator // self._denominator
        if self._is_negative:
            return -num
        return num


    def __neg__(self):
        if self._is_negative:
            return Rational(self._numerator, self._denominator)
        return Rational(-self._numerator, self._denominator)


    def __abs__(self):
        return Rational(self._numerator, self._denominator)


    def __invert__(self):
        coefficient = (-1) ** self._is_negative
        return Rational(coefficient * self._denominator, self._numerator)


    def simplify(self):
        g = gcd(self._numerator, self._denominator)
        self._numerator //= g
        self._denominator //= g

        # Turn into a Dyadic if we can
        if self._denominator & (self._denominator - 1) == 0:
            denominator = self._denominator
            numerator = self._numerator
            is_negative = self._is_negative
            self.__class__ = Dyadic
            self._numerator = numerator
            self._denominator = denominator
            self._is_negative = is_negative

        return self


    def simplified(self):
        g = gcd(self._numerator, self._denominator)
        numerator = self._numerator // g
        denominator = self._denominator // g
        coefficient = (-1) ** self._is_negative

        # Return a Dyadic if we can
        if denominator & (denominator - 1) == 0:
            return Dyadic(coefficient * numerator, denominator)

        return Rational(coefficient * numerator, denominator)


    def to_tex(self):
        if self._is_negative:
            return r"\frac{-%s}{%s}" % (str(self._numerator),
                                       str(self._denominator))
        return r"\frac{%s}{%s}" % (str(self._numerator),
                                   str(self._denominator))


    def __str__(self):
        if self._is_negative:
            return r"-%s/%s" % (str(self._numerator), str(self._denominator))
        return r"%s/%s" % (str(self._numerator), str(self._denominator))


class Dyadic(Rational):

    def __init__(self, numerator: int, denominator: int):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise ValueError("Dyadics have integral parts")
        if denominator == 0:
            raise ValueError("Dyadics have non-zero denominators")

        # This is a nice way to check that the denominator is a power of 2.
        if abs(denominator) & (abs(denominator) - 1) != 0:
            raise ValueError("Dyadics must have a denominator that is a " + \
                    "power of two.")

        self._numerator = abs(numerator)
        self._denominator = abs(denominator)
        self._is_negative = (numerator < 0) ^ (denominator < 0)


    def __neg__(self):
        if self._is_negative:
            return Dyadic(self._numerator, self._denominator)
        return Dyadic(-self._numerator, self._denominator)


    def __abs__(self):
        return Dyadic(self._numerator, self._denominator)


    def __add__(self, other):
        if isinstance(other, int):
            return _dyadic_add(self, Dyadic(other, 1))

        if isinstance(other, float):
            return float(self) + other

        if not isinstance(other, Dyadic):
            return NotImplemented

        return _dyadic_add(self, other)


    def __radd__(self, other):
        return self + other


    def __iadd__(self, other):
        if isinstance(other, int):
            d = Dyadic(other, 1)
        else:
            d = other
        if not isinstance(d, Dyadic):
            return NotImplemented

        numerator = d._numerator
        denominator = d._denominator

        while self._denominator < denominator:
            self._numerator <<= 1
            self._denominator <<= 1
        while self._denominator > denominator:
            numerator <<= 1
            denominator <<= 1

        if self._is_negative ^ d._is_negative:
            if self._is_negative:
                self._numerator = numerator - self._numerator
                if self._numerator < 0:
                    self._numerator = abs(self._numerator)
                else:
                    self._is_negative = False
            else:
                self._numerator -= numerator
                if self._numerator < 0:
                    self._numerator = abs(self._numerator)
                    self._is_negative = True
        else:
            self._numerator += numerator

        return self


    def __mul__(self, other):
        if isinstance(other, int):
            return _dyadic_multiply(self, Dyadic(other, 1))

        if isinstance(other, float):
            return float(self) * other

        if not isinstance(other, Dyadic):
            return NotImplemented

        return _dyadic_multiply(self, other)


    def __rmul__(self, other):
        return self * other


    def __imul__(self, other):
        if isinstance(other, int):
            d = Dyadic(other, 1)
        else:
            d = other
        if not isinstance(d, Dyadic):
            return NotImplemented

        numerator = other._numerator
        denominator = other._denominator

        while denominator != 1:
            self._denominator <<= 1
            denominator >>= 1

        self._numerator *= numerator
        self._is_negative ^= other._is_negative

        return self


    def __sub__(self, other):
        if not (isinstance(other, int) or isinstance(other, float) or \
                isinstance(other, Dyadic)):
            return NotImplemented

        return self + (-other)


    def __rsub__(self, other):
        if not (isinstance(other, int) or isinstance(other, float) or \
                isinstance(other, Dyadic)):
            return NotImplemented
        return -self + other


    def __isub__(self, other):
        if isinstance(other, int):
            d = Dyadic(other, 1)
        else:
            d = other
        if not isinstance(d, Dyadic):
            return NotImplemented

        numerator = d._numerator
        denominator = d._denominator
        is_negative = d._is_negative ^ True

        while self._denominator < denominator:
            self._numerator <<= 1
            self._denominator <<= 1
        while self._denominator > denominator:
            numerator <<= 1
            denominator <<= 1

        if self._is_negative ^ is_negative:
            if self._is_negative:
                self._numerator = numerator - self._numerator
                if self._numerator < 0:
                    self._numerator = abs(self._numerator)
                else:
                    self._is_negative = False
            else:
                self._numerator -= numerator
                if self._numerator < 0:
                    self._numerator = abs(self._numerator)
                    self._is_negative = True
        else:
            self._numerator += numerator

        return self


    def __eq__(self, other):
        if isinstance(other, int):
            return self == Dyadic(other, 1)
        if isinstance(other, float):
            return float(self) == other
        if not isinstance(other, Dyadic):
            return False
        if self._numerator != other._numerator:
            return False
        if self._denominator != other._denominator:
            return False
        return self._is_negative == other._is_negative


    def __lt__(self, other):
        if isinstance(other, int):
            return _dyadic_less_than(self, Dyadic(other, 1))

        if isinstance(other, float):
            return float(self) < other

        if not isinstance(other, Dyadic):
            return NotImplemented

        return _dyadic_less_than(self, other)


    def __le__(self, other):
        if isinstance(other, int):
            d = Dyadic(1, other)
        elif isinstance(other, float):
            return float(self) <= other
        elif not isinstance(other, Dyadic):
            return NotImplemented
        else:
            d = other

        if self._is_negative ^ d.is_negative:
            if self._is_negative:
                return True
            return False

        numerator1 = dyadic1._numerator
        denominator1 = dyadic1._denominator
        numerator2 = d._numerator
        denominator2 = d._denominator

        while denominator1 < denominator2:
            numerator1 <<= 1
            denominator1 <<= 1
        while denominator1 < denominator2:
            numerator2 <<= 1
            denominator2 <<= 1

        if dyadic1._is_negative:
            if numerator2 <= numerator1:
                return True
            return False
        if numerator1 <= numerator2:
            return True
        return False


    def __gt__(self, other):
        if isinstance(other, int):
            return _dyadic_less_than(Dyadic(other, 1), self)

        if isinstance(other, float):
            return float(self) > other

        if not isinstance(other, Dyadic):
            return NotImplemented

        return _dyadic_less_than(other, self)


    def __ge__(self, other):
        if isinstance(other, int):
            d = Dyadic(1, other)
        elif isinstance(other, float):
            return float(self) >= other
        elif not isinstance(other, Dyadic):
            return NotImplemented
        else:
            d = other

        if self._is_negative ^ d.is_negative:
            if self._is_negative:
                return False
            return True

        numerator1 = dyadic1._numerator
        denominator1 = dyadic1._denominator
        numerator2 = d._numerator
        denominator2 = d._denominator

        while denominator1 < denominator2:
            numerator1 <<= 1
            denominator1 <<= 1
        while denominator1 < denominator2:
            numerator2 <<= 1
            denominator2 <<= 1

        if dyadic1._is_negative:
            if numerator2 >= numerator1:
                return True
            return False
        if numerator1 >= numerator2:
            return True
        return False


    def simplify(self):
        if self._numerator == 0:
            self._denominator = 1
            return self

        # While neither has 1 as LSB.
        while ((self._numerator | self._denominator) & 0b1) ^ 0b1:
            self._numerator >>= 1
            self._denominator >>= 1

        return self


    def simplified(self):
        if self._numerator == 0:
            return Dyadic(0, 1)

        numerator = self._numerator
        denominator = self._denominator

        # While neither has 1 as LSB.
        while ((numerator | denominator) & 0b1) ^ 0b1:
            numerator >>= 1
            denominator >>= 1

        coefficient = (-1) ** self._is_negative

        return Dyadic(coefficient * numerator, denominator)


    def __repr__(self):
        if self._is_negative:
            return r"%s(-%s, %s)" % (type(self).__name__,
                                repr(self._numerator),repr(self._denominator))

        return r"%s(%s, %s)" % (type(self).__name__, repr(self._numerator),
                                repr(self._denominator))



def dyadic_gradient(coord1: (Dyadic, Dyadic), coord2: (Dyadic, Dyadic)) -> \
                                                                    Rational:
    x1_numerator = coord1[0]._numerator
    x1_denominator = coord1[0]._denominator
    y1_numerator = coord1[1]._numerator
    y1_denominator = coord1[1]._denominator
    x2_numerator = coord2[0]._numerator
    x2_denominator = coord2[0]._denominator
    y2_numerator = coord2[1]._numerator
    y2_denominator = coord2[1]._denominator

    m = max(x1_denominator, x2_denominator, y1_denominator, y2_denominator)

    while x1_denominator != m:
        x1_numerator <<= 1
        x1_denominator <<= 1
    while x2_denominator != m:
        x2_numerator <<= 1
        x2_denominator <<= 1
    while y1_denominator != m:
        y1_numerator <<= 1
        y1_denominator <<= 1
    while y2_denominator != m:
        y2_numerator <<= 1
        y2_denominator <<= 1

    x1_coef = (-1) ** coord1[0]._is_negative
    x2_coef = (-1) ** coord2[0]._is_negative
    y1_coef = (-1) ** coord1[1]._is_negative
    y2_coef = (-1) ** coord2[1]._is_negative

    x1 = x1_coef * x1_numerator
    x2 = x2_coef * x2_numerator
    y1 = y1_coef * y1_numerator
    y2 = y2_coef * y2_numerator

    result = Rational(y2 - y1, x2 - x1)

    return result.simplify()



def dyadic_is_power_of_two(dyadic: Dyadic) -> bool:
    if not isinstance(dyadic, Dyadic):
        raise ValueError

    dyadic = dyadic.simplified()
    if dyadic._numerator == 1 and \
            (dyadic._denominator & (dyadic._denominator - 1) == 0):
        return True
    if dyadic._denominator == 1 and \
            (dyadic._numerator & (dyadic._numerator - 1) == 0):
        return True
    return False



def _dyadic_add(dyadic1: Dyadic, dyadic2: Dyadic) -> Dyadic:
    numerator1 = dyadic1._numerator
    denominator1 = dyadic1._denominator
    numerator2 = dyadic2._numerator
    denominator2 = dyadic2._denominator

    while denominator1 < denominator2:
        numerator1 <<= 1
        denominator1 <<= 1
    while denominator1 > denominator2:
        numerator2 <<= 1
        denominator2 <<= 1

    if dyadic1._is_negative ^ dyadic2._is_negative:
        if dyadic1._is_negative:
            return Dyadic(numerator2 - numerator1, denominator1)
        return Dyadic(numerator1 - numerator2, denominator1)

    coefficient = (-1) ** dyadic1._is_negative
    return Dyadic(coefficient * (numerator1 + numerator2), denominator1)



def _dyadic_multiply(dyadic1: Dyadic, dyadic2: Dyadic) -> Dyadic:
    numerator1 = dyadic1._numerator
    denominator1 = dyadic1._denominator
    numerator2 = dyadic2._numerator
    denominator2 = dyadic2._denominator

    while denominator2 != 1:
        denominator1 <<= 1
        denominator2 >>= 1

    coefficient = (-1) ** (dyadic1._is_negative ^ dyadic2._is_negative)

    return Dyadic(coefficient * numerator1 * numerator2, denominator1)



def _dyadic_less_than(dyadic1: Dyadic, dyadic2: Dyadic) -> Dyadic:
    if dyadic1._is_negative ^ dyadic2._is_negative:
        if dyadic1._is_negative:
            return True
        return False

    numerator1 = dyadic1._numerator
    denominator1 = dyadic1._denominator
    numerator2 = dyadic2._numerator
    denominator2 = dyadic2._denominator

    while denominator1 < denominator2:
        numerator1 <<= 1
        denominator1 <<= 1
    while denominator1 > denominator2:
        numerator2 <<= 1
        denominator2 <<= 1

    if dyadic1._is_negative:
        if numerator2 < numerator1:
            return True
        return False
    if numerator1 < numerator2:
        return True
    return False

