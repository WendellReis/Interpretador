class Frame():
    def __init__(   
        self, 
        static_link=None,
        variables={},
        args={}
    ):
        self.static_link = static_link
        self.variables = variables
        self.args = args

    def new_var(self, id, val):
        if id in self.variables:
            raise Exception("ID de variável já existente no escopo.")
        self.variables[id] = val

    def get_var(self, id):
        return self.variables.get(id,None)
    
    def set_var(self, id, val):
        self.variables[id] = val
