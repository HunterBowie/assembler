import time
INSTRUCTIONS = [
    "nop",
    "lda",
    "ldi",
    "sta",
    "add",
    "sub",
    "inc",
    "dec",
    "jmp",
    "jc",
    "jn",
    "jz",
    "inw",
    "inx",
    "outy",
    "outz",
    "call",
    "ret",
    "push",
    "pull",
    "pop",
    "null",
    "null",
    "null",
    "null",
    "null",
    "null",
    "null",
    "null",
    "null",
    "null",
    "hlt"
]

HEX_CHARS = [
    "0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"
]

BIN_CHARS = [
    "0","1"
]

ADDR_SPOT = "@ADDRESS"
DATA_SPOT = "@DATA"
INFO_SPOT = "@INFO"

class ASMSyntaxError(Exception):
    pass

def read_file(path, split=True):
    with open(path+".txt", "r") as f:
        data = f.read()
        if split:
            data = data.split("\n")
        return data

def write_file(path, data):
    with open(path+".txt", "w") as f:
        f.write(data)

def make_int(value):
    if value[:2] == "0b":
        value = value[2:]
        value = value[::-1]
        digit = 1
        num = 0
        for i in range(len(value)):
            num += BIN_CHARS.index(value[i]) * digit
            digit = digit * 2
        return num
    elif value[:2] == "0x":
        value = value[2:]
        value = value[::-1]
        digit = 1
        num = 0
        for i in range(len(value)):
            num += HEX_CHARS.index(value[i]) * digit
            digit = digit * 16
        return num
    else:
        return int(value)

def is_literal_value(value):
    try:
        int(value)
    except ValueError:
        pass
    else:
        return True
    if value[:2] == "0b":
        return True
    if value[:2] == "0x":
        return True
    return False


class Assembler:
    MEM_SIZE = 255
    def __init__(self):
        self.output = []
        self.data = []
    
    def _clean(self):
        self.data = [line.strip() for line in self.data]
        self.data = [line for line in self.data if line != ""]
        new_data = []
        for line in self.data:
            if ";" in line:
                parts = line.split(";")
                new_data.append(parts[0].strip())
                continue
            new_data.append(line)
        self.data = new_data
    
    
    
    def assemble(self, data):
        pass



def format_output(output, file):
    format_data = read_file(file, split=False)
    new_output = []
    for addr_data in output:
        addr, data = addr_data
        output_line = format_data.replace(ADDR_SPOT, str(addr))
        output_line = output_line.replace(DATA_SPOT, str(data))
        new_output.append(output_line)
    return new_output

def merge_to_string(value):
    string = ""
    for item in value:
        string = string + item
    return string

        

def main():
    labels = {}
    output = []
    assembly = read_file("input")
    assembly = clean_assembly(assembly)
    remove_lines = []
    addr = 0
    for line in assembly:
        if "#" in line: # variables
            mod_line = line.replace("#", "")
            store_value = "0"
            if "->" in mod_line:
                mod_line, store_value = mod_line.split(" -> ")
            mod_line = mod_line.strip()
            label, value = mod_line.split(" ")
            labels[label] = value
            output.append((value, to_int(store_value)))
            remove_lines.append(line)
            continue

        if ":" in line: # labels
            label, mod_line = line.split(":")
            mod_line = mod_line.strip()
            labels[label] = addr
            if mod_line == "":
                remove_lines.append(line)
                continue
            else:
                assembly[assembly.index(line)] = mod_line
        addr += 2
                

        
    
    for line in remove_lines:
        assembly.remove(line)
    
    addr = 0
    for line in assembly:
        if " " not in line:
            operation = line
            operand = "0"
        else:
            operation, operand = line.split(" ")

        if is_raw_value(operand):
            operand = to_int(operand)
        else:
            operand = int(labels[operand])
                
        output.append((addr, INSTRUCTIONS.index(operation)))
        output.append((addr+1, operand))
        addr += 2
    output = format_output(output, "format")
    string_output = merge_to_string(output)
    write_file("output", string_output)
    print(f"\nAssembled Program at {time.asctime()}\n")


main()
