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

        elif opcode == "sw":  # I-type: sw $rt, imm($rs)
            rt = int(parts[1][1:])
            imm = int(parts[2])
            rs = int(parts[3][1:])

            self.ID_EX.instruction = instruction
            self.ID_EX.read_data1 = self.registers.read(rs)
            self.ID_EX.read_data2 = self.registers.read(rt)  # SW 要寫入記憶體的值
            self.ID_EX.imm = imm
            self.ID_EX.write_reg = None  # SW 不寫入暫存器
            
            self.ID_EX.EXE_signal = {'RegDst': 'X', 'ALUSrc': 1, }
            self.ID_EX.MEM_signal = {'Branch': 0, 'MemRead': 0, 'MemWrite': 1}
            self.ID_EX.WB_signal = {'RegWrite': 0, 'MemtoReg': 'X'}

        elif opcode == "add" or "sub":  # R-type: add $rd, $rs, $rt
            rd = int(parts[1][1:])
            rs = int(parts[2][1:])
            rt = int(parts[3][1:])

            self.ID_EX.instruction = instruction
            self.ID_EX.read_data1 = self.registers.read(rs)
            self.ID_EX.read_data2 = self.registers.read(rt)
            self.ID_EX.imm = 0
            self.ID_EX.write_reg = rd
            
            self.ID_EX.EXE_signal = {'RegDst': 1, 'ALUSrc': 0, }
            self.ID_EX.MEM_signal = {'Branch': 0, 'MemRead': 0, 'MemWrite': 0}
            self.ID_EX.WB_signal = {'RegWrite': 1, 'MemtoReg': 0}

        elif opcode == "beq":  # I-type: beq $rs, $rt, imm
            rs = int(parts[1][1:])
            rt = int(parts[2][1:])
            imm = int(parts[3])

            self.ID_EX.instruction = instruction
            self.ID_EX.read_data1 = self.registers.read(rs)
            self.ID_EX.read_data2 = self.registers.read(rt)
            self.ID_EX.imm = imm
            self.ID_EX.write_reg = None
            
            self.ID_EX.EXE_signal = {'RegDst': 'X', 'ALUSrc': 0, }
            self.ID_EX.MEM_signal = {'Branch': 1, 'MemRead': 0, 'MemWrite': 0}
            self.ID_EX.WB_signal = {'RegWrite': 0, 'MemtoReg': 'X'}

        else:
            print(f"ID: Unsupported instruction {instruction}")
            return

        # 顯示解碼結果
        print(f"ID: Decode instruction {instruction}")
        print(f"    EXE_signal = {self.ID_EX.EXE_signal}, rs = {rs}, rt = {rt if 'rt' in locals() else 'N/A'}, "
            f"rd = {rd if 'rd' in locals() else 'N/A'}, imm = {imm if 'imm' in locals() else 'N/A'}")

            
    def execution(self):
        """ EXE: Excution 階段 """
        instruction = self.ID_EX.instruction
        if instruction is None:
            return
        
        opcode = self.ID_EX.opcode
        read_data1 = self.ID_EX.read_data1
        read_data2 = self.ID_EX.read_data2
        imm = self.ID_EX.imm
        
        # ALU 運算
        if opcode == 'add':
            result = read_data1 + read_data2
        elif opcode == 'sub':
            result = read_data1 - read_data2
        elif opcode == 'lw' or 'sw':
            result = read_data1 + imm
        else:
            result = 0
            
        # 設定 EX/MEM Pipeline Reg
        self.EX_MEM.result = result
        self.EX_MEM.write_reg = self.ID_EX.write_reg
        
        # signal 傳遞
        self.EX_MEM.MEM_signal = self.ID_EX.MEM_signal
        self.EX_MEM.WB_signal = self.ID_EX.WB_signal
        
        print(f"EX: Execute instruction {instruction} | result = {result}")
        
        
    def memory_access(self):
        """ MEM: Memory Access 階段 """
        instruction = self.EX_MEM.instruction
        if instruction is None:
            return
        
        opcode = self.EX_MEM.opcode
        result = self.EX_MEM.result
        mem_data = 0
        
        # memory access
        if opcode == 'lw':
            mem_data = self.memory.read(result)
        elif opcode == 'sw':
            self.memory.write(result, self.EX_MEM.read_data2)
        
        # 設定 MEM/WB Pipeline Reg
        self.MEM_WB.result = result
        self.MEM_WB.mem_data = mem_data
        self.MEM_WB.write_reg = self.EX_MEM.write_reg
        
        # signal 傳遞
        self.MEM_WB.WB_signal = self.EX_MEM.WB_signal
        
        print(f"MEM: Memory Access | mem_data = {mem_data}")
        

    def write_back(self):
        """ WB: Write Back 階段 """
        
        