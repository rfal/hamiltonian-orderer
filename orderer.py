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
    def __init__(self, symbols):
        if not symbols or ZERO in symbols:
            self.symbols = [ZERO]
        elif symbols == [ONE]:
            self.symbols = symbols
        else:
            self.symbols = sorted([s for s in symbols if s != ONE]) # Thank God sorted() is stable!

    def __eq__(A, B):
        return A.symbols == B.symbols

    def __lt__(A, B):
        dom_a = A._dominant()
        dom_b = B._dominant()

        deg_dom_a = A._num_symbols_like(name=dom_a.name, behavior=dom_a.behavior)
        deg_dom_b = B._num_symbols_like(name=dom_b.name, behavior=dom_b.behavior)

        num_dags_a = A._num_symbols_like(name=dom_a.name, behavior=dom_a.behavior, dag=True)
        num_dags_b = B._num_symbols_like(name=dom_b.name, behavior=dom_b.behavior, dag=True)

        if dom_a.behavior != dom_b.behavior:
            return dom_a < dom_b
        elif deg_dom_a != deg_dom_b:
            return deg_dom_a < deg_dom_b
        elif dom_a.name != dom_b.name:
            return dom_a.name > dom_b.name
        elif num_dags_a != num_dags_b:
            return num_dags_a < num_dags_b
        else:
            same_normalness = (not A._more_normal_than(B, dom_a)) and (not B._more_normal_than(A, dom_b))
            if not same_normalness:
                return B._more_normal_than(A, dom_b)
            else:
                return A._delete_dominant() < B._delete_dominant()

    def __str__(self):
        groups = self._group_symbols()
        str_group = lambda x: str(x[0]) + ("^" + str(x[1]) if x[1] > 1 else "")
        
        return '.'.join(map(str_group, groups))

    def _group_symbols(self):
        '''
        Groups identical symbols into a couple (Symbol, power) for treatment by _str_grouped_symbols.

        Returns a list of such couples that bijectively represents the Term object.
        '''
        symbols = self.symbols
        
        res = []
        i = 0
        while i < len(symbols):
            s = symbols[i]
            j = 1
            while i + j < len(symbols) and symbols[i + j] == s:
                j += 1
            
            g = (s, j)
            res.append(g)

            i += j

        return res

    def _num_symbols_like(self, name=None, behavior=None, dag=None):
        '''
        Return the number of Symbols in a Term matching the given properties when specified.
        '''
        symbol_selection = self.symbols

        if name is not None:
            symbol_selection = [s for s in symbol_selection if s.name == name]
        if behavior is not None:
            symbol_selection = [s for s in symbol_selection if s.behavior == behavior]
        if dag is not None:
            symbol_selection = [s for s in symbol_selection if s.dag == dag]

        return len(symbol_selection)

    def _symbols_in(self):
        '''
        Return the ordered list of Symbols in a Term with no duplicates, all symbols having dag == False.
        '''
        symbols_undagged = [Symbol(s.name, s.behavior, dag=False) for s in self.symbols]

        res = []
        for s in symbols_undagged:
            if s not in res:
                res.append(s)

        return res

    def _dominant(self):
        '''
        Return the Symbol with the highest ordering priority in a Term, regardless of its dag attribute.
        '''
        symbols = self._symbols_in()
        max_behavior = max(self.symbols).behavior

        max_behavior_symbols = [s for s in symbols if s.behavior == max_behavior]

        return min(max_behavior_symbols)

    def _more_normal_than(self, t, sym):
        '''
        Return True if the normal ordering of dagged operators is better respected in self than in Term t regarding Symbol sym.
        '''
        if sym.behavior != 'annihilation':
            return False

        sym_list1 = [s for s in self.symbols if s == sym or s == sym.conj()]
        sym_list2 = [s for s in t.symbols if s == sym or s == sym.conj()]

        if len(sym_list1) != len(sym_list2):
            raise Exception('Compared terms do not have the same order in ' + sym.name + '.')

        n = len(sym_list1)
        go_on = True
        k = 0

        while go_on and k < n:
            d1 = sym_list1[k].dag
            d2 = sym_list2[k].dag

            if d1 and not d2 :
                return True

            go_on = (d1 == d2)
            k += 1

        return False

    def _delete_dominant(self):
        '''
        Return the same Term with all occurencces of its dominant symbol deleted.
        '''
        dom = self._dominant()
        new_symbols = [s for s in self.symbols if s != dom and s.conj() != dom]

        return Term(new_symbols)

class Expression:
    pass