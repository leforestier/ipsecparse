import operator

__all__ = ['Key', 'Keys']

class Expression(object):

    def evaluate(self, dct):
        raise NotImplementedError
        
    def __call__(self, dct):
        return self.evaluate(dct)
        
    def __eq__(self, arg):
        return BinaryOperation(operator.eq, self, arg)
        
    def __ne__(self, arg):
        return BinaryOperation(operator.ne, self, arg)
        
    def __and__(self, arg):
        return BinaryOperation(operator.and_, self, arg)
        
    def __or__(self, arg):
        return BinaryOperation(operator.or_, self, arg)

   
class Key(Expression):
    def __init__(self, name):
        self.name = name
        
    def evaluate(self, dct):
        return dct.get(self.name)
        
    def startswith(self, string):
        return BinaryOperation(str.startswith, self, string)


class Keys(Expression):
    def __init__(self, *args):
        self.names = args
        
    def evaluate(self, dct):
        return tuple(dct.get(name) for name in self.names)
        
    def contains(self, arg):
        return BinaryOperation(operator.contains, self, arg)
        

class BinaryOperation(Expression):
        
    def __init__(self, op, arg1, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        
    def evaluate(self, dct):
        arg1, arg2 = (
            arg.evaluate(dct)
            if isinstance(arg, Expression)
            else arg
            for arg in (self.arg1, self.arg2)
        )
        return self.op(arg1, arg2)
