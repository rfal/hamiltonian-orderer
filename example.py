from orderer import *

e = Expression('a a* a a*^2 a')

print(e.normal_order())