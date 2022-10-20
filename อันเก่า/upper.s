# load 10,000 into X1
lui    x1, 2
addi   x1,x1, 0x710


addi   x2, x0, 0

# increase X2 by 100 until it is 10,000
addi   x2, x2, 100
blt    x2, x1, -4

# after execution x1,x2 should contain
# 10,000 (0x2710)