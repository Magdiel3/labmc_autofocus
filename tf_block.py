import control
import numpy as np

current_blocks = {}

class tf_block:
    block = {}
    def __init__(self, id_name, disp_name, fn_name, num, den):
        current_blocks[id_name] = {
            "disp_name": disp_name,
            "fn_name": fn_name,
            "num": num,
            "den": den
        }
        self.disp_name = disp_name
        self.fn_name = fn_name
        self.num = num
        self.den = den

        self.tf = control.tf(num, den)
        current_blocks[id_name]["tf"] = self.tf

    def get_current_blocks(self):
        return current_blocks.keys()

    def print_tf(self):
        print(f"{self.fn_name} -> {self.disp_name}:", self.tf)