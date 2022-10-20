# store 0-9 to RAM locations 1000-10009
addi    x8, x0, 0
addi    x9, x0, 10
sw      x8, 1000(x8)
addi    x8, x8, 1
blt     x8, x9, -8


# copy RAM contents from
# source = address 1000-10009
# destination = address 100-109
addi    x8, x0, 0
lw      x10, 1000(x8)
sw      x10, 100(x8)
addi    x8, x8, 1
blt     x8, x9, -12


