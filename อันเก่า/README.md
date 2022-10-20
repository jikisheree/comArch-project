# riscv-isa-emu
Template code for a RISC-V ISA emulator lab project

Modify the template (template.py) to support the following RISC-V RV32I commands

## Binary Command List 				
* R-Format	ADD	SUB		
* I-Format	ADDI	LW	JALR	
* S-Format	SW			
* B-Format	BEQ	BNE	BLT	BGE
* U-Format	LUI			
* J-Format	JAL			

The template already handles the following
* Reading binary commands into RAM
* Demontrates how to implement ADD, ADDI
* Prints the contents of Registers, RAM
