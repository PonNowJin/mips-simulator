class Memory:
    def __init__(self, size=32):
        # 記憶體初始化，每個 word 預設為 1
        self.memory = [1] * size
        
    def read(self, address):
        """ 讀取 memory 值 """
        if 0 <= address < len(self.memory):
            return self.memory[address]
        raise ValueError("Invalid memory address")
    
    def write(self, address, value):
        """ 寫入 memory 值 """
        if 0 <= address < len(self.memory):
            self.memory[address] = value
        else:
            raise ValueError("Invalid memory address")
        
    def dump(self):
        """ 顯示 memory 內容 """
        for i, val in enumerate(self.memory):
            print(f"Memory[{i}]: {val}")
            