import unittest
from time import sleep
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

    def test00810_instanciateSymbolWithSpaceInName_error(self):
        # Arrange

        # Act

        # Assert
        self.assertRaises(Exception, lambda: Symbol('a e', 'annihilation'))

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

        self.assertTrue(xi.conj() < xi)
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

        self.assertTrue(xi > xi.conj())
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

    def test02500_mulSymbols_TermOK(self):
        # Arrange
        a = Symbol('a', 'annihilation')
        b = Symbol('b', 'annihilation')

        # Act
        res = a * b

        # Assert
        self.assertEqual(res, Term([a, b]))

class TestTerm(unittest.TestCase):
    def setUp(self):
        self.k = Symbol('k', 'real')
        self.n = Symbol('n', 'real')
        self.x = Symbol('x', 'real')
        self.xi = Symbol('xi', 'complex')
        self.zeta = Symbol('zeta', 'complex')
        self.z = Symbol('z', 'complex')
        self.a = Symbol('a', 'annihilation')
        self.b = Symbol('b', 'annihilation')

        self.bank = [self.k, self.n, self.x, self.xi, self.zeta, self.z, self.a, self.b]

    def test00100_instanciateZeroTerm_listOK(self):
        # Arrange

        # Act
        t = Term([ZERO])

        t_sym_list = t.symbols

        # Assert
        self.assertEqual(t_sym_list, [ZERO])

    def test00200_instanciateEmptyTerm_equalsZeroTerm(self):
        # Arrange

        # Act
        t = Term([])

        # Assert
        self.assertEqual(t.symbols, [ZERO])

    def test00300_instanciateOneTerm_listOK(self):
        # Arrange

        # Act
        t = Term([ONE])

        # Assert
        self.assertEqual(t.symbols, [ONE])

    def test00400_instanciateOrderedTerm_listOK(self):
        # Arrange
        symbols = [self.k, self.k, self.n, self.xi.conj(), self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.b.conj(), self.b.conj()]

        # Act
        t = Term(symbols)

        # Assert
        self.assertEqual(t.symbols, symbols)

    def test00500_instanciateNotOrderedTerm_listOK(self):
        # Arrange
        ordered_symbols = [self.k, self.k, self.n, self.xi.conj(), self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.b.conj(), self.b.conj()]
        symbols = [self.xi.conj(), self.zeta, self.k, self.zeta, self.a.conj(), self.xi.conj(), self.a.conj(), self.n, self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.k, self.b.conj(), self.b.conj(), self.zeta]

        # Act
        t = Term(symbols)

        # Assert
        self.assertEqual(t.symbols, ordered_symbols)

    def test00600_instanciateTermWithZero_zeroTerm(self):
        # Arrange
        symbols = [self.xi.conj(), self.zeta, self.k, ZERO, self.zeta, self.a.conj(), self.xi.conj(), self.a.conj(), self.n, self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.k, self.b.conj(), self.b.conj(), self.zeta]

        # Act
        t = Term(symbols)

        # Assert
        self.assertEqual(t.symbols, [ZERO])

    def test00700_instanciateTermWithOnes_noOnes(self):
        # Arrange
        symbols_no_ones = [self.k, self.k, self.n, self.xi.conj(), self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.b.conj(), self.b.conj()]
        symbols = [self.k, self.k, ONE, self.n, self.xi.conj(), ONE, ONE, self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, ONE, ONE, ONE, ONE, self.a.conj(), self.b, self.b, self.b.conj(), ONE, self.b.conj(), self.b.conj(), ONE, ONE]

        # Act
        t = Term(symbols)

        # Assert
        self.assertEqual(t.symbols, symbols_no_ones)

    def test00800_termEquality_Equal(self):
        # Arrange
        ordered_symbols = [self.k, self.k, self.n, self.xi.conj(), self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.b.conj(), self.b.conj()]
        symbols = [self.xi.conj(), self.zeta, self.k, self.zeta, self.a.conj(), self.xi.conj(), self.a.conj(), self.n, self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.k, self.b.conj(), self.b.conj(), self.zeta]
        
        t1 = Term(symbols)
        t2 = Term(ordered_symbols)

        # Act

        # Assert
        self.assertEqual(t1, t2)

    def test00900_nonCommutTermEquality_NotEqual(self):
        # Arrange
        t1 = Term([self.a, self.a.conj()])
        t2 = Term([self.a.conj(), self.a])

        # Act

        # Assert
        self.assertNotEqual(t1, t2)

    def test01000_printTermNoDouble_stringOK(self):
        # Arrange
        symbols = [self.k, self.n, self.xi.conj(), self.zeta, self.a.conj(), self.a, self.a.conj(), self.b, self.b.conj()]
        
        t = Term(symbols)

        # Act
        res = str(t)

        # Assert
        self.assertEqual(res, "k n xi* zeta a* a a* b b*")

    def test01100_groupSymbols_listOK(self):
        # Arrange
        symbols = [self.k, self.k, self.n, self.xi.conj(), self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.b.conj(), self.b.conj()]

        # Act
        t = Term(symbols)
        res = t._group_symbols()

        # Assert
        self.assertEqual(res, [(self.k, 2), (self.n, 1), (self.xi.conj(), 2), (self.zeta, 3), (self.a.conj(), 2), (self.a, 1), (self.a.conj(), 1), (self.b, 2), (self.b.conj(), 3)])

    def test01100_printTermWithDoubles_properPowers(self):
        # Arrange
        symbols = [self.k, self.k, self.n, self.xi.conj(), self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.b.conj(), self.b.conj()]
        
        t = Term(symbols)

        # Act
        res = str(t)

        # Assert
        self.assertEqual(res, "k^2 n xi*^2 zeta^3 a*^2 a a* b^2 b*^3")

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
        symbols = [self.k, self.k, self.n, self.xi.conj(), self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.b.conj(), self.b.conj()]

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

    def test01400_symbolsInTerm_OK(self):
        # Arrange
        symbols = [self.xi.conj(), self.zeta, self.k, self.zeta, self.a.conj(), self.xi.conj(), self.a.conj(), self.n, self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.k, self.b.conj(), self.b.conj(), self.zeta]

        t = Term(symbols)

        # Act
        res = t._symbols_in()

        # Assert
        self.assertEqual(res, [self.k, self.n, self.xi, self.zeta, self.a, self.b])

    def test01500_termsOrderLessThanZeroOneOneSymbol_True(self):
        # Arrange
        t1 = Term([ZERO])
        t2 = Term([ONE])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test01600_termsOrderLessThanOneZeroOneSymbol_False(self):
        # Arrange
        t1 = Term([ZERO])
        t2 = Term([ONE])

        # Act

        # Assert
        self.assertFalse(t2 < t1)

    def test01700_termsOrderLessThanOneRealOneSymbol_True(self):
        # Arrange
        t1 = Term([ONE])
        t2 = Term([self.x])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test01800_termsOrderLessThanRealComplexOneSymbol_True(self):
        # Arrange
        t1 = Term([self.x])
        t2 = Term([self.z])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test01900_termsOrderLessThanComplexAnnihilationOneSymbol_True(self):
        # Arrange
        t1 = Term([self.z])
        t2 = Term([self.a])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test02000_testOrderLTAnnihilatorsOneSymbol_True(self):
        # Arrange
        t1 = Term([self.b])
        t2 = Term([self.a])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test02010_testOrderLTAnnihilatorsDifferentTotalDegree_True(self):
        # Arrange
        t1 = Term([self.a, self.b, self.b])
        t2 = Term([self.a, self.b])

        # Act

        # Assert
        self.assertTrue(t2 < t1)

    def test02020_testOrderLTAnnihilatorsComplexDifferentTotalDegree_True(self):
        # Arrange
        t1 = Term([self.a, self.xi, self.xi.conj()])
        t2 = Term([self.a, self.xi])

        # Act

        # Assert
        self.assertTrue(t2 < t1)

    def test02100_testDominantSymbol_OK(self):
        # Arrange
        symbols = [self.xi.conj(), self.zeta, self.k, self.zeta, self.a.conj(), self.xi.conj(), self.a.conj(), self.n, self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.k, self.b.conj(), self.b.conj(), self.zeta]

        t = Term(symbols)

        # Act
        res = t._dominant()

        # Assert
        self.assertEqual(res, self.a)


    def test02200_termsOrderLTAnnihilatorsTwoSymbols_True(self):
        # Arrange
        t1 = Term([self.a])
        t2 = Term([self.x, self.a, self.a])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test02300_termsOrderLTAnnihilatorsTwoSymbolsConj_True(self):
        # Arrange
        t1 = Term([self.a.conj(), self.a])
        t2 = Term([self.a.conj(), self.a.conj()])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test02400_moreNormalThan_OK(self):
        # Arrange
        t1 = Term([self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj()])
        t2 = Term([self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a.conj(), self.a])

        # Act
        res21 = t2._more_normal_than(t1, self.a)
        res12 = t1._more_normal_than(t2, self.a)
        res11 = t1._more_normal_than(t1, self.a)

        # Assert
        self.assertTrue(res21)
        self.assertFalse(res12)
        self.assertFalse(res11)

    def test02500_moreNormalThanDifferentLengths_error(self):
        # Arrange
        t1 = Term([self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj()])
        t2 = Term([self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a.conj(), self.a, self.a])

        # Act

        # Assert
        self.assertRaises(Exception, lambda: t1._more_normal_than(t2, self.a))

    def test02600_termsOrderLTAnnihilNormalOrder_True(self):
        # Arrange
        t1 = Term([self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj()])
        t2 = Term([self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a.conj(), self.a])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test02700_deleteDominant_OK(self):
        # Arrange
        t = Term([self.k, self.n, self.n, self.xi, self.a.conj(), self.a, self.a.conj(), self.a, self.a, self.b, self.b])

        # Act
        res = t._delete_dominant()

        # Assert
        self.assertEqual(res, Term([self.k, self.n, self.n, self.xi, self.b, self.b]))

    def test02800_termsOrderLTAnnihilSecondDepth_True(self):
        # Arrange
        t1 = Term([self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])
        t2 = Term([self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b.conj(), self.b])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test02800_termsOrderLTAnnihilThirdDepth_True(self):
        # Arrange
        t1 = Term([self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])
        t2 = Term([self.xi.conj(), self.xi.conj(), self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])


        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test02900_termsOrderLTAnnihilForthDepth_True(self):
        # Arrange
        t1 = Term([self.n, self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])
        t2 = Term([self.n, self.n, self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test03000_termsOrderLTAnnihilForthDepthComplexDisordered_True(self):
        # Arrange
        t1 = Term([self.n, self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])
        t2 = Term([self.n, self.n, self.xi, self.xi.conj(), self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])

        # Act

        # Assert
        self.assertTrue(t1 < t2)

    def test03100_termsOrderLTEqualTerms_False(self):
        # Arrange
        t1 = Term([self.n, self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])

        # Act

        # Assert
        self.assertFalse(t1 < t1)

    def test03200_termsOrderLTE_True(self):
        # Arrange
        t1 = Term([self.n, self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])
        t2 = Term([self.n, self.n, self.xi, self.xi.conj(), self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])

        # Act

        # Assert
        self.assertTrue(t1 <= t2)
        self.assertTrue(t1 <= t1)

    def test03300_termsOrderGTAnnihilForthDepthComplexDisordered_True(self):
        # Arrange
        t1 = Term([self.n, self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])
        t2 = Term([self.n, self.n, self.xi, self.xi.conj(), self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])

        # Act

        # Assert
        self.assertTrue(t2 > t1)

    def test03400_termsOrderGTEqualTerms_False(self):
        # Arrange
        t1 = Term([self.n, self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])

        # Act

        # Assert
        self.assertFalse(t1 > t1)

    def test03500_termsOrderGTE_True(self):
        # Arrange
        t1 = Term([self.n, self.xi.conj(), self.xi, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])
        t2 = Term([self.n, self.n, self.xi, self.xi.conj(), self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.a, self.a.conj(), self.b, self.b])

        # Act

        # Assert
        self.assertTrue(t2 >= t1)
        self.assertTrue(t1 >= t1)

    def test03600_termConstructorWrongIdType_error(self):
        # Arrange
        info = 24

        # Act

        # Assert
        self.assertRaises(Exception, lambda: Term(info))

    def test03700_stringToTermOneSymbolZero_OK(self):
        # Arrange
        bank = []
        info = '0'

        # Act
        res = Term(info)
        expected_res = Term([ZERO])

        # Assert
        self.assertEqual(res, expected_res)

    def test03800_stringToTermOneSymbolOne_OK(self):
        # Arrange
        bank = []
        info = '1'

        # Act
        res = Term(info)
        expected_res = Term([ONE])

        # Assert
        self.assertEqual(res, expected_res)

    def test03900_stringToTermOneSymbolAnnihilator_OK(self):
        # Arrange
        bank = [self.a]
        info = 'a'

        # Act
        res = Term(info, bank)
        expected_res = Term([self.a])

        # Assert
        self.assertEqual(res, expected_res)

    def test04000_stringToTermAmbiguousBank_error(self):
        # Arrange
        bank = [self.a, self.a]
        info = 'a'

        # Act

        # Assert
        self.assertRaises(Exception, lambda: Term(info, bank))

    def test04100_stringToTermTwoSymbolsAnnihilator_OK(self):
        # Arrange
        bank = [self.a]
        info = 'a a'

        # Act
        res = Term(info, bank)
        expected_res = Term([self.a, self.a])

        # Assert
        self.assertEqual(res, expected_res)

    def test04200_stringToTermSymbolNotInBank_error(self):
        # Arrange
        bank = [self.a]
        info = 'b'

        # Act

        # Assert
        self.assertRaises(Exception, lambda: Term(info, bank))

    def test04300_stringToTermSquaredSymbol_OK(self):
        # Arrange
        info = 'a^2'

        # Act
        res = Term(info, self.bank)
        expected_res = Term([self.a, self.a])

        # Assert
        self.assertEqual(res, expected_res)

    def test04400_stringToTermDaggedSymbol_OK(self):
        # Arrange
        info = 'a*'

        # Act
        res = Term(info, self.bank)
        expected_res = Term([self.a.conj()])

        # Assert
        self.assertEqual(res, expected_res)

    def test04500_stringToTermAllAtOnce_OK(self):
        # Arrange
        symbols = [self.k, self.k, self.n, self.xi.conj(), self.xi.conj(), self.zeta, self.zeta, self.zeta, self.a.conj(), self.a.conj(), self.a, self.a.conj(), self.b, self.b, self.b.conj(), self.b.conj(), self.b.conj()]

        t = Term(symbols)
        t_str = 'k^2 n xi*^2 zeta^3 a*^2 a a* b^2 b*^3'

        # Act
        res = Term(t_str, self.bank)

        # Assert
        self.assertEqual(res, t)

    def test04600_mulTerms_OK(self):
        # Arrange
        t1 = Term([self.k, self.xi, self.a.conj(), self.a, self.b.conj(), self.b.conj()])
        t2 = Term([self.n, self.n, self.xi.conj(), self.zeta, self.a.conj(), self.a, self.b, self.b.conj()])

        # Act
        res = t1 * t2
        expected_res = Term([self.k, self.n, self.n, self.xi.conj(), self.xi, self.zeta, self.a.conj(), self.a, self.a.conj(), self.a, self.b.conj(), self.b.conj(), self.b, self.b.conj()])

        # Assert
        self.assertEqual(res, expected_res)

    def test04700_mulTermSymbol_TermOK(self):
        # Arrange
        t = Term([self.a])

        # Act
        res = t * self.b

        # Assert
        self.assertEqual(res, Term([self.a, self.b]))

    def test04800_mulSymbolTerm_TermOK(self):
        # Arrange
        t = Term([self.a])

        # Act
        res = self.b * t

        # Assert
        self.assertEqual(res, Term([self.b, self.a]))

class TestExpression(unittest.TestCase):
    def setUp(self):
        self.k = Symbol('k', 'real')
        self.n = Symbol('n', 'real')
        self.x = Symbol('x', 'real')
        self.xi = Symbol('xi', 'complex')
        self.zeta = Symbol('zeta', 'complex')
        self.z = Symbol('z', 'complex')
        self.a = Symbol('a', 'annihilation')
        self.b = Symbol('b', 'annihilation')

        self.bank = [self.k, self.n, self.x, self.xi, self.zeta, self.z, self.a, self.b]

    def test00100_instanciateExpressionEmptyList_attrZero(self):
        # Arrange

        # Act
        e = Expression([])

        # Assert
        self.assertEqual(e.terms, [Term()])

    def test00200_instanciateExpressionTwoTerms_attrOK(self):
        # Arrange
        t1 = Term('1')

        # Act
        e = Expression([t1, t1])

        # Assert
        self.assertEqual(e.terms, [t1, t1])

    def test00300_instanciateExpressionTwoDisorderedTerms_attrOK(self):
        # Arrange
        t1 = Term('1')
        t2 = Term('a* a')

        # Act
        e1 = Expression([t1, t2])
        e2 = Expression([t2, t1])

        # Assert
        self.assertEqual(e1.terms, [t2, t1])
        self.assertEqual(e2.terms, [t2, t1])

    def test00400_instanciateExpressionWithZero_zero(self):
        # Arrange
        t1 = Term('1')
        t2 = Term('a* a')
        t3 = Term()

        # Act
        e = Expression([t1, t2, t1, t3, t2, t2])

        # Assert
        self.assertEqual(e.terms, [Term()])

    def test00500_exprEquality_OK(self):
        # Arrange
        e1 = Expression([Term('1'), Term('a* a')])
        e2 = Expression([Term('1'), Term('a* a')])
        e3 = Expression([Term('b'), Term('a* a')])

        # Act

        # Assert
        self.assertEqual(e1, e2)
        self.assertNotEqual(e1, e3)

    def test00600_addExprExpr_OK(self):
        # Arrange
        e1 = Expression([Term('1'), Term('a* a')])
        e2 = Expression([Term('b')])

        # Act
        e3 = e1 + e2

        # Assert
        self.assertEqual(e3, Expression([Term('1'), Term('a* a'), Term('b')]))

    def test00700_addExprSymbol_OK(self):
        # Arrange
        e = Expression([Term('1'), Term('a* a'), Term('b')])

        # Act
        res = e + self.b

        # Assert
        self.assertEqual(res, Expression([Term('1'), Term('a* a'), Term('b'), Term('b')]))

    def test00800_addSymbolExpr_OK(self):
        # Arrange
        e = Expression([Term('1'), Term('a* a'), Term('b')])

        # Act
        res = self.b + e

        # Assert
        self.assertEqual(res, Expression([Term('1'), Term('a* a'), Term('b'), Term('b')]))

    def test00700_addExprTerm_OK(self):
        # Arrange
        e = Expression([Term('1'), Term('a* a'), Term('b')])

        # Act
        res = e + Term('b* b a')

        # Assert
        self.assertEqual(res, Expression([Term('1'), Term('a* a'), Term('b'), Term('b* b a')]))

    def test00800_addTermExpr_OK(self):
        # Arrange
        e = Expression([Term('1'), Term('a* a'), Term('b')])

        # Act
        res = Term('b* b a') + e

        # Assert
        self.assertEqual(res, Expression([Term('1'), Term('a* a'), Term('b'), Term('b* b a')]))

if __name__ == '__main__':
    print(">>> Testing Symbol class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSymbol)
    unittest.TextTestRunner().run(suite)

    sleep(0.3)

    print("\n>>> Testing Term class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTerm)
    unittest.TextTestRunner().run(suite)

    sleep(0.3)
    
    print("\n>>> Testing Expression class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExpression)
    unittest.TextTestRunner().run(suite)