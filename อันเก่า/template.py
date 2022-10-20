#########################################################
#  Template code for a RISC-V RV32I emulator            
#  =========================================
#  Variable list
#  RAM = Byte array containing RAM values for the CPU
#  PC = Program Counter
#  REGISTER = List containing the 32 register values (x0-x31) 
# 
#  CC-BY-NC
#  Arnan Sipitakiat. Dept. Computer Engineering. Chiang Mai University, Thailand


import struct
import os, sys

RAM_SIZE = 1024         # bytes

# 1. Open and read your binary file here
# ======================================
f = open(os.path.dirname(sys.argv[0])+"\simple_add.bin", "rb")
RAM = f.read()  # read contents into RAM variable
f.close()

instruction_count =  int(len(RAM)/4)

# Create all RAM locations 
RAM = RAM + bytearray([0]*(RAM_SIZE-instruction_count))


# 2. print the commands
# =====================
print ("Binary Commands")
print ("===============")
i = 0
while i < instruction_count:      
    CMD = struct.unpack('<i', RAM[i*4:(i*4)+4])[0]    # combine 4 bytes and store the 32 bit result in variable CMD
    print ('{0:032b}'.format(CMD))              # print CMD in binary
    i = i+1

# 3. Initialize the virtual machine
# =================================

REGISTER=[0] * 32       # Init array with 32 locations. Values = 0
PC = 0                  # Program Counter starts at 0


# 4.Execute the program 
# =====================

print("Execution")
print("=========")
CMD = struct.unpack('<i', RAM[PC:PC+4])[0]      # read the command. Combine 4 bytes. 
PC = PC + 4

while (CMD != 0):
    print("\nPC = ",'{0:03}'.format(PC-4))
    opcode = CMD & 0b1111111

    if (opcode) == 0b0010011:                  # if I-format instruction. (See Table 19.2 of the RISC-V Spec)        
        print("Type = I-Format")
        # fetch command parameters
        RD = (CMD >> 7) & 0b11111                   # RD = bits 7-11
        FUNCT3 = (CMD >> 12) & 0b111                # FUNCT3 = bits 12-14
        RS1 = (CMD >> 15) & 0b11111                 # RS1 = bits 15-19
        IMM = (CMD >> 20) & 0b111111111111          # IMM = bits 20-31

        if (FUNCT3 == 0b000):                       # if 'ADDI' command
            print("Command = ADDI")
            # execute
            REGISTER[RD] = REGISTER[RS1] + IMM

    
    if (opcode) == 0b0110011:                  # if R-format instruction. (See Table 19.2 of the RISC-V Spec)
        print ("Type = R-Format")
        # fetch command parameters
        RD = (CMD >> 7) & 0b11111                   # RD = bits 7-11
        FUNCT3 = (CMD >> 12) & 0b111                # FUNCT3 = bits 12-14
        RS1 = (CMD >> 15) & 0b11111                 # RS1 = bits 15-19
        RS2 = (CMD >> 20) & 0b11111                 # RE2 = bits 20-24
        FUNCT7 = (CMD >>25) & 0b1111111             # FUNCT7 = bits 25-31

        r_format_cmd = (FUNCT7 << 3) | FUNCT3       # combine the 10-bit command
       
        if (r_format_cmd == 0):                     # if 'ADD' command
            print("Command = ADD")
            # execute
            REGISTER[RD] = REGISTER[RS1] + REGISTER[RS2]


    CMD = struct.unpack('<i', RAM[PC:PC+4])[0]      # read the next command 
    PC = PC + 4




# 5. Print all register values
# ============================

print ("\nRegister contents")
print ("=================")
i=0
for REG in REGISTER:
   print ("x",i, "=", REG) 
   i=i+1

# 6. Print RAM values
# ===================
# Print the range defined by the code.
print ("RAM contents")
print ("============")

RAM_START = 0
RAM_STOP = 16   # must be a incremental of 4 (1 word)

for i in range(RAM_START, RAM_STOP, 4):
    print ("RAM", '{0:02}'.format(i), "=", hex(RAM[i]),":",hex(RAM[i+1]),":",hex(RAM[i+2]),":",hex(RAM[i+3]))

