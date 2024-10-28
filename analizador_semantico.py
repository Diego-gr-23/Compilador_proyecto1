class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors = []
        self.declared_variables = set()

    def analyze(self):
        i = 0
        while i < len(self.tokens):
            token, token_type = self.tokens[i]

            # Agregar a variables declaradas
            if token_type == "Palabra Reservada" and token in ["entero", "decimal", "booleano", "cadena"]:
                if i + 1 < len(self.tokens) and self.tokens[i + 1][1] == "Identificador":
                    self.declared_variables.add(self.tokens[i + 1][0])
            
            # Verificación de uso de variables no declaradas
            elif token_type == "Identificador" and token not in self.declared_variables:
                self.errors.append(f"Error: Variable '{token}' no declarada")

            i += 1

    def get_errors(self):
        return self.errors
