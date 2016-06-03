from orderer import *

e = Expression('a a* a a*^2 a')

e.normal_order()

print(e)