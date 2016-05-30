class Symbol:
    '''
    A symbol represents any scalar or operator in an expression. It has a symbol name, a behavior (subset with special properties to which it belongs) and a dagger attribute.

    The list of all implemented behaviors is a class attributes, as well as the list of those behaviors which are hermitian (invariant under conjugation).
    '''
    _behaviors = ['zero', 'one', 'real', 'complex', 'annihilation'] # List of implemented behaviors for symbols (order matters for comparison!)
    _hermitian_behaviors = ['zero', 'one', 'real'] # List of Hermitian behaviors for which the conj property is always False

    def __init__(self, name, behavior, dag=False):
        if behavior not in self._behaviors:
            raise Exception('Behavior "' + behavior + '" not implemented.')

        self.name = name
        self.behavior = behavior

        if behavior in self._hermitian_behaviors:
            self.dag = False
        else:
            self.dag = dag

    def __eq__(a, b):
        return str(a) == str(b) and a.behavior == b.behavior and a.dag == b.dag # The str thing just enables us to compare zeros and ones, because a girl has no name

    def __ne__(a,b):
        return not (a == b)

    def __lt__(a, b):
        i_b_a = a._behaviors.index(a.behavior)
        i_b_b = b._behaviors.index(b.behavior)

        if i_b_a != i_b_b:
            return i_b_a < i_b_b # We want the same order as the specified _behaviors list
        else:
            if a.behavior == "zero" or a.behavior == "one":
                return False # All the zeros and the ones are the same
            else:
                if a.name != b.name:
                    return a.name < b.name # Inside the same behavior we use the lexicographical orber
                else:
                    return False


    def __le__(a, b):
        return a < b or a == b or a.conj() == b or a.behavior == "zero" or a.behavior == "one" # Just because zero and one can have several names

    def __gt__(a,b):
        return b < a

    def __ge__(a,b):
        return b <= a

    def __str__(self):
        if self.behavior == 'zero':
            return '0'
        elif self.behavior == 'one':
            return '1'
        else:
            res = self.name
            if self.dag:
                res = res + '*'

            return res

    def conj(self):
        if self.name not in self._hermitian_behaviors:
            return Symbol(self.name, self.behavior, not self.dag)
        else:
            return Symbol(self.name, self.behavior, False)

ZERO = Symbol('0', 'zero')
ONE = Symbol('1', 'one')

class Term:
    pass

class Expression:
    pass