from registers import Registers
from memory import Memory
from pipeline import PipelineSimulator
from pathlib import Path


#####TODO#####
# branch
##############

def main():
    # 取得 input 內的 file
    current_file = Path(__file__)
    parent_dir = current_file.parent.parent
    input_file = parent_dir / 'input' / 'test2.txt'
    
    # 初始化暫存器與記憶體
    instruct_memory = Memory(size=32)
    instruct_memory.load_instruction(input_file)
    instruct_memory.dump()
    pipeline = PipelineSimulator(instruct_memory, debug_reg_mem=False, debug_pipeline_reg=False)
    pipeline.run()
    
if __name__ == "__main__":
    main()
    