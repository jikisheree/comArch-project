lines = []

# read file of machine code then append each instruction in arr
with open('code.txt', 'r') as fp:
    read = fp.readlines()
for i in range(0, len(read)):
    lines.append(read[i].rstrip('\n'))

mem = lines
pc = 0
reg = [0, 0, 0, 0, 0, 0, 0, 0]
ex_num = 0


# อ่าน opcode
def add_op(rs, rt, rd):
    global pc
    result = reg[rs] + reg[rt]
    reg[rd] = result
    pc += 1
    print('add -pc-: ', pc)


def nand_op(rs, rt, rd):
    global pc
    result = ~(reg[rs] & reg[rt])
    reg[rd] = result
    pc += 1
    print('nand -pc-: ', pc)


def lw_op(rs, rt, offset):
    global pc
    reg[rt] = mem[reg[rs] + offset]
    pc += 1
    print('lw -pc-: ', pc)


def sw_op(rs, rt, offset):
    global pc
    line = reg[rt]
    mem[reg[rs] + offset] = str(line)
    pc += 1
    print('sw -pc-: ', pc)


def beq_op(rs, rt, offset):
    global pc
    if reg[rs] == reg[rt]:
        pc += (offset + 1)
    else:
        pc += 1
    print('offset: ', offset)
    print('b -pc-: ', pc)


def jalr_op(rs, rt):
    global pc
    jump = reg[rs]

    reg[rt] = pc + 1
    pc += jump
    print('j -pc-: ', pc)


def halt_op():
    global pc
    pc += 1
    print('h -pc-: ', pc)


def printState():
    print('@@@\nState: \n\tpc ', pc, '\tmemory:')
    for k in range(0, len(mem)):
        print('\n\t\tmem[ ', k, ' ] ', mem[k])
    print('\nregisters:')
    for j in range(0, len(reg)):
        print('\n\t\treg[ ', j, ' ] ', reg[j])
    print('\nend state\n')


def print_halted():
    print('machine halted\ntotal of ', ex_num, ' instructions executed')
    print('final state of machine: ')
    printState()


def convert_32bit(n):
    if n > 0xFFFFFFFF:
        raise OverflowError
    elif n > 0x7FFFFFFFF:
        n = int(0x100000000 - n)
        if n < 2147483648:
            return -n
        else:
            return -2147483648
    return n


while True:

    printState()
    current = int(mem[pc])
    opcode = (current >> 21) & 0b0111

    # select 2 MSB of opcode

    # R-type
    if ((opcode & 0b110) >> 1) == 0:
        # set bit 15-3 to 0 (not used)
        inst = current & 0b10000000000000111
        # select rs, rt, rd
        rs = (inst >> 18) & 0b0111
        rt = (inst >> 15) & 0b0111
        rd = inst & 0b0111
        # select bit 0 of opcode
        if (opcode & 0b01) == 0:  # and
            add_op(rs, rt, rd)
        else:  # nand
            nand_op(rs, rt, rd)

    # I-type
    elif (((opcode & 0b110) >> 1) == 1) | (opcode == 0b100):
        # set nothing
        inst = current
        # select rs, rt, rd
        rs = (inst >> 18) & 0b0111
        rt = (inst >> 15) & 0b0111
        # select bit 15-0 to offset
        offset = inst & 0b01111111111111111
        offset = convert_32bit(offset)
        # lw or sw
        if ((opcode & 0b110) >> 1) == 1:
            # select bit 0 of opcode
            if (opcode & 0b011) == 0:  # lw
                lw_op(rs, rt, offset)
            else:  # sw
                sw_op(rs, rt, offset)
                # beq
        else:
            beq_op(rs, rt, offset)

    # J-type
    elif opcode == 0b101:
        # set bit 15-0 to 0 (not used)
        inst = current & 0b10000000000000000
        # select rs, rt, rd
        rs = (inst >> 18) & 0b0111
        rt = (inst >> 15) & 0b0111
        # jalr
        jalr_op(rs, rt)

    # O-type
    elif (opcode & 0b110) >> 1 == 3:
        # set bit 21-0 to 0 (not used)
        inst = current & 0b10000000000000000000000
        # select bit 0 of opcode
        if (opcode & 0b01) == 0:  # halt
            halt_op()
            print_halted()
            break
        else:  # noop
            continue
    ex_num += 1