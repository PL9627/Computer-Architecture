"""CPU functionality."""

import sys


HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.fl = 0b00000000

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        """ program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1 """
        print(sys.argv)

        if len(sys.argv) != 2:
            print("Wrong number of arguments, please pass file name")
            sys.exit(1)

        with open(sys.argv[1]) as f:
            for line in f:
                line_split = line.split('#')
                IR = line_split[0].strip()

                if IR == '':
                    continue
                IR_num = int(IR, 2)
                self.ram[address] = IR_num
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL": 
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV": 
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        self.reg[self.sp] = len(self.ram) - 1

        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                self.running = False
                self.pc += 1
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            elif IR == ADD:
                reg1 = self.ram[self.pc + 1]
                reg2 = self.ram[self.pc + 2]
                
                val1 = self.reg[reg1]
                val2 = self.reg[reg2]

                self.reg[reg1] = val1 + val2
                self.pc += 3
            elif IR == PUSH:
                reg_address = self.ram_read(self.pc + 1)
                push_val = self.reg[reg_address]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = push_val
                self.pc += 2
            elif IR == POP:
                reg_address = self.ram_read(self.pc + 1)
                pop_val = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
                self.reg[reg_address] = pop_val
                self.pc += 2
            elif IR == CALL:
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                reg_num = self.ram[self.pc + 1]
                print(self.ram[-2:])
                self.pc = self.reg[reg_num]
            elif IR == RET:
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
            elif IR == CMP:
                pass
            elif IR == JEQ:
                pass
            elif IR == JMP:
                pass
            elif IR == JNE:
                pass