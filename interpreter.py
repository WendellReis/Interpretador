from frame import Frame
import sys

CODE: list[list[str]] = None  # Lista de instruções
LABLES: dict[str,int] = None  # Lista de marcadores
PC = 0                        # Program Counter
STACK: list[Frame] = []       # Pilha de frames (chamadas de funções)
GLOBALS = {}                  # Variáveis globais

def read_code(dir):
    with open(dir,'+r') as file:
        code = file.read()
        
    code = code.split('\n')
    labels = {}
    for i, line in enumerate((code)):
        line = line.split(' ')
        if line[0] == 'LABEL':
            labels[line[1]] = i
    return code, labels

def current_frame():
    return STACK[-1]

def code_type(idx):
    return CODE[idx][0]

def LOAD():
    pass

def get_addresses():
    '''
    Retorna os endereços que estão no comando atual
    '''
    addresses = CODE[PC][1:] # Retorna tudo menos o tipo da instrução
    return addresses

def is_number(val):
    '''
    Tenta converter uma string em número
    '''
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return None


def to_value(id):
    '''
    Retorna o valor numérico ou da variável associada a id
    '''

    # id é número?
    val = is_number(id)
    if val is not None:
        return val
    
    # id é uma váriável global?
    val = GLOBALS.get(id,None)
    if val is not None:
        return val
    
    # id é uma variável local?
    frame = current_frame()
    val = frame.get_var(id)
    if val is not None:
        return val
    return None


def ADD():
    global PC
    a,b,c = get_addresses()
    val = to_value(b) + to_value(c)

    if a in GLOBALS:
        GLOBALS[a] = val
    else:
        current_frame().set_var(a,val)

    PC += 1


def SUB():
    global PC
    a,b,c = get_addresses()
    val = to_value(b) - to_value(c)

    if a in GLOBALS:
        GLOBALS[a] = val
    else:
        current_frame().set_var(a,val)

    PC += 1

def MULT():
    global PC
    a,b,c = get_addresses()
    val = to_value(b)*to_value(c)

    if a in GLOBALS:
        GLOBALS[a] = val
    else:
        current_frame().set_var(a,val)

    PC += 1

def DIV():
        global PC
        a,b,c = get_addresses()

        try:
            val = to_value(b)/to_value(c)
        except ZeroDivisionError:
            val = 0

        if a in GLOBALS:
            GLOBALS[a] = val
        else:
            current_frame().set_var(a,val)

        PC += 1

def LABEL():
    global PC
    PC += 1

def JUMP():
    global PC
    label = get_addresses()[0]
    PC = LABLES[label]

def BGT():
    global PC
    a,b,label = get_addresses()
    if to_value(a) > to_value(b):
        PC = LABLES[label]
    else:
        PC += 1

def BGE():
    global PC
    a,b,label = get_addresses()
    if to_value(a) >= to_value(b):
        PC = LABLES[label]
    else:
        PC += 1

def BLT():
    global PC
    a,b,label = get_addresses()
    if to_value(a) < to_value(b):
        PC = LABLES[label]
    else:
        PC += 1

def BLE():
    global PC
    a,b,label = get_addresses()
    if to_value(a) <= to_value(b):
        PC = LABLES[label]
    else:
        PC += 1

def CALL():
    pass

def RETURN():
    pass

def main():
    HANDLER = {
        'LD': LOAD,
        'ADD': ADD,
        'SUB': SUB,
        'MULT': MULT,
        'DIV': DIV,
        'LABEL': LABEL,
        'J': JUMP,
        'CALL': CALL,
        'RET': RETURN,
    }
    args = sys.argv
    if len(args)<=1:
        return
    
    CODE, LABLES = read_code(args[1])
    print(CODE)

    STACK.append(Frame())
    PC = LABLES.get('main',None)

    while PC:
        HANDLER[code_type(PC)]()

if __name__ == "__main__":
    main()