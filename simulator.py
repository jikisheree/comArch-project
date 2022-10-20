lines = []

# read file of machine code then append each instruction in arr
with open('code1.txt', 'r') as fp:
    read = fp.readlines()
for i in range(0, len(read)):
    lines.append(read[i].rstrip('\n'))

for i in range(0, len(read)):
    print("memory["+str(i)+"]="+str(lines[i]))

print('\n\n')

mem = [0]*65536
code_num=0
for line in lines:
    mem[code_num] = line
    code_num+=1

pc = 0
reg = [0, 0, 0, 0, 0, 0, 0, 0]
ex_num = 0

ifRunning = True


# อ่าน opcode
def add_op(rs, rt, rd):
    global pc
    if rd == 0:
        return
    else:
        result = (reg[rs] + reg[rt])
        # print(reg)
        # print(rs,rt)
        # print(reg[rs] , reg[rt])
        reg[rd] = result
        pc += 1
        # print('add -pc-: ', pc)


def nand_op(rs, rt, rd):
    global pc
    if rd == 0:
        return
    else:
        result = ~(reg[rs] & reg[rt])
        reg[rd] = result
        pc += 1
        # print('nand -pc-: ', pc)


def lw_op(rs, rt, offset):
    global pc
    if rt == 0:
        return
    else:
        reg[rt] = int(mem[reg[rs] + offset])
        # print('gg', reg[rt])
        pc += 1
        # print('lw -pc-: ', pc)


def sw_op(rs, rt, offset):
    global pc
    line = reg[rt]
    print('sw offset:', offset)
    print('reg[rs]:', reg[rs])
    index = reg[rs] + offset
    mem[reg[rs] + offset] = str(line)
    pc += 1
    # print('sw -pc-: ', pc)


def beq_op(rs, rt, offset):
    global pc
    if reg[rs] == reg[rt]:
        pc += (offset + 1)
    else:
        pc += 1
    # print('offset: ', offset)
    # print('b -pc-: ', pc)


def jalr_op(rs, rt):
    global pc
    if rs == rt:
        pc += 1
        return
    if rt != 0:
        reg[rt] = pc + 2
    pc = reg[rs]
  
    # print('j -pc-: ', pc)


def halt_op():
    global pc
    pc += 1
    # print('h -pc-: ', pc)


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


def print_halted():
    print('machine halted\ntotal of ', ex_num, ' instructions executed')
    print('final state of machine: ')
    printState()

def sign_extend(num: int):
    if num & (1 << 15):
        num -= (1 << 16)
    return num

def convert_32bit(n):
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


while (ifRunning):

    printState()
    machine_code = int(mem[pc])
    # print(machine_code)
    opcode = (machine_code >> 22) & 0b0111

    # select 2 MSB of opcode

    # R-type
    if ((opcode & 0b110) >> 1) == 0:
        # set bit 15-3 to 0 (not used)
        inst = machine_code & 0b1111110000000000000111
        # select rs, rt, rd
        # print(bin(inst))
        rs = (inst >> 19) & 0b0111
        rt = (inst >> 16) & 0b0111
        rd = inst & 0b0111
        # select bit 0 of opcode
        # print("opp", opcode)
        if (opcode & 0b01) == 0:  # and
            add_op(rs, rt, rd)
        else:  # nand
            nand_op(rs, rt, rd)

    # I-type
    elif (((opcode & 0b110) >> 1) == 1) | (opcode == 0b100):
        # set nothing
        inst = machine_code & 0b1111111111111111111111
        # select rs, rt, rd
        rs = (inst >> 19) & 0b0111
        rt = (inst >> 16) & 0b0111
        # select bit 15-0 to offset
        offset = sign_extend(inst & 0b1111111111111111)
        # print("inst" , inst)
        offset = convert_32bit(offset)

        # lw or sw
        # print("opp", opcode)
        if ((opcode & 0b110) >> 1) == 1:
            # select bit 0 of opcode
            if (opcode & 0b011) == 2:  # lw
                lw_op(rs, rt, offset)
            else:  # sw
                sw_op(rs, rt, offset)
                # beq
        else:
            # print(offset , bin(offset))
            beq_op(rs, rt, offset)

    # J-type
    elif opcode == 0b101:
        # set bit 15-0 to 0 (not used)
        inst = machine_code & 0b1111110000000000000000
        # select rs, rt, rd
        rs = (inst >> 19) & 0b0111
        rt = (inst >> 16) & 0b0111
        # jalr
        jalr_op(rs, rt)

    # O-type
    elif (opcode & 0b110) >> 1 == 3:
        # set bit 21-0 to 0 (not used)
        inst = machine_code & 0b1110000000000000000000000
        # select bit 0 of opcode
        if (opcode & 0b01) == 0:  # halt
            halt_op()
            ifRunning = False
    ex_num += 1


print_halted()