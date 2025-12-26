from frame import Frame
import sys

CODE: list[list[str]] = None  # Lista de instruções
LABELS: dict[str,int] = None  # Lista de marcadores
PC = 0                        # Program Counter
STACK: list[Frame] = []       # Pilha de frames (chamadas de funções)
GLOBALS = {}                  # Variáveis globais
PARAMETERS = []               # Fila de parâmetros usado pela instrução PARAM

def read_code(dir):
    with open(dir,'+r') as file:
        code = file.read()
        
    code = code.split('\n')
    labels = {}
    for i, line in enumerate((code)):
        code[i] = line = line.split(' ')
        if line[0] == 'LABEL':
            labels[line[1]] = i
    return code, labels

def current_frame():
    global STACK
    return STACK[-1] if len(STACK) else None

def code_type(idx):
    return CODE[idx][0]

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

    global GLOBALS, STACK

    # id é número?
    val = is_number(id)
    if val is not None:
        return val
    
    # id é uma váriável global?
    val = GLOBALS.get(id,None)
    if val is not None:
        return val
    
    # id é um argumento de função ou variável local?
    frame = current_frame()
    val = frame.get_var(id)
    if val is not None:
        return to_value(val)
    return None

def LOAD():
    global PC, GLOBALS, STACK
    a,b = get_addresses()

    try:
        if b in GLOBALS:
            b = GLOBALS[b]
        elif b in current_frame().variables:
            b = current_frame().get_var(b)
    except:
        1
        
    b = to_value(b)

    if a in GLOBALS:
        GLOBALS[a] = b
    else:
        try:
            if a not in current_frame().variables:
                current_frame().new_var(a)
            current_frame().set_var(a,b)
        except:
            GLOBALS[a] = b
    
    PC+=1

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
    PC = LABELS[label]

def BGT():
    global PC
    a,b,label = get_addresses()

    if to_value(a) > to_value(b):
        PC = LABELS[label]
    else:
        PC += 1

def BGE():
    global PC
    a,b,label = get_addresses()
    if to_value(a) >= to_value(b):
        PC = LABELS[label]
    else:
        PC += 1

def BLT():
    global PC
    a,b,label = get_addresses()
    if to_value(a) < to_value(b):
        PC = LABELS[label]
    else:
        PC += 1

def BLE():
    global PC
    a,b,label = get_addresses()
    if to_value(a) <= to_value(b):
        PC = LABELS[label]
    else:
        PC += 1

def PARAM():
    global PC, PARAMETERS
    a = get_addresses()[0]
    PARAMETERS.append(to_value(a))
    
    PC += 1

def CALL():
    global PC, PARAMETERS, STACK, LABELS
    a, b = get_addresses()
    params = {}
    for i in range(to_value(b)):
        aux = PARAMETERS.pop(0)
        params[f'a{i}'] = to_value(aux)
    PARAMETERS.clear()
    
    STACK.append(Frame(PC+1,params))
    PC = LABELS.get(a,None)

def RETURN():
    global PC, STACK, GLOBALS
    a = get_addresses()[0]
    GLOBALS['ra'] = to_value(a)
    # print(len(STACK))
    PC = current_frame().static_link
    STACK.pop()

def PRINT():
    global PC
    a = get_addresses()[0]
    print(to_value(a))

    PC += 1

def main():
    HANDLER = {
        'LD': LOAD,
        'ADD': ADD,
        'SUB': SUB,
        'MULT': MULT,
        'DIV': DIV,
        'LABEL': LABEL,
        'J': JUMP,
        'BGT': BGT,
        'BGE': BGE, 
        'BLT': BLT,
        'BLE': BLE,
        'PARAM': PARAM,
        'CALL': CALL,
        'RET': RETURN,
        'PRINT': PRINT,
        '': None
    }
    args = sys.argv
    if len(args)<=1:
        return
    global CODE, LABELS, PC
    CODE, LABELS = read_code(args[1])
    PC = 0

    while code_type(PC) != 'LABEL':
        HANDLER[code_type(PC)]()

    STACK.append(Frame())
    PC = LABELS.get('main',None)

    while PC is not None:
        func = code_type(PC)
        if func:
            HANDLER[code_type(PC)]()
        else:
            PC += 1

if __name__ == "__main__":
    main()