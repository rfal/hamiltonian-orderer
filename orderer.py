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

        if ' ' in name:
            raise Exception("A Symbol's name cannot contain spaces.")

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
            behavior = a.behavior
            if behavior == "zero" or behavior == "one":
                return False # All the zeros and the ones are the same
            else:
                if a.name != b.name:
                    return a.name < b.name # Inside the same behavior we use the lexicographical orber
                elif a.dag != b.dag and behavior != 'annihilation':
                    return a.dag # Dagged symbols come before when they commute
                else:
                    return False

    def __gt__(a, b):
        return b < a

    def __le__(a, b):
        return not a > b

    def __ge__(a, b):
        return not a < b

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

    def __repr__(self):
        return "Symbol('{}', '{}', dag={})".format(self.name, self.behavior, self.dag)

    def __mul__(a, b):
        if isinstance(b, Symbol):
            return Term([a, b])
        else:
            return NotImplemented

    def __add__(a, b):
        if isinstance(b, Symbol):
            return Expression([Term([a]), Term([b])])
        else:
            return NotImplemented

    def conj(self):
        if self.name not in self._hermitian_behaviors:
            return Symbol(self.name, self.behavior, not self.dag)
        else:
            return Symbol(self.name, self.behavior, False)

ZERO = Symbol('0', 'zero')
ONE = Symbol('1', 'one')

class Term:
    '''
    A Term is a product of Symbols and can be instanciated as such. It has a list of symbols as its only attribute and can be bijectively represented by a string in the form
        "s_1^k_1 s_2^k_2 ... s_n^k_n"
    where the s_is are Symbols or conjugates of Symbols. Some default symbols are defined in the class attribute _default_bank that is used by default when instanciated a Term using such a string.

    Terms are totally ordered in a recursive manner according to the order relationship "I naturally write this Term to the *right* of that Term in an Expression".
    '''
    _default_bank = [Symbol('k', 'real'), Symbol('n', 'real'), Symbol('x', 'real'), Symbol('xi', 'complex'), Symbol('zeta', 'complex'), Symbol('z', 'complex'), Symbol('a', 'annihilation'), Symbol('b', 'annihilation')]

    def __init__(self, info=[], bank=None):
        if bank is None:
            bank = self._default_bank

        if isinstance(info, str):
            if any(bank.count(s) > 1 for s in bank):
                raise Exception('The symbol bank given is ambiguous.')

            if ZERO not in bank:
                bank.append(ZERO)

            if ONE not in bank:
                bank.append(ONE)

            infos = info.split(' ')

            symbols = []

            for i in infos:
                i_sym_pow = i.split('^')
                i_sym, i_pow = (i_sym_pow[0], int(i_sym_pow[1])) if '^' in i else (i, 1)

                if not i_sym:
                    i_sym = '1' # Simplest way to implement the fact that an empty product is 1

                if i_sym[-1] == '*':
                    i_sym = i_sym[:-1]
                    dag = True
                else:
                    dag = False
                
                try:
                    new_s = next(s for s in bank if s.name == i_sym)
                except StopIteration:
                    raise Exception("Unknown symbol '" + i_sym + "'.")

                if dag:
                    new_s = new_s.conj()
                
                symbols.extend([new_s] * i_pow)

            self.__init__(symbols)
        elif isinstance(info, list):
            symbols = info
            if ZERO in symbols:
                self.symbols = [ZERO]
            elif not symbols or all(s == ONE for s in symbols):
                self.symbols = [ONE] # An empty product is equal to 1
            else:
                self.symbols = sorted([s for s in symbols if s != ONE]) # Thank God sorted() is stable!
        else:
            raise Exception('Term constructor argument should be a string or a list of Symbols.')

    def __eq__(A, B):
        return A.symbols == B.symbols

    def __lt__(A, B):
        '''
        Recursively determine if A is 'smaller' than B, meaning that A would be naturally written after B.
        '''
        # Base cases
        if ZERO in B.symbols:
            return False
        elif B.symbols == [ONE]:
            return ZERO in A.symbols

        # First compare the total degree of A and B according to complex and annihilation symbols (becauses complex symbols are supposed to vary in time, so that they count)
        # Note that if this comparison holds through the recursion
        deg_a = A._num_symbols_like(behavior='complex') + A._num_symbols_like(behavior='annihilation')
        deg_b = B._num_symbols_like(behavior='complex') + B._num_symbols_like(behavior='annihilation')

        if deg_a != deg_b:
            return deg_a < deg_b

        # From now on we only consider the dominant symbol in A and B
        dom_a = A._dominant()
        dom_b = B._dominant()

        # First compare the dominant symbols' behaviors
        if dom_a.behavior != dom_b.behavior:
            return dom_a < dom_b

        # Then compare their degree according to the dominant symbol
        deg_dom_a = A._num_symbols_like(name=dom_a.name, behavior=dom_a.behavior)
        deg_dom_b = B._num_symbols_like(name=dom_b.name, behavior=dom_b.behavior)

        if deg_dom_a != deg_dom_b:
            return deg_dom_a < deg_dom_b

        # Then compare the name of the dominant symbol (reverse order)
        if dom_a.name != dom_b.name:
            return dom_a.name > dom_b.name

        dom = dom_a # == dom_b

        # Then compare the number of daggers on the dominant symbol
        num_dags_a = A._num_symbols_like(name=dom.name, behavior=dom.behavior, dag=True)
        num_dags_b = B._num_symbols_like(name=dom.name, behavior=dom.behavior, dag=True)

        if num_dags_a != num_dags_b:
            return num_dags_a < num_dags_b

        # Then compare the "normalness" of both terms according to the dominant symbol
        same_normalness = (not A._more_normal_than(B, dom)) and (not B._more_normal_than(A, dom))
        if not same_normalness:
            return B._more_normal_than(A, dom)

        # Otherwise delete the dominant part and compare the rest
        return A._delete_dominant() < B._delete_dominant()

    def __gt__(A, B):
        return B < A

    def __le__(A, B):
        return not A > B

    def __ge__(A, B):
        return not A < B

    def __ne__(A, B):
        return not A == B

    def __str__(self):
        groups = self._group_symbols()
        str_group = lambda x: str(x[0]) + ("^" + str(x[1]) if x[1] > 1 else "")
        
        return ' '.join(map(str_group, groups))

    def __repr__(self):
        return "Term('{}')".format(str(self))

    def __mul__(A, B):
        if isinstance(B, Term):
            return Term(A.symbols + B.symbols)
        elif isinstance(B, Symbol):
            return Term(A.symbols + [B])
        else:
            return NotImplemented

    def __rmul__(A, B):
        if isinstance(B, Term):
            return Term(B.symbols + A.symbols)
        elif isinstance(B, Symbol):
            return Term([B] + A.symbols)

    def __add__(A, B):
        if isinstance(B, Term):
            return Expression([A, B])
        else:
            return NotImplemented

    def conj(self):
        symbols = [s.conj() for s in reversed(self.symbols)]

        return Term(symbols)

    def is_normal_ordered(self, symbol=None):
        if symbol is not None:
            symbols = [s for s in self.symbols if s.name == symbol.name and s.behavior == symbol.behavior]
            switch = False

            for s in symbols:
                if not switch:
                    switch = not s.dag
                else:
                    if s.dag:
                        break
            else:
                return True

            return False
        else:
            for s in self._symbols_in():
                if not self.is_normal_ordered(symbol=s):
                    break
            else:
                return True

            return False

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

    def _more_normal_than(A, B, sym):
        '''
        Return True if the normal ordering of dagged operators is better respected in A than in B regarding Symbol sym.
        '''
        if sym.behavior != 'annihilation':
            return False

        sym_list_a = [s for s in A.symbols if s == sym or s == sym.conj()]
        sym_list_b = [s for s in B.symbols if s == sym or s == sym.conj()]

        if len(sym_list_a) != len(sym_list_b):
            raise Exception('Compared terms do not have the same order in ' + sym.name + '.')

        n = len(sym_list_a)
        go_on = True
        k = 0

        while go_on and k < n:
            d_a = sym_list_a[k].dag
            d_b = sym_list_b[k].dag

            if d_a and not d_b :
                return True

            go_on = (d_a == d_b)
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
    def __init__(self, info=[], bank=None):
        if bank is None:
            bank = Term._default_bank

        if isinstance(info, str):
            if not info:
                self.__init__()
            else:
                infos = info.split('+')
                terms = [Term(i) for i in infos]
                self.__init__(terms)
        elif isinstance(info, list):
            if not info or all(t == Term('0') for t in info):
                self.terms = [Term('0')] # An empty sum is zero
            else:
                self.terms = sorted(info)[::-1] # Because we want the Terms in decreasing order
                self.terms = [t for t in self.terms if t != Term('0')] # then we remove all occurences of 0
        else:
            raise Exception('Expression constructor argument should be a string or a list of Terms.')

    def __eq__(E, F):
        return E.terms == F.terms

    def __add__(E, F):
        if isinstance(F, Expression):
            return Expression(E.terms + F.terms)
        elif isinstance(F, Symbol):
            return E + Expression([Term([F])])
        elif isinstance(F, Term):
            return E + Expression([F])
        else:
            return NotImplemented

    def __radd__(E, F):
        return E + F

    def __mul__(E, F):
        if isinstance(F, Symbol) or isinstance(F, Term):
            return Expression([t * F for t in E.terms])
        elif isinstance(F, Expression):
            terms = []

            for e in E.terms:
                for t in F.terms:
                    terms.append(e * t)

            return Expression(terms)
        else:
            return NotImplemented

    def __rmul__(E, F):
        if isinstance(F, Symbol) or isinstance(F, Term):
            return Expression([F * t for t in E.terms])
        else:
            return NotImplemented

    def __str__(self):
        return ' + '.join(map(str, self.terms))

    def __repr__(self):
        return "Expression('{}')".format(str(self))

    def conj(self):
        terms = [t.conj() for t in self.terms]

        return Expression(terms)

    def normal_order(self):
        for i, t in enumerate(self.terms):
            if not t.is_normal_ordered():
                # len(t.symbols) >= 2, otherwise t would automatically be normal-ordered
                symbols = t.symbols
                terms = self.terms
                e_before = Expression(terms[:i])
                e_after = Expression(terms[i+1:])

                for j, s in enumerate(symbols):
                    s1 = symbols[j]
                    s2 = symbols[j + 1]
                    if s2.dag and not s1.dag:
                        t_before = Term(symbols[:j])
                        t_after = Term(symbols[j+1:])
                        t_inv = Term([s2, s1])
                        
                        new_part = t_before * Expression([t_inv, Term([ONE])]) * t_after

                        new_expr = e_before + new_part + e_after
                        print('')
                        print('t_before: ' + str(t_before))
                        print('t_after: ' + str(t_after))
                        print('t_inv: ' + str(t_inv))
                        print('new_part: ' + str(new_part))
                        print('new_expr: ' + str(new_expr))
                        
                        self.terms = new_expr.terms
                        break

                break
        return