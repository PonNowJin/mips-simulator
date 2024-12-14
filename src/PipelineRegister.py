class PipelineRegister:
    def __init__(self):
        self.instruction = None     # 當前指令
        self.opcode = None   # 指令type
        self.pc = 0                 # 程式計數器
        self.read_data1 = 0         # 暫存器讀取的值1
        self.read_data2 = 0         # 暫存器讀取的值2
        self.imm = 0                # 立即值
        self.result = 0             # EX 階段運算結果
        self.mem_data = 0           # MEM 階段讀取的記憶體值
        self.write_reg = 0          # 目標寫入暫存器
        
        # 個個階段需要的 signal
        self.WB_signal = None
        self.MEM_signal = None
        self.EXE_signal = None
        
        