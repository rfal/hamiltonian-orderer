import unittest
from orderer import *

class TestSymbol(unittest.TestCase):
    def test00100_instanciateZero_NameAndBehaviorOK(self):
        # Arrange
        zero = Symbol('0', 'zero')
        
        # Act
        name = zero.name
        behavior = zero.behavior

        # Assert
        self.assertEqual(name, '0')
        self.assertEqual(behavior, 'zero')

    def test00200_instanciateZero_ConjAlwaysFalse(self):
        # Arrange
        zero = Symbol('0', 'zero', True)

        # Act
        dag = zero.dag

        # Assert
        self.assertFalse(dag)

    def test00300_instanciateOne_NameAndBehaviorOK(self):
        # Arrange

        # Act
        one = Symbol('1', 'one')

        name = one.name
        behavior = one.behavior

        # Assert
        self.assertEqual(name, '1')
        self.assertEqual(behavior, 'one')

    def test00400_instanciateOne_ConjAlwaysFalse(self):
        # Arrange
        one = Symbol('1', 'one', True)

        # Act
        dag = one.dag

        # Arrange
        self.assertFalse(dag)

    def test00500_instanciateComplexConjugate_ConjTrue(self):
        # Arrange
        z = Symbol('z', 'complex', True)

        # Act
        dag = z.dag

        # Assert
        self.assertTrue(dag)

    def test00600_instanciateHermitianConjugate_ConjTrue(self):
        # Arrange
        a = Symbol('a', 'annihilation', True)

        # Act
        dag = a.dag

        # Assert
        self.assertTrue(dag)

    def test00700_zeroAndOneInBehaviorList_OK(self):
        # Arrange
        behaviors = Symbol._behaviors

        # Act

        # Assert
        self.assertIn('zero', behaviors)
        self.assertIn('one', behaviors)

    def test00800_instanciateNonExistingBehavior_error(self):
        # Arrange

        # Act

        # Assert
        self.assertRaises(Exception, lambda: Symbol('a', 'ThisBehaviorWillNeverExist'))

    def test00900_instanciateTwoEqualSymbols_equal(self):
        # Arrange
        a1 = Symbol('a', 'annihilation')
        a2 = Symbol('a', 'annihilation')

        # Act

        # Assert
        self.assertEqual(a1, a2)

    def test01000_instancianteTwoDifferentSymbolNames_notEqual(self):
        # Arrange
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        # Act

        # Assert
        self.assertNotEqual(a, b)

    def test01100_instancianteTwoDifferentSymbolBehaviors_notEqual(self):
        # Arrange
        a1 = Symbol('a', 'annihilation')
        a2 = Symbol('a', 'complex')

        # Act

        # Assert
        self.assertNotEqual(a1, a2)

    def test01200_instancianteTwoDifferentSymbolDaggers_notEqual(self):
        # Arrange
        a = Symbol('a', 'annihilation')
        a_dag = Symbol('a', 'annihilation', True)

        # Act

        # Assert
        self.assertNotEqual(a, a_dag)

    def test01210_classAttributeZero_OK(self):
        # Arrange
        zero = Symbol('0', 'zero')

        # Act

        # Assert
        self.assertEqual(ZERO, zero)

    def test01220_classAttributeOne_OK(self):
        # Arrange
        one = Symbol('1', 'one')

        # Act

        # Assert
        self.assertEqual(ONE, one)

    def test01300_conjugateZero_invariant(self):
        # Arrange
        zero = Symbol('0', 'zero')

        # Act
        zero_dag = zero.conj()

        # Assert
        self.assertEqual(zero_dag, zero)

    def test01400_conjugateOne_invariant(self):
        # Arrange
        one = Symbol('1', 'one')

        # Act
        one_dag = one.conj()

        # Assert
        self.assertEqual(one_dag, one)

    def test01500_conjugateReal_invariant(self):
        # Arrange
        x = Symbol('x', 'real')

        # Act
        x_dag = x.conj()

        # Assert
        self.assertEqual(x_dag, x)

    def test01600_conjugateComplex_dagTrue(self):
        # Arrange
        z = Symbol('z', 'complex')

        # Act
        z_dag = z.conj()

        # Assert
        self.assertTrue(z_dag.dag)

    def test01600_conjugateAnnihilation_dagTrue(self):
        # Arrange
        a = Symbol('a', 'annihilation')

        # Act
        a_dag = a.conj()

        # Assert
        self.assertTrue(a_dag.dag)

    def test01700_doubleConjugatComplex_invariant(self):
        # Arrange
        z = Symbol('z', 'complex')

        # Act
        z_dag_dag = z.conj().conj()

        # Assert
        self.assertEqual(z, z_dag_dag)

    def test01800_doubleConjugatAnnihilation_invariant(self):
        # Arrange
        a = Symbol('a', 'annihilation')

        # Act
        a_dag_dag = a.conj().conj()

        # Assert
        self.assertEqual(a, a_dag_dag)

    def test01900_allHermitianBehaviorsInBehaviorList_OK(self):
        # Arrange

        # Act

        # Assert
        for b in Symbol._hermitian_behaviors:
            self.assertIn(b, Symbol._behaviors)

    def test02000_symbolComparisonLessThan_OK(self):
        '''
        The order of symbols is fully determined by this term:
            0 . k^2 . n . xi*^4 . chi^2 . 1 . a*^2 . a . a* . b^2 . b*^7
        '''
        # Arrange
        zero = Symbol('0', 'zero')
        zero_2 = Symbol('00', 'zero')
        one = Symbol('1', 'one')
        one_2 = Symbol('11', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        # Act

        # Assert
        self.assertFalse(zero < zero_2)
        self.assertFalse(one < one_2)
        self.assertTrue(k < n)
        self.assertTrue(xi < zeta)
        self.assertTrue(a < b)

        self.assertTrue(zero < k)
        self.assertTrue(n < xi)
        self.assertTrue(zeta < a)

        self.assertFalse(xi.conj() < xi)
        self.assertFalse(a.conj() < a)

    def test02100_symbolComparisonLessThanEqual_OK(self):
        '''
        The order of symbols is fully determined by this term:
            0 . k^2 . n . xi*^4 . chi^2 . 1 . a*^2 . a . a* . b^2 . b*^7
        '''
        # Arrange
        zero = Symbol('0', 'zero')
        zero_2 = Symbol('00', 'zero')
        one = Symbol('1', 'one')
        one_2 = Symbol('11', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        # Act

        # Assert
        self.assertTrue(zero <= zero_2)
        self.assertTrue(one <= one_2)
        self.assertTrue(k <= n)
        self.assertTrue(xi <= zeta)
        self.assertTrue(a <= b)

        self.assertTrue(zero <= k)
        self.assertTrue(n <= xi)
        self.assertTrue(zeta <= a)

        self.assertTrue(xi.conj() <= xi)
        self.assertTrue(a.conj() <= a)

    def test02200_symbolComparisonGreaterThan_OK(self):
        '''
        The order of symbols is fully determined by this term:
            0 . k^2 . n . xi*^4 . chi^2 . 1 . a*^2 . a . a* . b^2 . b*^7
        '''
        # Arrange
        zero = Symbol('0', 'zero')
        zero_2 = Symbol('00', 'zero')
        one = Symbol('1', 'one')
        one_2 = Symbol('11', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        # Act

        # Assert
        self.assertFalse(zero > zero_2)
        self.assertFalse(one > one_2)
        self.assertTrue(n > k)
        self.assertTrue(zeta > xi)
        self.assertTrue(b > a)

        self.assertTrue(k > zero)
        self.assertTrue(xi > n)
        self.assertTrue(a > zeta)

        self.assertFalse(xi > xi.conj())
        self.assertFalse(a > a.conj())

    def test02200_symbolComparisonGreaterThanEqual_OK(self):
        '''
        The order of symbols is fully determined by this term:
            0 . k^2 . n . xi*^4 . chi^2 . 1 . a*^2 . a . a* . b^2 . b*^7
        '''
        # Arrange
        zero = Symbol('0', 'zero')
        zero_2 = Symbol('00', 'zero')
        one = Symbol('1', 'one')
        one_2 = Symbol('11', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        # Act

        # Assert
        self.assertTrue(zero >= zero_2)
        self.assertTrue(one >= one_2)
        self.assertTrue(n >= k)
        self.assertTrue(zeta >= xi)
        self.assertTrue(b >= a)

        self.assertTrue(k >= zero)
        self.assertTrue(xi >= n)
        self.assertTrue(a >= zeta)

        self.assertTrue(xi >= xi.conj())
        self.assertTrue(a >= a.conj())

    def test02300_notDaggedSymbolStr_Name(self):
        # Arrange
        zero = Symbol('0', 'zero')
        zero_2 = Symbol('00', 'zero')
        one = Symbol('1', 'one')
        one_2 = Symbol('11', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        # Act

        # Assert
        self.assertEqual(str(zero), '0')
        self.assertEqual(str(zero_2), '0')
        self.assertEqual(str(one), '1')
        self.assertEqual(str(one_2), '1')
        self.assertEqual(str(k), 'k')
        self.assertEqual(str(n), 'n')
        self.assertEqual(str(xi), 'xi')
        self.assertEqual(str(zeta), 'zeta')
        self.assertEqual(str(a), 'a')
        self.assertEqual(str(b), 'b')

    def test02400_daggedSymbolStr_Name(self):
        # Arrange
        zero_dag = Symbol('0', 'zero', dag=True)
        zero_2_dag = Symbol('00', 'zero', dag=True)
        one_dag = Symbol('1', 'one', dag=True)
        one_2_dag = Symbol('11', 'one', dag=True)
        k_dag = Symbol('k', 'real', dag=True)
        n_dag = Symbol('n', 'real', dag=True)
        xi_dag = Symbol('xi', 'complex', dag=True)
        zeta_dag = Symbol('zeta', 'complex', dag=True)
        a_dag = Symbol('a', 'annihilation', dag=True)
        b_dag = Symbol('b', 'annihilation', dag=True)

        # Act

        # Assert
        self.assertEqual(str(zero_dag), '0')
        self.assertEqual(str(zero_2_dag), '0')
        self.assertEqual(str(one_dag), '1')
        self.assertEqual(str(one_2_dag), '1')
        self.assertEqual(str(k_dag), 'k')
        self.assertEqual(str(n_dag), 'n')
        self.assertEqual(str(xi_dag), 'xi*')
        self.assertEqual(str(zeta_dag), 'zeta*')
        self.assertEqual(str(a_dag), 'a*')
        self.assertEqual(str(b_dag), 'b*')

class TestTerm(unittest.TestCase):
    def test00100_instanciateZeroTerm_listOK(self):
        # Arrange
        zero = Symbol('0', 'zero')

        # Act
        t = Term([zero])
        t_sym_list = t.symbols

        # Assert
        self.assertEqual(t_sym_list, [zero])

    def test00200_instanciateEmptyTerm_equalsZeroTerm(self):
        # Arrange
        zero = Symbol('0', 'zero')

        # Act
        t = Term([])

        # Assert
        self.assertEqual(t.symbols, [zero])

    def test00300_instanciateOneTerm_listOK(self):
        # Arrange
        one = Symbol('1', 'one')

        # Act
        t = Term([one])

        # Assert
        self.assertEqual(t.symbols, [one])

    def test00400_instanciateOrderedTerm_listOK(self):
        # Arrange
        zero = Symbol('0', 'zero')
        one = Symbol('1', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        symbols = [k, k, n, xi.conj(), xi.conj(), zeta, zeta, zeta, a.conj(), a.conj(), a, a.conj(), b, b, b.conj(), b.conj(), b.conj()]

        # Act
        t = Term(symbols)

        # Assert
        self.assertEqual(t.symbols, symbols)

    def test00500_instanciateNotOrderedTerm_listOK(self):
        # Arrange
        zero = Symbol('0', 'zero')
        one = Symbol('1', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        ordered_symbols = [k, k, n, xi.conj(), xi.conj(), zeta, zeta, zeta, a.conj(), a.conj(), a, a.conj(), b, b, b.conj(), b.conj(), b.conj()]
        symbols = [xi.conj(), zeta, k, zeta, a.conj(), xi.conj(), a.conj(), n, a, a.conj(), b, b, b.conj(), k, b.conj(), b.conj(), zeta]

        # Act
        t = Term(symbols)

        # Assert
        self.assertEqual(t.symbols, ordered_symbols)

    def test00600_instanciateTermWithZero_zeroTerm(self):
        # Arrange
        zero = Symbol('0', 'zero')
        one = Symbol('1', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        symbols = [xi.conj(), zeta, k, zero, zeta, a.conj(), xi.conj(), a.conj(), n, a, a.conj(), b, b, b.conj(), k, b.conj(), b.conj(), zeta]

        # Act
        t = Term(symbols)

        # Assert
        self.assertEqual(t.symbols, [zero])

    def test00700_instanciateTermWithOnes_noOnes(self):
        # Arrange
        zero = Symbol('0', 'zero')
        one = Symbol('1', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        symbols_no_ones = [k, k, n, xi.conj(), xi.conj(), zeta, zeta, zeta, a.conj(), a.conj(), a, a.conj(), b, b, b.conj(), b.conj(), b.conj()]
        symbols = [k, k, one, n, xi.conj(), one, one, xi.conj(), zeta, zeta, zeta, a.conj(), a.conj(), a, one, one, one, one, a.conj(), b, b, b.conj(), one, b.conj(), b.conj(), one, one]

        # Act
        t = Term(symbols)

        # Assert
        self.assertEqual(t.symbols, symbols_no_ones)

    def test00800_termEquality_Equal(self):
        # Arrange
        zero = Symbol('0', 'zero')
        one = Symbol('1', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        ordered_symbols = [k, k, n, xi.conj(), xi.conj(), zeta, zeta, zeta, a.conj(), a.conj(), a, a.conj(), b, b, b.conj(), b.conj(), b.conj()]
        symbols = [xi.conj(), zeta, k, zeta, a.conj(), xi.conj(), a.conj(), n, a, a.conj(), b, b, b.conj(), k, b.conj(), b.conj(), zeta]
        
        t1 = Term(symbols)
        t2 = Term(ordered_symbols)

        # Act

        # Assert
        self.assertEqual(t1, t2)

    def test00900_nonCommutTermEquality_NotEqual(self):
        # Arrange
        a = Symbol('a', 'annihilation')

        t1 = Term([a, a.conj()])
        t2 = Term([a.conj(), a])

        # Act

        # Assert
        self.assertNotEqual(t1, t2)

    def test01000_printTermNoDouble_stringOK(self):
        # Arrange
        zero = Symbol('0', 'zero')
        one = Symbol('1', 'one')
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        symbols = [k, n, xi.conj(), zeta, a.conj(), a, a.conj(), b, b.conj()]
        
        t = Term(symbols)

        # Act
        res = str(t)

        # Assert
        self.assertEqual(res, "k.n.xi*.zeta.a*.a.a*.b.b*")

    def test01100_groupSymbols_listOK(self):
        # Arrange
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        symbols = [k, k, n, xi.conj(), xi.conj(), zeta, zeta, zeta, a.conj(), a.conj(), a, a.conj(), b, b, b.conj(), b.conj(), b.conj()]

        # Act
        t = Term(symbols)
        res = t._group_symbols()

        # Assert
        self.assertEqual(res, [(k, 2), (n, 1), (xi.conj(), 2), (zeta, 3), (a.conj(), 2), (a, 1), (a.conj(), 1), (b, 2), (b.conj(), 3)])

    def test01100_printTermWithDoubles_properPowers(self):
        # Arrange
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        symbols = [k, k, n, xi.conj(), xi.conj(), zeta, zeta, zeta, a.conj(), a.conj(), a, a.conj(), b, b, b.conj(), b.conj(), b.conj()]
        
        t = Term(symbols)

        # Act
        res = str(t)

        # Assert
        self.assertEqual(res, "k^2.n.xi*^2.zeta^3.a*^2.a.a*.b^2.b*^3")

    def test01200_numSymbolsLikeZero_OK(self):
        # Arrange
        t = Term([ZERO])

        # Act
        res_name_zero = t._num_symbols_like(name=ZERO.name)
        res_behavior_zero = t._num_symbols_like(behavior=ZERO.behavior)
        res_dag_zero = t._num_symbols_like(dag=ZERO.dag)
        res_name_one = t._num_symbols_like(name=ONE.name)
        res_behavior_one = t._num_symbols_like(behavior=ONE.behavior)
        res_dag_one = t._num_symbols_like(dag=ONE.dag)

        # Assert
        self.assertEqual(res_name_zero, 1)
        self.assertEqual(res_behavior_zero, 1)
        self.assertEqual(res_dag_zero, 1)
        self.assertEqual(res_name_one, 0)
        self.assertEqual(res_behavior_one, 0)
        self.assertEqual(res_dag_one, 1)

    def test01300_numSymbolsLikeBigTerm_OK(self):
        # Arrange
        k = Symbol('k', 'real')
        n = Symbol('n', 'real')
        xi = Symbol('xi', 'complex')
        zeta = Symbol('zeta', 'complex')
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        symbols = [k, k, n, xi.conj(), xi.conj(), zeta, zeta, zeta, a.conj(), a.conj(), a, a.conj(), b, b, b.conj(), b.conj(), b.conj()]

        t = Term(symbols)

        # Act
        res_name_zero = t._num_symbols_like(name=ZERO.name)
        res_behavior_zero = t._num_symbols_like(behavior=ZERO.behavior)
        res_name_one = t._num_symbols_like(name=ONE.name)
        res_behavior_one = t._num_symbols_like(behavior=ONE.behavior)
        res_name_k = t._num_symbols_like(name='k')
        res_behavior_real = t._num_symbols_like(behavior='real')
        res_name_n = t._num_symbols_like(name='n')
        res_name_xi = t._num_symbols_like(name='xi')
        res_behavior_complex = t._num_symbols_like(behavior='complex')
        res_name_zeta = t._num_symbols_like(name='zeta')
        res_name_a = t._num_symbols_like(name='a')
        res_behavior_annihilation = t._num_symbols_like(behavior='annihilation')
        res_name_b = t._num_symbols_like(name='b')
        res_dag = t._num_symbols_like(dag=True)
        res_all = t._num_symbols_like()

        # Assert
        self.assertEqual(res_name_zero, 0)
        self.assertEqual(res_behavior_zero, 0)
        self.assertEqual(res_name_one, 0)
        self.assertEqual(res_behavior_one, 0)
        self.assertEqual(res_name_k, 2)
        self.assertEqual(res_behavior_real, 3)
        self.assertEqual(res_name_n, 1)
        self.assertEqual(res_name_xi, 2)
        self.assertEqual(res_behavior_complex, 5)
        self.assertEqual(res_name_zeta, 3)
        self.assertEqual(res_name_a, 4)
        self.assertEqual(res_behavior_annihilation, 9)
        self.assertEqual(res_name_b, 5)
        self.assertEqual(res_dag, 8)
        self.assertEqual(res_all, 17)

class TestExpression(unittest.TestCase):
    pass

if __name__ == '__main__':
    print(">>> Testing Symbol class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSymbol)
    unittest.TextTestRunner(verbosity=2).run(suite)

    print("\n======================================================================\n")

    print(">>> Testing Term class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTerm)
    unittest.TextTestRunner(verbosity=2).run(suite)

    print("\n======================================================================\n")
    
    print(">>> Testing Expression class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExpression)
    unittest.TextTestRunner(verbosity=2).run(suite)