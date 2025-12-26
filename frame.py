class Undefined:
    '''
    Classe que representa modelo apra variáveis sem valor atribuído
    '''
    pass

UNDEFINED = Undefined()

class Frame():
    def __init__(   
        self, 
        static_link=None,
        args={}
    ):
        self.static_link = static_link
        self.args = args
        self.variables = {}

    def new_var(self, id):
        if id in self.variables:
            raise Exception("ID de variável já existente no escopo.")
        self.variables[id] = UNDEFINED

    def get_var(self, id):
        val = self.variables.get(id,None)

        if val is None:
            return self.args.get(id,None)
        return val
    
    def set_var(self, id, val):
        if id in self.args:
            self.args[id] = val
        elif id in self.variables:
            self.variables[id] = val
