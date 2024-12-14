from registers import Registers
from memory import Memory

def main():
    # 初始化暫存器與記憶體
    registers = Registers()
    memory = Memory(size=32)
    
    print("Initial Register Values:")
    registers.dump()
    
    print("\nInitial Memory Values:")
    memory.dump()
    
    # 測試讀寫功能
    print("\nTesting Register Write:")
    registers.write(2, 10)
    print(f"Register $2 = {registers.read(2)}")

    print("\nTesting Memory Write:")
    memory.write(4, 20)
    print(f"Memory[4] = {memory.read(4)}")

if __name__ == "__main__":
    main()