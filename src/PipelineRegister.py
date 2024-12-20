class PipelineRegister:
    def __init__(self):
        self.stall = False  # 是否需要停滯
        self.instruction = None     # 當前指令
        self.opcode = None          # 指令type
        self.pc = 0                 # 程式計數器
        self.read_data1 = 0         # 暫存器讀取的值1
        self.read_data2 = 0         # 暫存器讀取的值2
        self.imm = 0                # 立即值
        self.result = 0             # EX 階段運算結果
        self.mem_data = 0           # MEM 階段讀取的記憶體值
        self.write_reg = 0          # 目標寫入暫存器(rd)
        self.Rt = None              # rt
        self.Rs = None              # rs
        
        # 個個階段需要的 signal
        self.WB_signal = {'RegWrite': 0, 'MemtoReg': 0}
        self.MEM_signal = {'Branch': 0, 'MemRead': 0, 'MemWrite': 0}
        self.EXE_signal = {'RegDst': 0, 'ALUSrc': 0, }
        
    def dump(self):
        """
        打印 PipelineRegister 的當前狀態。
        """
        print("Pipeline Register Dump:")
        print(f"  Stall: {self.stall}")
        print(f"  Instruction: {self.instruction}")
        print(f"  Opcode: {self.opcode}")
        print(f"  PC: {self.pc}")
        print(f"  Read Data 1: {self.read_data1}")
        print(f"  Read Data 2: {self.read_data2}")
        print(f"  Immediate: {self.imm}")
        print(f"  Result: {self.result}")
        print(f"  Memory Data: {self.mem_data}")
        print(f"  Write Register: {self.write_reg}")
        print(f"  Rt: {self.Rt}")
        print(f"  Rs: {self.Rs}")
        print('------\n')
        
    def reset(self):
        """重置所有成員變數"""
        self.stall = False
        self.instruction = None
        self.opcode = None
        self.pc = 0
        self.read_data1 = 0
        self.read_data2 = 0
        self.imm = 0
        self.result = 0
        self.mem_data = 0
        self.write_reg = 0
        self.Rt = None              
        self.Rs = None

        # 重置所有 signal
        self.WB_signal = {'RegWrite': 0, 'MemtoReg': 0}
        self.MEM_signal = {'Branch': 0, 'MemRead': 0, 'MemWrite': 0}
        self.EXE_signal = {'RegDst': 0, 'ALUSrc': 0, }
        
        