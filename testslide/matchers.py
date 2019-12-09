import re


class _AndMatcher:
    """
    Equality is true if both "a" and "b" are true.
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return self.a == other and self.b == other

    def __repr__(self):
        return f"{self.a} & {self.b}"


class _XorMatcher:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return (self.a == other or self.b != other) and (
            self.a != other or self.b == other
        )

    def __repr__(self):
        return f"{self.a} ^ {self.b}"


class _InvMatcher:
    def __init__(self, matcher):
        self.matcher = matcher

    def __eq__(self, other):
        return not (self.matcher == other)

    def __repr__(self):
        return f"! {self.matcher}"


class _OrMatcher:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return self.a == other or self.b == other

    def __repr__(self):
        return f"{self.a} | {self.b}"


class _Matcher:
    """
    Allows composition of equality of objects by using bitwise operations.
    """

    def __and__(self, other):
        return _AndMatcher(self, other)

    def __xor__(self, other):
        return _XorMatcher(self, other)

    def __inv__(self):
        return _InvMatcher(self)

    def __or__(self, other):
        return _OrMatcher(self, other)


class regex_match(_Matcher):
    """
    Compares true if other mathes given regex.
    """

    def __init__(self, pattern, flags=0):
        self.pattern = pattern
        self.flags = flags
        self.prog = re.compile(pattern, flags)

    def __eq__(self, other):
        if not isinstance(other, str):
            return False
        return bool(self.prog.match(other))

    def __repr__(self):
        return "<regex_match 0x{:02X} pattern={}{}>".format(
            id(self),
            repr(self.pattern),
            f" flags={self.flags}" if self.flags != 0 else "",
        )


class _RichComparison(_Matcher):
    def __init__(self, klass, lt=None, le=None, eq=None, ne=None, ge=None, gt=None):
        self.klass = klass
        self.lt = lt
        self.le = le
        self.eq = eq
        self.ne = ne
        self.ge = ge
        self.gt = gt

    def __eq__(self, other):
        if not isinstance(other, self.klass):
            return False
        if self.lt is not None and not (other < self.lt):
            return False
        if self.le is not None and not (other <= self.le):
            return False
        if self.eq is not None and not (other == self.eq):
            return False
        if self.ne is not None and not (other != self.ne):
            return False
        if self.ge is not None and not (other >= self.ge):
            return False
        if self.gt is not None and not (other > self.gt):
            return False
        return True

    def __repr__(self):
        return "<{} 0x{:02X}{}{}{}{}{}{}>".format(
            type(self).__name__,
            id(self),
            f" lt={self.lt}" if self.lt is not None else "",
            f" le={self.le}" if self.le is not None else "",
            f" eq={self.eq}" if self.eq is not None else "",
            f" ne={self.ne}" if self.ne is not None else "",
            f" ge={self.ge}" if self.ge is not None else "",
            f" gt={self.gt}" if self.gt is not None else "",
        )


class float_comparison(_RichComparison):
    """
    Compares true if other number passes all rich comparison cases given.
    """

    def __init__(self, lt=None, le=None, eq=None, ne=None, ge=None, gt=None):
        super().__init__(float, lt=lt, le=le, eq=eq, ne=ne, ge=ge, gt=gt)


class int_comparison(_RichComparison):
    """
    Compares true if other number passes all rich comparison cases given.
    """

    def __init__(self, lt=None, le=None, eq=None, ne=None, ge=None, gt=None):
        super().__init__(int, lt=lt, le=le, eq=eq, ne=ne, ge=ge, gt=gt)
