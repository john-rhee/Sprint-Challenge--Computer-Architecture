"""CPU functionality."""

import sys


# Set variables
LDI = 0b10000010
HTL = 0b00000001
MUL = 0b10100010
PRN = 0b01000111
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.reg = [0b00000000] * 8

        self.pc = 0b00000000

        self.fl = 0b00000000

        self.ram = [0b00000000] * 256

    def load(self, ls8):
        """Load a program into memory."""

        address = 0

        with open(ls8, 'r') as ifile:
            
            for line in ifile:
                if line.strip() == '':
                    pass
                elif line.strip().startswith('#'):
                    pass
                else:
                    self.ram[address] = int(line.strip()[:8], 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    # Compare 2 registers
    def handle_CMP(self):
        register_0 = self.ram_read(self.pc+1)
        register_1 = self.ram_read(self.pc+2)
        self.alu('CMP', register_0, register_1)
        self.pc += 2

    # If CMP flag LGE is 001
    def handle_JEQ(self):
        if self.fl == 0b00000001:
            register = self.ram_read(self.pc+1)
            self.pc = self.reg[register] - 1
        else:
            self.pc += 1

    # Jump to regiester
    def handle_JMP(self):
        register = self.ram_read(self.pc+1)
        self.pc = self.reg[register] -1

    # If CMP flag LGE is NOT 001
    def handle_JNE(self):
        if self.fl != 0b00000001:
            register = self.ram_read(self.pc+1)
            self.pc = self.reg[register] - 1
        else:
            self.pc += 1

    # Load to register with value
    def handle_LDI(self):
        register = self.ram_read(self.pc+1)
        immediate = self.ram_read(self.pc+2)
        self.reg[register] = immediate
        self.pc += 2

    # Multiply 2 registers
    def handle_MUL(self):
        register_0 = self.ram_read(self.pc+1)
        register_1 = self.ram_read(self.pc+2)
        self.alu('MUL', register_0, register_1)
        self.pc += 2
    
    # Print from register
    def handle_PRN(self):
        register = self.ram_read(self.pc+1)
        print(self.reg[register])
        self.pc += 1

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # Read from RAM
    def ram_read(self, address):
        return self.ram[address]

    # Write to RAM with value
    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        while True:
            instruction = self.ram_read(self.pc)

            if instruction == HTL:
                break

            elif instruction == LDI:
                self.handle_LDI()

            elif instruction == MUL:
                self.handle_MUL()

            elif instruction == PRN:
                self.handle_PRN()

            elif instruction == CMP:
                self.handle_CMP()

            elif instruction == JEQ:
                self.handle_JEQ()

            elif instruction == JMP:
                self.handle_JMP()

            elif instruction == JNE:
                self.handle_JNE()

            self.pc += 1


