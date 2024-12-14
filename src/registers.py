class Registers:
    def __init__(self):
        # 32個暫存器, $0固定為0, 其他設為1
        self.registers = [1] * 32
        self.registers[0] = 0
        
    def read(self, reg_num):
        """ 讀取暫存器的值 """
        if 0 <= reg_num < 32:
            return self.registers[reg_num]
        raise ValueError("Invalid register number")
    
    def write(self, reg_num, value):
        """ 寫入暫存器的值 ($0不能寫入) """
        if reg_num == 0:
            return
        if 0 <= reg_num < 32:
            self.registers[reg_num] = value
        else:
            raise ValueError("Invalid register number")
        
    def dump(self):
        """ 顯示所有暫存器的值 """
        for i, val in enumerate(self.registers):
            print(f"${i}: {val}")
            
    