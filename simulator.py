# Simulator
# read file of machine code then append each instruction in arr
lines = []

# open file then read file
file_path = 'machine_code/4.txt'
with open(file_path, 'r') as fp:
    read = fp.readlines()
# append each line (instruction) into array
for i in range(0, len(read)):
    lines.append(read[i].rstrip('\n'))

# print memory
for i in range(0, len(read)):
    print("memory[" + str(i) + "]=" + str(lines[i]))
print('\n\n')

# declaring global variables

# var to store current pc
pc = 0
# array to store register
reg = [0, 0, 0, 0, 0, 0, 0, 0]
# var to count total number of execution
ex_num = 0
# boolean foe checking if program is halted or not
ifRunning = True
# array to store memory
mem = [0] * 65536
# var to keep total number of memories
code_num = 0
# store each initializing memory into 'mem' array
for line in lines:
    mem[code_num] = str(line)
    code_num += 1


# function of operation of each instruction
# add operation
def add_op(rs, rt, rd):
    global pc
    # if address of destination register is 0 then we won't overwrite it
    # (register 0 has to always bo zero)
    if rd == 0:
        return
    else:
        # add value from rs and rt together
        # then keep the result at register rd
        result = (reg[rs] + reg[rt])
        reg[rd] = result
        # count pc to next memory
        pc += 1


# nand operation
def nand_op(rs, rt, rd):
    global pc
    # if address of destination register is 0 then we won't overwrite it
    # (register 0 has to always bo zero)
    if rd == 0:
        return
    else:
        # 'nand' value from rs and rt together
        # then keep the result at register rd
        result = ~(reg[rs] & reg[rt])
        reg[rd] = result
        # count pc to next memory
        pc += 1


# load word operation
def lw_op(rs, rt, offset):
    global pc
    # if address of second register is 0 then we won't overwrite it
    # (register 0 has to always bo zero)
    if rt == 0:
        return
    else:
        # load value from memory address of 'value from rs add with offset'
        reg[rt] = int(mem[reg[rs] + offset])
        # count pc to next memory
        pc += 1


# store word operation
def sw_op(rs, rt, offset):
    global pc
    # store value from register rt to memory address of 'value from rs add with offset'
    mem[reg[rs] + offset] = str(reg[rt])
    # count pc to next memory
    pc += 1


# beq operation
def beq_op(rs, rt, offset):
    global pc
    # if value from register rs is equal to value from rt
    if reg[rs] == reg[rt]:
        # count pc to memory of 'offset + 1'
        pc += (offset + 1)
    # else
    else:
        # count pc to next memory
        pc += 1


# jalr operation
def jalr_op(rs, rt):
    global pc
    # if rs is equal to rt then do nothing
    if rs == rt:
        # count pc to next memory
        pc += 1
        return
    # if rt is not 0 (if it is 0 we won't overwrite it)
    if rt != 0:
        # store value of 'current pc + 1' to register rt
        reg[rt] = pc + 1
    # pc jump to address that stored in rs
    pc = reg[rs]


# halt operation
def halt_op():
    # do nothing and just count pc to next address
    global pc
    pc += 1


# sign extend
def sign_extend(num: int):
    if num & (1 << 15):
        num -= (1 << 16)
    return num


# overflow
def check_overflow(n):
    # print('n',bin(n))
    if n > 0xFFFFFFFF:
        raise OverflowError
    elif n > 0x7FFFFFFFF:
        n = int(0x100000000 - n)
        if n < 2147483648:
            return -n
        else:
            return -2147483648
    else:
        return n


# print machine state
def printState():
    print('@@@')
    print('state:')
    print('\tpc', pc)
    print('\n\tmemory:')
    for k in range(0, code_num):
        print('\t\tmem[', k, ']', mem[k])
    print('\n\tregisters:')
    for j in range(0, len(reg)):
        print('\t\treg[', j, ']', reg[j])
    print('\nend state\n')


# print state when halted and show total number of execution
def print_halted():
    print('machine halted\ntotal of ', ex_num, ' instructions executed')
    print('final state of machine: ')
    printState()


# while program is not halted
while ifRunning:

    # print current machine state
    printState()
    # load current instruction depending on current pc count
    machine_code = int(mem[pc])
    # select opcode bits
    opcode = (machine_code >> 22) & 0b0111

    # R-type
    # if 2 MSB of opcode is equal to 0
    if ((opcode & 0b110) >> 1) == 0:
        # set bit 15-3 of machine code to 0 (not used)
        # select only bit 21-0
        inst = machine_code & 0b1111110000000000000111
        # select rs, rt, rd
        rs = (inst >> 19) & 0b0111                                         # bit 21-19
        rt = (inst >> 16) & 0b0111                                         # bit 18-16
        rd = inst & 0b0111                                                 # bit 2-0
        # select bit 0 of opcode
        # if bit 0 of opcode is 0 -> add operation
        if (opcode & 0b01) == 0:                                           # add
            add_op(rs, rt, rd)
        # else -> nand operation
        else:                                                              # nand
            nand_op(rs, rt, rd)

    # I-type
    # if 2 MSB of opcode is equal to 1 (or 0b01) or opcode is 0b100
    elif (((opcode & 0b110) >> 1) == 1) | (opcode == 0b100):
        # select only bit 21-0
        inst = machine_code & 0b1111111111111111111111
        # select rs, rt, rd
        rs = (inst >> 19) & 0b0111                                          # bit 21-19
        rt = (inst >> 16) & 0b0111                                          # bit 18-16
        offset = sign_extend(inst & 0b1111111111111111)                     # bit 15-0
        # convert to 32 bits
        offset = check_overflow(offset)

        # lw or sw
        # if 2 MSB of opcode is equal to 1 (or 0b01) -> lw operation
        if ((opcode & 0b110) >> 1) == 1:
            # select bit 1-0 of opcode
            # if it is equal to 1 -> lw operation
            if (opcode & 0b011) == 2:
                lw_op(rs, rt, offset)
            # else -> sw operation
            else:
                sw_op(rs, rt, offset)
        # else -> beq operation
        else:
            beq_op(rs, rt, offset)

    # J-type
    # if opcode is equal to 0b101
    elif opcode == 0b101:
        # set bit 15-0 to 0 (not used) and select only bit 21-0
        inst = machine_code & 0b1111110000000000000000
        # select rs, rt, rd
        rs = (inst >> 19) & 0b0111                                          # bit 21-19
        rt = (inst >> 16) & 0b0111                                          # bit 18-16
        # call only jalr operation
        jalr_op(rs, rt)

    # O-type
    # if 2 MSB of opcode is equal to 3 (or 0b11)
    elif (opcode & 0b110) >> 1 == 3:
        # select bit 0 of opcode
        # if bit 0 of opcode is 0 then halt
        if (opcode & 0b01) == 0:  # halt
            halt_op()
            # set ifRunning to false
            ifRunning = False

    # count number of current execution
    ex_num += 1

# when exit while loop then program is halted -> print halt state
print_halted()
