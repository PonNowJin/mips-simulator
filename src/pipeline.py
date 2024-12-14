from PipelineRegister import PipelineRegister
from memory import Memory
from registers import Registers

class PipelineSimulator:
    def __init__(self):
        # 初始化記憶體、暫存器和 PC
        self.memory = Memory()
        self.registers = Registers()
        self.pc = 0
        
        # 初始化 Pipeline 暫存器
        self.IF_ID = PipelineRegister()
        self.ID_EX = PipelineRegister()
        self.EX_MEM = PipelineRegister()
        self.MEM_WB = PipelineRegister()
        
    def instruction_fetch(self):
        """ IF: Instruction Fetch """
        instruction = self.memory.read(self.pc // 4)
        self.IF_ID.instruction = instruction
        self.IF_ID.pc = self.pc
        print(f"IF: Fetch instruction {instruction} at PC = {self.pc}")
        self.pc += 4
        
    def instruction_decode(self):
        """ ID: Instruction Decode 階段 """
        instruction = self.IF_ID.instruction  # 取得字串格式的指令
        if instruction is None:
            return

        # 將指令字串拆分
        parts = instruction.replace(",", "").replace("(", " ").replace(")", "").split()
        opcode = parts[0]  # 指令名稱，例如 lw, add, beq

        # 根據不同指令分類解析
        if opcode == "lw":  # I-type: lw $rt, imm($rs)
            rt = int(parts[1][1:])  # 取得目標暫存器號碼，例如 $2 -> 2
            imm = int(parts[2])     # 立即值，例如 8
            rs = int(parts[3][1:])  # 基址暫存器，例如 $0 -> 0

            # 填入 ID/EX Pipeline Register
            self.ID_EX.instruction = instruction
            self.ID_EX.opcode = opcode
            self.ID_EX.read_data1 = self.registers.read(rs)
            self.ID_EX.read_data2 = 0  # LW 不使用第二個讀取值
            self.ID_EX.imm = imm
            self.ID_EX.write_reg = rt
            
            self.ID_EX.EXE_signal = {'RegDst': 0, 'ALUSrc': 1, }
            self.ID_EX.MEM_signal = {'Branch': 0, 'MemRead': 1, 'MemWrite': 1}
            self.ID_EX.WB_signal = {'RegWrite': 1, 'MemtoReg': 1}
            
        # 做到這 -----------------------------------------------------  

        elif opcode == "sw":  # I-type: sw $rt, imm($rs)
            rt = int(parts[1][1:])
            imm = int(parts[2])
            rs = int(parts[3][1:])

            self.ID_EX.instruction = instruction
            self.ID_EX.EXE_signal = "MEM"
            self.ID_EX.read_data1 = self.registers.read(rs)
            self.ID_EX.read_data2 = self.registers.read(rt)  # SW 要寫入記憶體的值
            self.ID_EX.imm = imm
            self.ID_EX.write_reg = None  # SW 不寫入暫存器

        elif opcode == "add":  # R-type: add $rd, $rs, $rt
            rd = int(parts[1][1:])
            rs = int(parts[2][1:])
            rt = int(parts[3][1:])

            self.ID_EX.instruction = instruction
            self.ID_EX.EXE_signal = "ALU"
            self.ID_EX.read_data1 = self.registers.read(rs)
            self.ID_EX.read_data2 = self.registers.read(rt)
            self.ID_EX.imm = 0
            self.ID_EX.write_reg = rd

        elif opcode == "beq":  # I-type: beq $rs, $rt, imm
            rs = int(parts[1][1:])
            rt = int(parts[2][1:])
            imm = int(parts[3])

            self.ID_EX.instruction = instruction
            self.ID_EX.EXE_signal = "BRANCH"
            self.ID_EX.read_data1 = self.registers.read(rs)
            self.ID_EX.read_data2 = self.registers.read(rt)
            self.ID_EX.imm = imm
            self.ID_EX.write_reg = None

        else:
            print(f"ID: Unsupported instruction {instruction}")
            return

        # 顯示解碼結果
        print(f"ID: Decode instruction {instruction}")
        print(f"    EXE_signal = {self.ID_EX.EXE_signal}, rs = {rs}, rt = {rt if 'rt' in locals() else 'N/A'}, "
            f"rd = {rd if 'rd' in locals() else 'N/A'}, imm = {imm if 'imm' in locals() else 'N/A'}")

            
                