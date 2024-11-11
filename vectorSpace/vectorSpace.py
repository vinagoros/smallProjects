class R2Vector:
    def __init__(self, *, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return sum(val ** 2 for val in vars(self).values()) ** 0.5

    def __str__(self): #to string
        return str(tuple(getattr(self, i) for i in vars(self)))

    def __repr__(self): #representation of object instatiation
        arg_list = [f'{key}={val}' for key, val in vars(self).items()]
        args = ', '.join(arg_list)
        return f'{self.__class__.__name__}({args})'

    def __add__(self, other): #use of + operator
        if type(self) != type(other):
            return NotImplemented
        kwargs = {i: getattr(self, i) + getattr(other, i) for i in vars(self)}
        return self.__class__(**kwargs)

    def __sub__(self, other): #use of - operator
        if type(self) != type(other):
            return NotImplemented
        kwargs = {i: getattr(self, i) - getattr(other, i) for i in vars(self)}
        return self.__class__(**kwargs)

    def __mul__(self, other): #use of * operator
        if type(other) is not (int or float):
            return NotImplemented
        else:
            kwargs = {i: getattr(self, i) * other for i in vars(self)}
            return self.__class__(**kwargs)

    def __eq__(self, other): #use of equality operator
        if type(self) != type(other):
            return NotImplemented
        return all([getattr(self, i) == getattr(other, i) for i in vars(self)])

    def __ne__(self, other): #use of not equals
        return not self == other

    def __lt__(self, other): #less than
        if type(self) != type(other):
            return NotImplemented
        return self.norm() < other.norm()

    def __gt__(self, other): #greater than
        if type(self) != type(other):
            return NotImplemented
        return self.norm() > other.norm()

    def __le__(self, other): #<=
        return not self > other

    def __ge__(self, other): #>=
        return not self < other


class R3Vector(R2Vector):
    def __init__(self, *, x, y, z):
        super().__init__(x=x, y=y)
        self.z = z

    def cross(self, other):
        if type(self) != type(other):
            return NotImplemented
        kwargs = {
            'x': self.y * other.z - self.z * other.y,
            'y': self.z * other.x - self.x * other.z,
            'z': self.x * other.y - self.y * other.x
        }

        return self.__class__(**kwargs)


v1 = R3Vector(x=2, y=3, z=1)