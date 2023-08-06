#!/usr/bin/env python
# coding=UTF-8

class ValueExhaustive(object) :
    """Exhaust all the operators for the objects to calculation."""
    
    def __init__(self, objects, *args) :
        """ValueExhaustive(iterable, operator1, operator2, operator3)
or ValueExhaustive(iterable, operators)
Create a ValueExhaustive object.
Use self.calculate() to calculate and return a tuple.
Use self.calculatepairs() to calculate and return a dict.
Use self.listexpr() to list all possible expressions as a tuple.
E.g.
>>> ValueExhaustive((3, 2, 1), "+-", "*/").listexpr()
("3+2*1", "3+2/1", "3-2*1", "3-2/1")
>>> ValueExhaustive((2, 4, 6, 8, 10), "+-").listexpr()
('2+4+6+8+10', '2+4+6+8-10', '2+4+6-8+10', '2+4+6-8-10', '2+4-6+8+10',
'2+4-6+8-10', '2+4-6-8+10', '2+4-6-8-10', '2-4+6+8+10', '2-4+6+8-10',
'2-4+6-8+10', '2-4+6-8-10', '2-4-6+8+10', '2-4-6+8-10', '2-4-6-8+10',
'2-4-6-8-10')
>>> ValueExhaustive((2, 4, 6, 8, 10), "+-").calculate()
(30, 10, 14, -6, 18, -2, 2, -18, 22, 2, 6, -14, 10, -10, -6, -26)
>>> ValueExhaustive((2, 4, 6, 8, 10), "+-").calculatepairs()
{'2+4+6+8+10': 30, '2+4+6+8-10': 10, '2+4+6-8+10': 14, '2+4+6-8-10': -6,
'2+4-6+8+10': 18, '2+4-6+8-10': -2, '2+4-6-8+10': 2, '2+4-6-8-10': -18,
'2-4+6+8+10': 22, '2-4+6+8-10': 2, '2-4+6-8+10': 6, '2-4+6-8-10': -14,
'2-4-6+8+10': 10, '2-4-6+8-10': -10, '2-4-6-8+10': -6, '2-4-6-8-10': -26}"""
        
        try :
            object_amount = 0
            _objects = ()
            for i in objects :
                object_amount = object_amount + 1
                _objects = _objects + (i,)
        except TypeError :
            raise TypeError("'%s' object is not iterable"%type(objects))
        
        if len(args) == 0 :
            raise TypeError("ValueExhaustive expected 2 argument, got 1")
        elif len(args) == 1 :
            args = args * (object_amount-1)
        else :
            if object_amount - 1 > len(args) :
                raise TypeError("too few operators for all the objects")
            args = args[0:object_amount-1]
        try :
            for i in args :
                for j in i :
                    pass
        except TypeError :
            raise TypeError("'%s' object is not iterable"%type(i))
        self.objects = _objects
        self.operators = args
    
    def __repr__(self) :
        """Return repr(self)."""
        
        return "ValueExhaustive(%s, %s)" % (repr(self.objects),
                                            repr(self.operators)[1:-1])
    
    def __eq__(self, value) :
        """Return self==value."""
        
        try :
            return self.objects == value.objects and \
                   self.operators == value.operators
        except AttributeError :
            return not not 0
    
    def __ne__(self, value) :
        """Return self!=value."""
        
        return not(self == value)
    
    def listexpr(self) :
        exec_prod = []
        exec_expr = "res=()\n"
        space_width = 0
        double_tuplerange = ()
        for i in tuple(range(len(self.operators))) :
            double_tuplerange = double_tuplerange + (i, i)
        for i in range(len(self.operators)) :
            exec_expr = exec_expr + " " * space_width + \
                        "for i%d in self.operators[%d]:\n" % (i, i)
            space_width = space_width + 1
        exec_expr = exec_expr + " " * space_width + "res=res+(str(" + \
                    ("repr(eval('self.objects[%d]'))+'%%s'%%i%d+"*\
                    len(self.operators)) % double_tuplerange + \
                    "repr(eval('self.objects[%d]')))" % \
                    len(self.operators) + ",)\nexec_prod.append(res)"
        exec(exec_expr)
        return exec_prod[0]
    
    def calculate(self) :
        exec_prod = []
        exec_expr = "res=()\n"
        space_width = 0
        for i in range(len(self.operators)) :
            exec_expr = exec_expr + " " * space_width + \
                        "for i%d in self.operators[%d]:\n" % (i, i)
            space_width = space_width + 1
        exec_expr = exec_expr + " " * space_width + "res=res+(eval('" + \
                    ("self.objects[%d]%%s"*len(self.operators)) % \
                    tuple(range(len(self.operators))) + \
                    "self.objects[%d]'%%(" % len(self.operators) + \
                    ("i%d,"*len(self.operators)) % \
                    tuple(range(len(self.operators))) + \
                    ")),)\nexec_prod.append(res)"
        exec(exec_expr)
        return exec_prod[0]
    
    def calculatepairs(self) :
        keys = self.listexpr()
        values = self.calculate()
        res = {}
        for i in range(len(keys)) :
            res[keys[i]] = values[i]
        return res
