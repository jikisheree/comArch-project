# Simple Multiply and Divide 
# ==========================
#
# This code performs (a*b)+(c/d)
# Register usage:
# - s0 = result
# - a0, a1 = parameter a,b for mul and c,d for div respectively
# - a0 = also serves as return value
# - t0,t1 = temporary variables used inside mul,div
#
# Psuedo code 
# ===========
#
# result = multiply ( 3, 2 ) 
# result = result + divide ( 8, 2 ) 
#
# multiply (a, b) {
#  answer = a
#  while (1<b) {
#   answer = answer + a
#   b = b-1
#  }
#  return(answer)
# }
#
# divide (a, b) {
#  answer = 0
#  while (b < a) {
#   a = a - b
#   answer = answer + 1
#  }
#  if (a == b) {
#   answer = answer + 1
#  }
#  return(answer)
# }

addi s0, zero, 0    # result = 0
addi a0, zero,4     # prameter a of mul()
addi a1, zero,3    # parameter b of muil()
jal ra, MUL        # call mul()
add s0, zero, a0     # put return value in result (s0)

addi a0, zero, 8    # parameter c for div()
addi a1, zero, 2    # parameter d for div()
jal ra, DIV        # call div()
add s0, s0, a0    # add result with return value in a0
jal zero, END      # end program

MUL:
    addi t0, zero,1    # t0 = 1
    add t1, zero, a0    # t1 = a0
    blt t0,a1, 12    # branch if t0 > a1
    add  a0, zero, t1  # a0 = t1
    jalr zero, ra, 0    # return
    add t1, t1, a0    # t1 = t1 + a0
    addi a1, a1, -1    # a1 = a1 - 1
    jal zero, -20     # loop 

DIV:
    addi t0,zero ,0    # t0 = 0
    blt a1, a0, 8      # branch if a1 < a0
    jal zero, 16       # jump
    sub a0, a0, a1     # a0 = a0 - a1
    addi t0, t0, 1     # t0 = t0 + 1
    jal zero, -16      # loop
    bne a0, a1, 8      # branch if a0 <> a1
    addi t0, t0, 1     # t0 = t0 + 1
    add a0, zero,t0    # a0 = t0
    jalr zero, ra,0    # return

END:
    addi    zero, zero, 0     # just a place holder
